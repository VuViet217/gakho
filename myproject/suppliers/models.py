from django.db import models
from django.utils import timezone

class Supplier(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã nhà cung cấp")
    name = models.CharField(max_length=200, verbose_name="Tên nhà cung cấp")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    contact_name = models.CharField(max_length=100, verbose_name="Tên người liên hệ")
    contact_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"
        ordering = ['code', 'name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
        ('completed', 'Hoàn thành'),
    )
    
    po_number = models.CharField(max_length=50, unique=True, verbose_name="Mã PO")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="purchase_orders", verbose_name="Nhà cung cấp")
    order_date = models.DateField(default=timezone.now, verbose_name="Ngày đặt hàng")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    po_image = models.ImageField(upload_to='purchase_orders/', blank=True, null=True, verbose_name="Hình ảnh PO")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Đơn đặt hàng"
        verbose_name_plural = "Đơn đặt hàng"
        ordering = ['-order_date', 'po_number']
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier.name}"
        
    @property
    def total_amount(self):
        """Tính tổng giá trị của đơn đặt hàng"""
        return sum(item.total_price for item in self.items.all())
        
    @property
    def total_quantity(self):
        """Tính tổng số lượng sản phẩm trong đơn đặt hàng"""
        return sum(item.quantity for item in self.items.all())
        
    @property
    def product_count(self):
        """Trả về số lượng sản phẩm khác nhau trong đơn đặt hàng"""
        return self.items.count()
        
    def get_status_display_class(self):
        """Trả về lớp CSS cho trạng thái đơn hàng"""
        status_classes = {
            'pending': 'warning',
            'approved': 'info',
            'rejected': 'danger',
            'completed': 'success',
        }
        return status_classes.get(self.status, 'secondary')

class PurchaseOrderItem(models.Model):
    """
    Model trung gian để thiết lập mối quan hệ nhiều-nhiều giữa PurchaseOrder và Product
    với các thông tin bổ sung như số lượng, đơn giá...
    """
    purchase_order = models.ForeignKey(
        PurchaseOrder, 
        on_delete=models.CASCADE, 
        related_name="items", 
        verbose_name="Đơn đặt hàng"
    )
    # product sẽ được import động để tránh circular import
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE,
        related_name='purchase_items',
        verbose_name="Sản phẩm"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng") 
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Đơn giá")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"
        ordering = ['purchase_order', 'product']
        
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.name} ({self.quantity})"
        
    @property
    def total_price(self):
        """Tính tổng giá trị của mục đơn hàng"""
        return self.quantity * self.unit_price
