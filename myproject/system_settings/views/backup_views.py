"""
Backup views for system settings
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import FileResponse, Http404
import logging

from ..models import BackupConfiguration, BackupHistory
from ..backup_service import BackupService

logger = logging.getLogger(__name__)


# Hàm kiểm tra quyền admin
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role in ['sm', 'admin'])


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
