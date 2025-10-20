from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

from employees.models import Employee
from inventory.models import Product

class InventoryRequest(models.Model):
    """
    Model lưu trữ thông tin yêu cầu cấp phát vật tư
    """
    # Trạng thái yêu cầu
    STATUS_DRAFT = 'draft'            # Bản nháp
    STATUS_PENDING = 'pending'        # Chờ phê duyệt
    STATUS_APPROVED = 'approved'      # Đã phê duyệt
    STATUS_REJECTED = 'rejected'      # Bị từ chối
    STATUS_SCHEDULED = 'scheduled'    # Đã lên lịch cấp phát
    STATUS_COMPLETED = 'completed'    # Đã hoàn thành cấp phát
    STATUS_CANCELED = 'canceled'      # Đã hủy
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Bản nháp')),
        (STATUS_PENDING, _('Chờ phê duyệt')),
        (STATUS_APPROVED, _('Đã phê duyệt')),
        (STATUS_REJECTED, _('Bị từ chối')),
        (STATUS_SCHEDULED, _('Đã lên lịch')),
        (STATUS_COMPLETED, _('Đã hoàn thành')),
        (STATUS_CANCELED, _('Đã hủy')),
    ]
    
    # Thông tin cơ bản
    request_code = models.CharField(_('Mã yêu cầu'), max_length=20, unique=True)
    title = models.CharField(_('Tiêu đề yêu cầu'), max_length=255)
    description = models.TextField(_('Mô tả'), blank=True, null=True)
    status = models.CharField(_('Trạng thái'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    # Thông tin thời gian
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ngày cập nhật'), auto_now=True)
    expected_date = models.DateField(_('Ngày mong muốn nhận'), null=True, blank=True)
    scheduled_date = models.DateTimeField(_('Ngày giờ dự kiến cấp phát'), null=True, blank=True)
    completed_date = models.DateTimeField(_('Ngày hoàn thành'), null=True, blank=True)
    
    # Người liên quan
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_requests',
        verbose_name=_('Người tạo yêu cầu')
    )
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_requests',
        verbose_name=_('Người phê duyệt')
    )
    warehouse_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='warehouse_managed_requests',
        verbose_name=_('Quản lý kho phụ trách')
    )
    
    # Thông tin phê duyệt
    approval_date = models.DateTimeField(_('Ngày phê duyệt'), null=True, blank=True)
    approval_note = models.TextField(_('Ghi chú phê duyệt'), blank=True, null=True)
    rejection_reason = models.TextField(_('Lý do từ chối'), blank=True, null=True)
    
    # Ghi chú bổ sung
    notes = models.TextField(_('Ghi chú'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Yêu cầu cấp phát')
        verbose_name_plural = _('Yêu cầu cấp phát')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.request_code} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('inventory_request_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Tự động tạo mã yêu cầu nếu chưa có
        if not self.request_code:
            last_request = InventoryRequest.objects.order_by('-id').first()
            last_id = last_request.id if last_request else 0
            self.request_code = f'YC{timezone.now().strftime("%y%m")}{last_id + 1:04d}'
        super().save(*args, **kwargs)
    
    def mark_as_pending(self):
        """Đánh dấu yêu cầu là đang chờ phê duyệt"""
        self.status = self.STATUS_PENDING
        self.save()
    
    def approve(self, approver, note=None):
        """Phê duyệt yêu cầu"""
        self.status = self.STATUS_APPROVED
        self.approver = approver
        self.approval_date = timezone.now()
        self.approval_note = note
        self.save()
    
    def reject(self, approver, reason=None):
        """Từ chối yêu cầu"""
        self.status = self.STATUS_REJECTED
        self.approver = approver
        self.approval_date = timezone.now()
        self.rejection_reason = reason
        self.save()
    
    def schedule(self, warehouse_manager, scheduled_date):
        """Lên lịch cấp phát"""
        self.status = self.STATUS_SCHEDULED
        self.warehouse_manager = warehouse_manager
        self.scheduled_date = scheduled_date
        self.save()
    
    def complete(self):
        """Đánh dấu yêu cầu đã hoàn thành"""
        self.status = self.STATUS_COMPLETED
        self.completed_date = timezone.now()
        self.save()
    
    def cancel(self):
        """Hủy yêu cầu"""
        self.status = self.STATUS_CANCELED
        self.save()
    
    @property
    def can_be_edited(self):
        """Kiểm tra xem yêu cầu có thể chỉnh sửa không"""
        return self.status in [self.STATUS_DRAFT, self.STATUS_PENDING]
    
    @property
    def can_be_deleted(self):
        """Kiểm tra xem yêu cầu có thể xóa không"""
        return self.status in [self.STATUS_DRAFT, self.STATUS_PENDING, self.STATUS_REJECTED]


class RequestEmployee(models.Model):
    """
    Liên kết giữa yêu cầu và nhân viên cần cấp phát
    """
    request = models.ForeignKey(
        InventoryRequest, 
        on_delete=models.CASCADE,
        related_name='request_employees',
        verbose_name=_('Yêu cầu')
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='inventory_requests',
        verbose_name=_('Nhân viên')
    )
    notes = models.TextField(_('Ghi chú'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Nhân viên cần cấp phát')
        verbose_name_plural = _('Nhân viên cần cấp phát')
        unique_together = ('request', 'employee')
    
    def __str__(self):
        return f"{self.request.request_code} - {self.employee}"


class RequestItem(models.Model):
    """
    Sản phẩm trong yêu cầu cấp phát
    """
    request = models.ForeignKey(
        InventoryRequest,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Yêu cầu')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='request_items',
        verbose_name=_('Sản phẩm')
    )
    requested_quantity = models.PositiveIntegerField(_('Số lượng yêu cầu'))
    approved_quantity = models.PositiveIntegerField(_('Số lượng phê duyệt'), null=True, blank=True)
    issued_quantity = models.PositiveIntegerField(_('Số lượng đã cấp phát'), default=0)
    notes = models.TextField(_('Ghi chú'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Sản phẩm yêu cầu')
        verbose_name_plural = _('Sản phẩm yêu cầu')
        unique_together = ('request', 'product')
    
    def __str__(self):
        return f"{self.product.name} - SL: {self.requested_quantity}"
    
    def save(self, *args, **kwargs):
        # Nếu không có số lượng phê duyệt, mặc định là số lượng yêu cầu
        if self.approved_quantity is None:
            self.approved_quantity = self.requested_quantity
        super().save(*args, **kwargs)


class EmployeeProductRequest(models.Model):
    """
    Liên kết giữa nhân viên, sản phẩm và yêu cầu cấp phát
    Mô hình này cho phép mỗi nhân viên có thể chọn các sản phẩm khác nhau trong cùng một yêu cầu
    """
    request = models.ForeignKey(
        InventoryRequest,
        on_delete=models.CASCADE,
        related_name='employee_products',
        verbose_name=_('Yêu cầu')
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='product_requests',
        verbose_name=_('Nhân viên')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='employee_requests',
        verbose_name=_('Sản phẩm')
    )
    quantity = models.PositiveIntegerField(_('Số lượng yêu cầu'))
    approved_quantity = models.PositiveIntegerField(_('Số lượng phê duyệt'), null=True, blank=True)
    issued_quantity = models.PositiveIntegerField(_('Số lượng đã cấp phát'), default=0)
    notes = models.TextField(_('Ghi chú'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Phân bổ sản phẩm cho nhân viên')
        verbose_name_plural = _('Phân bổ sản phẩm cho nhân viên')
        unique_together = ('request', 'employee', 'product')
    
    def __str__(self):
        return f"{self.employee} - {self.product.name} - SL: {self.quantity}"
    
    def save(self, *args, **kwargs):
        # Nếu không có số lượng phê duyệt, mặc định là số lượng yêu cầu
        if self.approved_quantity is None:
            self.approved_quantity = self.quantity
        super().save(*args, **kwargs)
