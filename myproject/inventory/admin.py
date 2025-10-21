from django.contrib import admin
from .models import Category, Unit, Warehouse, WarehouseRow, WarehouseColumn, Product, StockTransaction

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Warehouse)
admin.site.register(WarehouseRow)
admin.site.register(WarehouseColumn)
admin.site.register(Product)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_code', 'product', 'transaction_type', 'quantity', 'transaction_date', 'created_by']
    list_filter = ['transaction_type', 'transaction_date']
    search_fields = ['transaction_code', 'product__name', 'reference_code']
    readonly_fields = ['transaction_code', 'transaction_date']
