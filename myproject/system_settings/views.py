from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
import logging

from .models import EmailConfiguration
from .forms import EmailConfigurationForm, TestEmailForm
from .email_service import send_test_email
from .smtp_checker import check_smtp_connection

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
