from django.db import models
from django.utils import timezone
from inventory.models import Product


class MonthlyInventorySnapshot(models.Model):
    """Snapshot tồn kho cuối mỗi tháng để so sánh"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='monthly_snapshots')
    year = models.IntegerField()
    month = models.IntegerField()  # 1-12
    
    # Số liệu đầu tháng
    opening_stock = models.IntegerField(default=0, verbose_name='Tồn đầu tháng')
    
    # Số liệu cuối tháng (tự động cập nhật)
    closing_stock = models.IntegerField(default=0, verbose_name='Tồn cuối tháng')
    
    # Biến động trong tháng
    total_received = models.IntegerField(default=0, verbose_name='Tổng nhập')
    total_issued = models.IntegerField(default=0, verbose_name='Tổng xuất')
    
    # Metadata
    is_closed = models.BooleanField(default=False, verbose_name='Đã chốt')
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày chốt')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reports_monthly_inventory_snapshot'
        verbose_name = 'Snapshot tồn kho tháng'
        verbose_name_plural = 'Snapshot tồn kho tháng'
        unique_together = ['product', 'year', 'month']
        ordering = ['-year', '-month', 'product__name']
        indexes = [
            models.Index(fields=['year', 'month']),
            models.Index(fields=['product', 'year', 'month']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.month}/{self.year}"
    
    def close_month(self):
        """Chốt tháng - lưu số liệu cuối tháng"""
        if not self.is_closed:
            self.closing_stock = self.product.current_quantity
            self.is_closed = True
            self.closed_at = timezone.now()
            self.save()
    
    @property
    def stock_change(self):
        """Chênh lệch tồn kho"""
        return self.closing_stock - self.opening_stock
    
    @property
    def stock_change_percentage(self):
        """Phần trăm thay đổi"""
        if self.opening_stock == 0:
            return 0
        return round((self.stock_change / self.opening_stock) * 100, 2)


class InventoryAudit(models.Model):
    """Kiểm kê kho"""
    STATUS_CHOICES = [
        ('draft', 'Bản nháp'),
        ('in_progress', 'Đang kiểm kê'),
        ('completed', 'Hoàn thành'),
    ]
    
    audit_code = models.CharField(max_length=50, unique=True, verbose_name='Mã kiểm kê')
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    audit_date = models.DateField(verbose_name='Ngày kiểm kê')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    notes = models.TextField(blank=True, verbose_name='Ghi chú')
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='audits_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'reports_inventory_audit'
        verbose_name = 'Phiếu kiểm kê'
        verbose_name_plural = 'Phiếu kiểm kê'
        ordering = ['-audit_date', '-created_at']
    
    def __str__(self):
        return f"{self.audit_code} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.audit_code:
            # Tự động tạo mã kiểm kê: AUD-YYYYMM-XXX
            from django.db.models import Max
            today = timezone.now()
            prefix = f"AUD-{today.strftime('%Y%m')}"
            
            last_audit = InventoryAudit.objects.filter(
                audit_code__startswith=prefix
            ).aggregate(Max('audit_code'))['audit_code__max']
            
            if last_audit:
                last_number = int(last_audit.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.audit_code = f"{prefix}-{new_number:03d}"
        
        super().save(*args, **kwargs)


class InventoryAuditItem(models.Model):
    """Chi tiết kiểm kê từng sản phẩm"""
    audit = models.ForeignKey(InventoryAudit, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Số liệu hệ thống
    system_quantity = models.IntegerField(verbose_name='Số lượng hệ thống')
    
    # Số liệu kiểm kê thực tế (điền tay)
    actual_quantity = models.IntegerField(null=True, blank=True, verbose_name='Số lượng thực tế')
    
    # Ghi chú về chênh lệch
    notes = models.TextField(blank=True, verbose_name='Ghi chú')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reports_inventory_audit_item'
        verbose_name = 'Chi tiết kiểm kê'
        verbose_name_plural = 'Chi tiết kiểm kê'
        unique_together = ['audit', 'product']
    
    def __str__(self):
        return f"{self.audit.audit_code} - {self.product.name}"
    
    @property
    def difference(self):
        """Chênh lệch giữa thực tế và hệ thống"""
        if self.actual_quantity is None:
            return None
        return self.actual_quantity - self.system_quantity
    
    @property
    def difference_percentage(self):
        """Phần trăm chênh lệch"""
        if self.actual_quantity is None or self.system_quantity == 0:
            return None
        return round((self.difference / self.system_quantity) * 100, 2)
