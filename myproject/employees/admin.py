from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Department, Employee


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        import_id_fields = ['code']
        fields = ('code', 'name', 'description')
        export_order = fields


class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ['code', 'name', 'description', 'created_at', 'updated_at']
    search_fields = ['code', 'name', 'description']
    list_filter = ['created_at', 'updated_at']


class EmployeeResource(resources.ModelResource):
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'code')
    )

    class Meta:
        model = Employee
        import_id_fields = ['employee_id']
        fields = (
            'employee_id', 'last_name', 'first_name', 'full_name', 
            'department', 'date_of_birth', 'gender', 'id_card', 
            'phone_number', 'email', 'address', 'position', 
            'join_date', 'status'
        )
        export_order = fields

    def before_import_row(self, row, **kwargs):
        # Chuyển đổi giới tính từ tên đầy đủ thành mã
        gender_map = {'Nam': 'M', 'Nữ': 'F', 'Khác': 'O'}
        if 'gender' in row:
            row['gender'] = gender_map.get(row['gender'], row['gender'])
        
        # Chuyển đổi trạng thái từ chuỗi sang boolean
        if 'status' in row:
            status = row['status'].lower() if isinstance(row['status'], str) else row['status']
            if status in ['1', 'true', 'yes', 'có', 'y', 'đang làm việc']:
                row['status'] = True
            else:
                row['status'] = False


class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ['employee_id', 'full_name', 'department', 'position', 'phone_number', 'email', 'join_date', 'status']
    search_fields = ['employee_id', 'first_name', 'last_name', 'full_name', 'phone_number', 'email', 'id_card']
    list_filter = ['department', 'gender', 'join_date', 'status', 'created_at', 'updated_at']
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('employee_id', 'last_name', 'first_name', 'department', 'position')
        }),
        ('Thông tin cá nhân', {
            'fields': ('date_of_birth', 'gender', 'id_card', 'phone_number', 'email', 'address')
        }),
        ('Thông tin công việc', {
            'fields': ('join_date', 'status')
        }),
    )


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
