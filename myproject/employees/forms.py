from django import forms
from .models import Department, Employee
from django.core.exceptions import ValidationError


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['code', 'name', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã bộ phận'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên bộ phận'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập mô tả', 'rows': 3}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            # Chuyển mã thành chữ in hoa và loại bỏ khoảng trắng
            return code.strip().upper()
        return code


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'last_name', 'first_name', 'department'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã nhân viên'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên'}),
            'department': forms.Select(attrs={'class': 'form-control select2'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'id_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số CMND/CCCD'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ', 'rows': 2}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập chức vụ'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if employee_id:
            # Chuyển mã thành chữ in hoa và loại bỏ khoảng trắng
            return employee_id.strip().upper()
        return employee_id


class ImportForm(forms.Form):
    import_file = forms.FileField(
        label='Chọn file Excel/CSV',
        help_text='Định dạng hỗ trợ: .xlsx, .xls, .csv'
    )
    
    def clean_import_file(self):
        import_file = self.cleaned_data.get('import_file')
        if import_file:
            name = import_file.name.lower()
            if not (name.endswith('.xlsx') or name.endswith('.xls') or name.endswith('.csv')):
                raise ValidationError("Chỉ hỗ trợ file Excel (.xlsx, .xls) hoặc CSV (.csv)")
        return import_file