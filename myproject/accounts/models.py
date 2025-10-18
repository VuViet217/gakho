from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = (
        ('sm', 'SM (Senior Manager)'),
        ('admin', 'Quản trị viên'),
        ('manager', 'Quản lý'),
        ('staff', 'Nhân viên'),
        ('viewer', 'Chỉ xem'),
    )
    
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='staff',
        verbose_name='Vai trò'
    )
    department = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='Bộ phận'
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='Số điện thoại'
    )
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        blank=True, 
        null=True,
        verbose_name='Ảnh đại diện'
    )
    
    # Thêm trường người quản lý
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name='Người quản lý'
    )
    
    # Thông tin liên hệ người quản lý
    manager_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Họ tên người quản lý'
    )
    manager_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email người quản lý'
    )
    
    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'
        ordering = ['username']

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.get_full_name()} - {self.email} ({self.username})"
        return f"{self.username} - {self.email}"
    
    def clean(self):
        """Validate: SM không được có người quản lý"""
        super().clean()
        if self.role == 'sm' and self.manager:
            raise ValidationError({
                'manager': 'SM (Senior Manager) không được có người quản lý.'
            })
        
        # Các vai trò khác phải có người quản lý
        if self.role != 'sm' and not self.manager and self.pk:
            # Chỉ check khi update, không check khi tạo mới
            pass
    
    def save(self, *args, **kwargs):
        # Tự động xóa manager nếu là SM
        if self.role == 'sm':
            self.manager = None
            self.manager_name = None
            self.manager_email = None
        
        # Tự động cập nhật manager_name và manager_email từ manager
        if self.manager:
            self.manager_name = self.manager.get_full_name() or self.manager.username
            self.manager_email = self.manager.email
        
        # Nếu không có manager nhưng có manager_email, giữ nguyên giá trị manager_email
        # Điều này cho phép người dùng chỉ nhập email manager mà không cần chọn từ danh sách
        
        super().save(*args, **kwargs)
    
    @property
    def is_sm(self):
        """Kiểm tra có phải SM không"""
        return self.role == 'sm'
    
    @property
    def can_approve(self):
        """Kiểm tra có quyền phê duyệt không"""
        return self.role in ['sm', 'admin', 'manager']
