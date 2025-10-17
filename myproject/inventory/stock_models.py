from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from suppliers.models import PurchaseOrder, PurchaseOrderItem
from inventory.models import Product


class StockReceipt(models.Model):
    """Model lưu thông tin phiếu nhập kho"""
    receipt_number = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu nhập")
    purchase_order = models.ForeignKey(
        PurchaseOrder, 
        on_delete=models.CASCADE,
        related_name='stock_receipts',
        verbose_name="Đơn đặt hàng"
    )
    receipt_date = models.DateField(default=timezone.now, verbose_name="Ngày nhập kho")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name="created_receipts",
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Phiếu nhập kho"
        verbose_name_plural = "Phiếu nhập kho"
        ordering = ['-receipt_date', 'receipt_number']
    
    def __str__(self):
        return f"{self.receipt_number} - {self.purchase_order.po_number}"
    
    def generate_receipt_number(self):
        """Tạo mã phiếu nhập theo quy tắc NK-YYYYMMDD-XXX"""
        today = timezone.now().date()
        date_string = today.strftime('%Y%m%d')
        
        try:
            # Lấy số phiếu nhập trong ngày
            today_receipts = StockReceipt.objects.filter(
                receipt_date=today
            ).count()
            print(f"Số phiếu nhập đã có trong ngày {today}: {today_receipts}")
            
            # Tạo mã phiếu nhập mới, đảm bảo số thứ tự ít nhất là 1
            next_number = today_receipts + 1
            receipt_number = f"NK-{date_string}-{next_number:03d}"
            print(f"Tạo mã phiếu nhập mới: {receipt_number}")
            return receipt_number
        except Exception as e:
            print(f"Lỗi khi tạo mã phiếu nhập: {str(e)}")
            # Tạo mã phiếu nhập mặc định với timestamp để đảm bảo tính duy nhất
            import time
            timestamp = int(time.time())
            receipt_number = f"NK-{date_string}-{timestamp}"
            print(f"Tạo mã phiếu nhập thay thế: {receipt_number}")
            return receipt_number
    
    def save(self, *args, **kwargs):
        print(f"=== DEBUG LƯU PHIẾU NHẬP KHO ===")
        print(f"Phiếu nhập đã có mã: {self.receipt_number is not None}")
        
        # Tạo mã phiếu nhập mới nếu chưa có
        if not self.receipt_number:
            try:
                self.receipt_number = self.generate_receipt_number()
                print(f"Đã tạo mã phiếu nhập mới: {self.receipt_number}")
            except Exception as e:
                print(f"Lỗi khi tạo mã phiếu nhập: {str(e)}")
                import traceback
                traceback.print_exc()
                raise e
        
        print(f"Thông tin phiếu nhập trước khi lưu:")
        print(f"- ID: {self.id}")
        print(f"- Mã phiếu nhập: {self.receipt_number}")
        print(f"- Đơn đặt hàng: {self.purchase_order}")
        print(f"- Ngày nhập: {self.receipt_date}")
        
        try:
            # Lưu phiếu nhập kho
            super().save(*args, **kwargs)
            print(f"Đã lưu phiếu nhập kho thành công: ID={self.id}, Mã={self.receipt_number}")
        except Exception as e:
            print(f"Lỗi khi lưu phiếu nhập kho: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
    
    @property
    def total_items(self):
        """Tổng số mặt hàng nhập kho"""
        return self.items.count()
    
    @property
    def total_quantity(self):
        """Tổng số lượng sản phẩm nhập kho"""
        return sum(item.quantity for item in self.items.all())


class StockReceiptItem(models.Model):
    """Model lưu chi tiết sản phẩm trong phiếu nhập kho (Đơn giản hóa)"""
    receipt = models.ForeignKey(
        StockReceipt, 
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Phiếu nhập kho"
    )
    purchase_order_item = models.ForeignKey(
        PurchaseOrderItem,
        on_delete=models.SET_NULL,
        related_name='receipt_items',
        verbose_name="Chi tiết đơn hàng",
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='receipt_items',
        verbose_name="Sản phẩm"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Số lượng nhập")
    notes = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Chi tiết phiếu nhập"
        verbose_name_plural = "Chi tiết phiếu nhập"
    
    def __str__(self):
        return f"{self.receipt.receipt_number} - {self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        # Lưu chi tiết phiếu nhập
        is_new = self.pk is None
        
        # Ghi log chi tiết
        print(f"=== DEBUG LƯU CHI TIẾT PHIẾU NHẬP ===")
        print(f"Chi tiết phiếu nhập là mới: {is_new}")
        print(f"Phiếu nhập gốc: {self.receipt.receipt_number if hasattr(self, 'receipt') and self.receipt else 'Không có'}")
        
        # Xác nhận là có product trước khi lưu
        if self.product:
            print(f"Sản phẩm: {self.product.name} (ID: {self.product.id})")
            
            try:
                # Đảm bảo purchase_order_item có thể là NULL
                # Chỉ định rõ ràng purchase_order_item là None nếu không có
                if not hasattr(self, 'purchase_order_item') or self.purchase_order_item is None:
                    print("Purchase order item là None, không cần quan tâm")
                    # Không cần thiết lập gì cả, trường này sẽ là NULL trong DB
                
                # Lưu chi tiết phiếu nhập - BYPASS phương thức save() của Django
                from django.db import connection
                cursor = connection.cursor()
                if is_new:
                    # INSERT một bản ghi mới trực tiếp vào DB
                    # Lấy purchase_order_item_id nếu có
                    po_item_id = self.purchase_order_item.id if hasattr(self, 'purchase_order_item') and self.purchase_order_item else None
                    
                    cursor.execute("""
                        INSERT INTO inventory_stockreceiptitem 
                        (product_id, receipt_id, quantity, notes, created_at, purchase_order_item_id)
                        VALUES (%s, %s, %s, %s, NOW(), %s)
                    """, [self.product.id, self.receipt.id, self.quantity, self.notes, po_item_id])
                    print(f"Đã thêm chi tiết phiếu nhập trực tiếp vào DB")
                    
                    # Cập nhật số lượng sản phẩm
                    self.update_product_quantity()
                    return  # Thoát khỏi phương thức
                else:
                    print(f"Đã lưu chi tiết phiếu nhập với ID: {self.pk}")
                    # Tiếp tục với super().save() cho trường hợp UPDATE
                    super().save(*args, **kwargs)
            except Exception as e:
                print(f"Lỗi khi lưu chi tiết phiếu nhập: {str(e)}")
                import traceback
                traceback.print_exc()
                raise e
        else:
            error_msg = "Không thể lưu StockReceiptItem mà không có sản phẩm"
            print(f"LỖI: {error_msg}")
            raise ValueError(error_msg)
    
    def update_product_quantity(self):
        """Cập nhật số lượng sản phẩm sau khi nhập kho"""
        if self.product:
            self.product.current_quantity += self.quantity
            self.product.save(update_fields=['current_quantity'])