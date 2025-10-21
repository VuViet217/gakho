from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailTemplate(models.Model):
    """
    Model lưu trữ các mẫu email được sử dụng trong hệ thống.
    Mỗi mẫu có một mã định danh (code) riêng biệt và được sử dụng cho các trường hợp cụ thể.
    """
    TEMPLATE_TYPES = [
        ('request_created', 'Yêu cầu cấp phát mới'),
        ('pending_approval', 'Yêu cầu chờ phê duyệt'),
        ('request_approved', 'Yêu cầu đã được phê duyệt'),
        ('request_rejected', 'Yêu cầu bị từ chối'),
        ('warehouse_scheduled', 'Kho đã hẹn lịch cấp phát'),
        ('request_completed', 'Yêu cầu đã hoàn thành'),
        ('other', 'Mẫu khác'),
    ]
    
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Mã mẫu'),
        help_text=_('Mã định danh duy nhất cho mẫu email, ví dụ: request_created')
    )
    
    type = models.CharField(
        max_length=30,
        choices=TEMPLATE_TYPES,
        default='other',
        verbose_name=_('Loại mẫu')
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Tên mẫu'),
        help_text=_('Tên hiển thị của mẫu email')
    )
    
    subject = models.CharField(
        max_length=255,
        verbose_name=_('Tiêu đề email'),
        help_text=_('Tiêu đề của email sẽ được gửi')
    )
    
    content = models.TextField(
        verbose_name=_('Nội dung email'),
        help_text=_('Nội dung của email. Có thể sử dụng các biến với cú pháp {{variable_name}}')
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Mô tả'),
        help_text=_('Mô tả về mẫu email và trường hợp sử dụng')
    )
    
    is_html = models.BooleanField(
        default=True,
        verbose_name=_('Định dạng HTML'),
        help_text=_('Email được gửi ở định dạng HTML thay vì text thuần túy')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Kích hoạt'),
        help_text=_('Mẫu email này có đang được sử dụng hay không')
    )
    
    variables = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Danh sách biến'),
        help_text=_('Danh sách các biến có thể sử dụng trong mẫu này ở định dạng JSON')
    )

    # Danh sách email mặc định (dấu phẩy phân tách). Người nhận sẽ được gửi thông báo tự động nếu mẫu này được sử dụng.
    default_recipients = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Người nhận mặc định'),
        help_text=_('Danh sách địa chỉ email, phân tách bằng dấu phẩy. Ví dụ: a@x.com,b@y.com')
    )

    # Danh sách CC mặc định (dấu phẩy phân tách)
    default_cc = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('CC mặc định'),
        help_text=_('Danh sách địa chỉ email CC, phân tách bằng dấu phẩy')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Mẫu email')
        verbose_name_plural = _('Mẫu email')
        ordering = ['type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"