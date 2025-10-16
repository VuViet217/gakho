from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Supplier, PurchaseOrder


class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'code', 'name', 'address', 'contact_name', 'contact_phone', 'contact_email')


class PurchaseOrderResource(resources.ModelResource):
    class Meta:
        model = PurchaseOrder
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'po_number', 'supplier', 'order_date', 'status', 'description')


@admin.register(Supplier)
class SupplierAdmin(ImportExportModelAdmin):
    resource_class = SupplierResource
    list_display = ('code', 'name', 'contact_name', 'contact_phone', 'contact_email')
    list_filter = ('created_at',)
    search_fields = ('code', 'name', 'contact_name', 'contact_phone', 'contact_email')
    ordering = ('code', 'name')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(ImportExportModelAdmin):
    resource_class = PurchaseOrderResource
    list_display = ('po_number', 'supplier', 'order_date', 'status')
    list_filter = ('status', 'order_date', 'supplier')
    search_fields = ('po_number', 'supplier__name', 'description')
    ordering = ('-order_date', 'po_number')
