from django.contrib import admin
from .models import MonthlyInventorySnapshot, InventoryAudit, InventoryAuditItem


@admin.register(MonthlyInventorySnapshot)
class MonthlyInventorySnapshotAdmin(admin.ModelAdmin):
    list_display = ['product', 'year', 'month', 'opening_stock', 'closing_stock', 'stock_change', 'is_closed']
    list_filter = ['year', 'month', 'is_closed']
    search_fields = ['product__name', 'product__product_code']
    readonly_fields = ['created_at', 'updated_at', 'closed_at']


class InventoryAuditItemInline(admin.TabularInline):
    model = InventoryAuditItem
    extra = 0
    fields = ['product', 'system_quantity', 'actual_quantity', 'notes']
    readonly_fields = ['system_quantity']


@admin.register(InventoryAudit)
class InventoryAuditAdmin(admin.ModelAdmin):
    list_display = ['audit_code', 'title', 'audit_date', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'audit_date']
    search_fields = ['audit_code', 'title']
    readonly_fields = ['audit_code', 'created_at', 'updated_at', 'completed_at']
    inlines = [InventoryAuditItemInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('audit_code', 'title', 'audit_date', 'status')
        }),
        ('Chi tiết', {
            'fields': ('notes', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
