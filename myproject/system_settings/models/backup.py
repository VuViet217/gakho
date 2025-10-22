from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class BackupConfiguration(models.Model):
    """Cấu hình backup tự động"""
    
    BACKUP_FREQUENCY_CHOICES = [
        ('daily', _('Hàng ngày')),
        ('weekly', _('Hàng tuần')),
        ('monthly', _('Hàng tháng')),
        ('manual', _('Thủ công')),
    ]
    
    # Cấu hình backup
    backup_frequency = models.CharField(
        max_length=20,
        choices=BACKUP_FREQUENCY_CHOICES,
        default='manual',
        verbose_name=_('Tần suất backup')
    )
    backup_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_('Thời gian backup (cho tự động)')
    )
    include_database = models.BooleanField(
        default=True,
        verbose_name=_('Backup database')
    )
    include_media = models.BooleanField(
        default=True,
        verbose_name=_('Backup media files')
    )
    max_backups_keep = models.IntegerField(
        default=10,
        verbose_name=_('Số lượng backup giữ lại'),
        help_text=_('Số lượng backup tối đa được lưu trữ')
    )
    
    # Thông tin
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Kích hoạt backup tự động')
    )
    last_backup_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Lần backup cuối')
    )
    last_backup_success = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('Backup cuối thành công')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày tạo'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Ngày cập nhật'))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backup_configs_created',
        verbose_name=_('Người tạo')
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backup_configs_updated',
        verbose_name=_('Người cập nhật')
    )
    
    class Meta:
        verbose_name = _('Cấu hình Backup')
        verbose_name_plural = _('Cấu hình Backup')
        db_table = 'backup_configuration'
    
    def __str__(self):
        return f"Backup Config - {self.get_backup_frequency_display()}"


class BackupHistory(models.Model):
    """Lịch sử backup"""
    
    BACKUP_TYPE_CHOICES = [
        ('full', _('Toàn bộ')),
        ('database', _('Database only')),
        ('media', _('Media only')),
    ]
    
    BACKUP_STATUS_CHOICES = [
        ('pending', _('Đang xử lý')),
        ('success', _('Thành công')),
        ('failed', _('Thất bại')),
    ]
    
    # Thông tin backup
    backup_type = models.CharField(
        max_length=20,
        choices=BACKUP_TYPE_CHOICES,
        default='full',
        verbose_name=_('Loại backup')
    )
    backup_name = models.CharField(
        max_length=255,
        verbose_name=_('Tên file backup')
    )
    backup_file = models.FileField(
        upload_to='backups/',
        verbose_name=_('File backup'),
        null=True,
        blank=True
    )
    file_size = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Kích thước (bytes)')
    )
    
    # Trạng thái
    status = models.CharField(
        max_length=20,
        choices=BACKUP_STATUS_CHOICES,
        default='pending',
        verbose_name=_('Trạng thái')
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Thông báo lỗi')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày tạo'))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Người tạo')
    )
    is_auto = models.BooleanField(
        default=False,
        verbose_name=_('Backup tự động')
    )
    
    # Thông tin restore
    restored_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Ngày restore')
    )
    restored_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backups_restored',
        verbose_name=_('Người restore')
    )
    
    class Meta:
        verbose_name = _('Lịch sử Backup')
        verbose_name_plural = _('Lịch sử Backup')
        db_table = 'backup_history'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.backup_name} - {self.get_status_display()}"
    
    def get_file_size_display(self):
        """Hiển thị kích thước file dễ đọc"""
        if not self.file_size:
            return "N/A"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
