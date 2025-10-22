from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
import logging

from .models import EmailConfiguration, BackupConfiguration, BackupHistory
from .forms import EmailConfigurationForm, TestEmailForm
from .email_service import send_test_email
from .smtp_checker import check_smtp_connection
from .backup_service import BackupService

logger = logging.getLogger(__name__)

# Hàm kiểm tra quyền admin
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role in ['sm', 'admin'])

@login_required
@user_passes_test(is_admin)
def email_settings(request):
    """
    Hiển thị và cập nhật cấu hình email SMTP
    """
    # Lấy cấu hình email hiện tại hoặc tạo mới nếu chưa có
    config = EmailConfiguration.objects.first()
    
    if request.method == 'POST':
        if 'reset_test' in request.POST:
            # Reset trạng thái test email
            if config:
                config.last_test_date = None
                config.last_test_success = None
                config.save()
                messages.success(request, 'Đã reset trạng thái test email!')
            return redirect('email_settings')
            
        elif 'save_config' in request.POST:
            if config:
                # Cập nhật cấu hình hiện có
                form = EmailConfigurationForm(request.POST, instance=config)
            else:
                # Tạo mới cấu hình
                form = EmailConfigurationForm(request.POST)
                
            if form.is_valid():
                email_config = form.save(commit=False)
                email_config.updated_by = request.user
                
                if not email_config.created_by:
                    email_config.created_by = request.user
                    
                email_config.save()
                messages.success(request, 'Đã cập nhật cấu hình email thành công!')
                return redirect('email_settings')
        
        elif 'test_email' in request.POST:
            # Xử lý form test email
            test_form = TestEmailForm(request.POST)
            
            # Kiểm tra config trước khi xử lý
            if not config or not config.is_active:
                messages.error(request, 'Vui lòng cấu hình và kích hoạt SMTP trước khi gửi email test!')
                return redirect('email_settings')
            
            if test_form.is_valid():
                recipient = test_form.cleaned_data['recipient']
                subject = test_form.cleaned_data['subject']
                message = test_form.cleaned_data['message']
                
                # Cài đặt biến SMTP settings từ cấu hình trong DB
                settings.EMAIL_HOST = config.smtp_host
                settings.EMAIL_PORT = config.smtp_port
                settings.EMAIL_TIMEOUT = config.smtp_timeout / 1000  # Convert từ ms sang giây
                settings.EMAIL_CONNECTION_TIMEOUT = config.smtp_conn_timeout / 1000  # Convert từ ms sang giây
                
                # Cài đặt xác thực
                if config.auth_method == 'normal':
                    settings.EMAIL_HOST_USER = config.smtp_username
                    settings.EMAIL_HOST_PASSWORD = config.smtp_password
                else:  # 'none'
                    settings.EMAIL_HOST_USER = ''
                    settings.EMAIL_HOST_PASSWORD = ''
                
                settings.EMAIL_USE_TLS = config.use_tls
                settings.EMAIL_USE_SSL = config.use_ssl
                settings.DEFAULT_FROM_EMAIL = config.from_email
                
                # Thêm các cài đặt bổ sung để đảm bảo kết nối ổn định với mail server nội bộ
                settings.EMAIL_TIMEOUT = 60  # Tăng timeout lên 60 giây
                settings.EMAIL_USE_LOCALTIME = True  # Sử dụng thời gian địa phương
                
                # Kiểm tra kết nối SMTP trước
                logger.info(f"Kiểm tra kết nối SMTP đến {config.smtp_host}:{config.smtp_port}")
                
                conn_success, conn_msg = check_smtp_connection(config)
                if not conn_success:
                    # Lưu thông tin kết nối thất bại
                    config.last_test_success = False
                    config.last_test_date = timezone.now()
                    config.save(update_fields=['last_test_success', 'last_test_date'])
                    
                    messages.error(request, f'Lỗi kết nối SMTP: {conn_msg}')
                    return redirect('email_settings')
                
                # Kết nối OK, thử gửi email
                logger.info(f"Kết nối SMTP OK, thử gửi email đến {recipient}")
                success, msg = send_test_email(recipient, subject, message)
                
                if success:
                    messages.success(request, f'Gửi email thành công đến {recipient}!')
                else:
                    messages.error(request, f'Lỗi khi gửi email: {msg}')
                
                return redirect('email_settings')
                
            form = EmailConfigurationForm(instance=config)
    else:
        form = EmailConfigurationForm(instance=config)
        
    test_form = TestEmailForm()
    
    return render(request, 'system_settings/email_settings.html', {
        'form': form,
        'test_form': test_form,
        'config': config,
        'title': 'Cấu hình Email SMTP'
    })


# ================== BACKUP VIEWS ==================

@login_required
@user_passes_test(is_admin)
def backup_settings(request):
    """
    Hiển thị trang quản lý backup
    """
    # Lấy hoặc tạo cấu hình backup
    config, created = BackupConfiguration.objects.get_or_create(
        defaults={
            'created_by': request.user,
            'backup_frequency': 'manual',
            'include_database': True,
            'include_media': True,
            'max_backups_keep': 10,
        }
    )
    
    if request.method == 'POST':
        # Cập nhật cấu hình backup
        config.backup_frequency = request.POST.get('backup_frequency', 'manual')
        config.backup_time = request.POST.get('backup_time') or None
        config.include_database = 'include_database' in request.POST
        config.include_media = 'include_media' in request.POST
        config.max_backups_keep = int(request.POST.get('max_backups_keep', 10))
        config.is_active = 'is_active' in request.POST
        config.updated_by = request.user
        config.save()
        
        messages.success(request, 'Cập nhật cấu hình backup thành công!')
        return redirect('backup_settings')
    
    # Lấy danh sách backup history
    backup_list = BackupHistory.objects.all().order_by('-created_at')[:20]
    
    return render(request, 'system_settings/backup_settings.html', {
        'config': config,
        'backup_list': backup_list,
        'title': 'Quản lý Backup'
    })


@login_required
@user_passes_test(is_admin)
def create_backup(request):
    """
    Tạo backup mới
    """
    if request.method == 'POST':
        backup_type = request.POST.get('backup_type', 'full')
        
        try:
            backup_service = BackupService()
            backup_history = backup_service.create_backup(
                backup_type=backup_type,
                user=request.user,
                is_auto=False
            )
            
            messages.success(
                request,
                f'Tạo backup thành công! File: {backup_history.backup_name} '
                f'({backup_history.get_file_size_display()})'
            )
        except Exception as e:
            logger.error(f"Lỗi khi tạo backup: {str(e)}")
            messages.error(request, f'Lỗi khi tạo backup: {str(e)}')
    
    return redirect('backup_settings')


@login_required
@user_passes_test(is_admin)
def download_backup(request, backup_id):
    """
    Tải backup file
    """
    backup = get_object_or_404(BackupHistory, id=backup_id)
    
    if not backup.backup_file:
        raise Http404("Backup file không tồn tại")
    
    try:
        response = FileResponse(
            backup.backup_file.open('rb'),
            as_attachment=True,
            filename=backup.backup_name
        )
        return response
    except Exception as e:
        logger.error(f"Lỗi khi tải backup: {str(e)}")
        messages.error(request, f'Lỗi khi tải file backup: {str(e)}')
        return redirect('backup_settings')


@login_required
@user_passes_test(is_admin)
def restore_backup(request, backup_id):
    """
    Restore từ backup
    """
    if request.method == 'POST':
        backup = get_object_or_404(BackupHistory, id=backup_id)
        
        # Kiểm tra xác nhận
        confirm = request.POST.get('confirm_restore')
        if confirm != 'RESTORE':
            messages.error(request, 'Vui lòng nhập "RESTORE" để xác nhận!')
            return redirect('backup_settings')
        
        try:
            backup_service = BackupService()
            backup_service.restore_backup(backup, user=request.user)
            
            messages.success(
                request,
                f'Restore backup thành công từ file: {backup.backup_name}. '
                f'Vui lòng khởi động lại ứng dụng để áp dụng thay đổi.'
            )
        except Exception as e:
            logger.error(f"Lỗi khi restore backup: {str(e)}")
            messages.error(request, f'Lỗi khi restore backup: {str(e)}')
    
    return redirect('backup_settings')


@login_required
@user_passes_test(is_admin)
def delete_backup(request, backup_id):
    """
    Xóa backup
    """
    if request.method == 'POST':
        backup = get_object_or_404(BackupHistory, id=backup_id)
        
        try:
            backup_service = BackupService()
            backup_service.delete_backup(backup)
            
            messages.success(request, f'Đã xóa backup: {backup.backup_name}')
        except Exception as e:
            logger.error(f"Lỗi khi xóa backup: {str(e)}")
            messages.error(request, f'Lỗi khi xóa backup: {str(e)}')
    
    return redirect('backup_settings')
