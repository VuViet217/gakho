from django.contrib import admin
from .models import EmailConfiguration

@admin.register(EmailConfiguration)
class EmailConfigurationAdmin(admin.ModelAdmin):
    list_display = ('smtp_host', 'smtp_port', 'smtp_username', 'from_email', 'is_active', 'last_test_success', 'last_test_date')
    list_filter = ('is_active', 'use_tls', 'use_ssl', 'last_test_success')
    search_fields = ('smtp_host', 'smtp_username', 'from_email')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'last_test_date', 'last_test_success')
    fieldsets = (
        ('Cấu hình SMTP', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'from_email')
        }),
        ('Tùy chọn', {
            'fields': ('use_tls', 'use_ssl', 'is_active')
        }),
        ('Trạng thái', {
            'fields': ('last_test_success', 'last_test_date')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
