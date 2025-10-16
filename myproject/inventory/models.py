from django.db import models
from django.utils.translation import gettext_lazy as _
from suppliers.models import PurchaseOrder
from django.urls import reverse

class Category(models.Model):
    """Danh mục sản phẩm trong kho"""
    name = models.CharField(_("Tên danh mục"), max_length=100)
    description = models.TextField(_("Mô tả"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ngày tạo"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Ngày cập nhật"), auto_now=True)

    class Meta:
        verbose_name = _("Danh mục")
        verbose_name_plural = _("Danh mục")
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

class Unit(models.Model):
    """Đơn vị tính cho sản phẩm"""
    name = models.CharField(_("Tên đơn vị"), max_length=50)
    abbreviation = models.CharField(_("Viết tắt"), max_length=10)
    
    class Meta:
        verbose_name = _("Đơn vị tính")
        verbose_name_plural = _("Đơn vị tính")
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("unit_detail", kwargs={"pk": self.pk})

class Warehouse(models.Model):
    """Kho lưu trữ sản phẩm"""
    name = models.CharField(_("Tên kho"), max_length=100)
    location = models.CharField(_("Địa điểm"), max_length=255, blank=True, null=True)
    description = models.TextField(_("Mô tả"), blank=True, null=True)
    active = models.BooleanField(_("Còn hoạt động"), default=True)
    created_at = models.DateTimeField(_("Ngày tạo"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Ngày cập nhật"), auto_now=True)

    class Meta:
        verbose_name = _("Kho")
        verbose_name_plural = _("Kho")
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("warehouse_detail", kwargs={"pk": self.pk})

class WarehouseRow(models.Model):
    """Dãy trong kho"""
    warehouse = models.ForeignKey(
        Warehouse, 
        on_delete=models.CASCADE, 
        related_name="rows", 
        verbose_name=_("Kho")
    )
    row_code = models.CharField(_("Mã dãy"), max_length=50)
    description = models.TextField(_("Mô tả"), blank=True, null=True)
    
    class Meta:
        verbose_name = _("Dãy kho")
        verbose_name_plural = _("Dãy kho")
        ordering = ["row_code"]
        unique_together = [['warehouse', 'row_code']]

    def __str__(self):
        return f"{self.warehouse.name} - Dãy {self.row_code}"
    
    def get_absolute_url(self):
        return reverse("warehouse_row_detail", kwargs={"pk": self.pk})

class WarehouseColumn(models.Model):
    """Cột trong dãy kho"""
    row = models.ForeignKey(
        WarehouseRow, 
        on_delete=models.CASCADE, 
        related_name="columns", 
        verbose_name=_("Dãy kho")
    )
    column_code = models.CharField(_("Mã cột"), max_length=50)
    description = models.TextField(_("Mô tả"), blank=True, null=True)
    
    class Meta:
        verbose_name = _("Cột kho")
        verbose_name_plural = _("Cột kho")
        ordering = ["column_code"]
        unique_together = [['row', 'column_code']]

    def __str__(self):
        return f"{self.row} - Cột {self.column_code}"
    
    def get_absolute_url(self):
        return reverse("warehouse_column_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    """Sản phẩm trong kho"""
    product_code = models.CharField(_("Mã sản phẩm"), max_length=50, unique=True)
    name = models.CharField(_("Tên sản phẩm"), max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        related_name="products", 
        verbose_name=_("Danh mục"),
        null=True
    )
    unit = models.ForeignKey(
        Unit, 
        on_delete=models.SET_NULL, 
        related_name="products", 
        verbose_name=_("Đơn vị tính"),
        null=True
    )
    purchase_order = models.ForeignKey(
        PurchaseOrder, 
        on_delete=models.SET_NULL, 
        related_name="products", 
        verbose_name=_("Đơn đặt hàng"),
        null=True
    )
    column = models.ForeignKey(
        WarehouseColumn, 
        on_delete=models.SET_NULL, 
        related_name="products", 
        verbose_name=_("Vị trí trong kho"),
        null=True
    )
    current_quantity = models.PositiveIntegerField(_("Số lượng hiện tại"), default=0)
    minimum_quantity = models.PositiveIntegerField(_("Số lượng tối thiểu"), default=0)
    description = models.TextField(_("Mô tả"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ngày tạo"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Ngày cập nhật"), auto_now=True)

    class Meta:
        verbose_name = _("Sản phẩm")
        verbose_name_plural = _("Sản phẩm")
        ordering = ["product_code"]

    def __str__(self):
        return f"{self.product_code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    
    @property
    def is_low_stock(self):
        """Kiểm tra xem sản phẩm có đang ở mức tồn kho thấp hay không"""
        return self.current_quantity <= self.minimum_quantity
    
    @property
    def warehouse_location(self):
        """Trả về vị trí đầy đủ của sản phẩm trong kho"""
        if self.column:
            return f"{self.column}"
        return "Chưa xác định"
