from django.db import models
from django.core.exceptions import ValidationError


class EmailConfiguration(models.Model):
    """
    Model để lưu trữ cấu hình email SMTP cho hệ thống.
    Chỉ cho phép tạo một cấu hình duy nhất.
    """
    AUTH_CHOICES = [
        ('none', 'Không cần xác thực'),
        ('normal', 'Username và Password'),
    ]
    
    smtp_host = models.CharField(max_length=255, verbose_name='SMTP Host')
    smtp_port = models.PositiveIntegerField(verbose_name='SMTP Port')
    auth_method = models.CharField(
        max_length=10, 
        choices=AUTH_CHOICES,
        default='normal',
        verbose_name='SMTP Outgoing Authentication'
    )
    smtp_username = models.CharField(max_length=255, verbose_name='SMTP Username', blank=True, null=True)
    smtp_password = models.CharField(max_length=255, verbose_name='SMTP Password', blank=True, null=True)
    from_email = models.EmailField(verbose_name='Email người gửi')
    from_name = models.CharField(max_length=255, verbose_name='Tên người gửi', default='Hệ thống quản lý kho')
    use_tls = models.BooleanField(default=True, verbose_name='Sử dụng TLS')
    use_ssl = models.BooleanField(default=False, verbose_name='Sử dụng SSL')
    smtp_conn_timeout = models.PositiveIntegerField(default=60000, verbose_name='SMTP - Communication Timeout')
    smtp_timeout = models.PositiveIntegerField(default=60000, verbose_name='SMTP - Timeout')
    
    # Thông tin bổ sung
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_email_configs',
        verbose_name='Người tạo'
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_email_configs',
        verbose_name='Người cập nhật'
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    last_test_success = models.BooleanField(null=True, blank=True, verbose_name='Test cuối thành công')
    last_test_date = models.DateTimeField(null=True, blank=True, verbose_name='Ngày test cuối')
    
    class Meta:
        verbose_name = 'Cấu hình Email'
        verbose_name_plural = 'Cấu hình Email'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.smtp_username} ({self.smtp_host}:{self.smtp_port})"
    
    def save(self, *args, **kwargs):
        """Kiểm tra xem đã tồn tại cấu hình khác chưa"""
        if not self.pk and EmailConfiguration.objects.exists():
            # Nếu đang tạo mới và đã có cấu hình khác
            # Đảm bảo chỉ có một cấu hình được lưu
            # Bỏ qua nếu đã có một cấu hình rồi
            # Thay vào đó hãy cập nhật cấu hình hiện tại
            raise ValidationError("Chỉ được phép có một cấu hình email. Hãy cập nhật cấu hình hiện tại.")
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validate: TLS và SSL không thể cùng được bật"""
        if self.use_tls and self.use_ssl:
            raise ValidationError("Không thể sử dụng cả TLS và SSL cùng lúc")