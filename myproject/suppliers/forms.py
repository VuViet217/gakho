from django import forms
from .models import Supplier, PurchaseOrder
from django.core.exceptions import ValidationError

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['code', 'name', 'address', 'contact_name', 'contact_phone', 'contact_email']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã nhà cung cấp'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên nhà cung cấp'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ', 'rows': 3}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên người liên hệ'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            # Chuyển mã thành chữ in hoa và loại bỏ khoảng trắng
            return code.strip().upper()
        return code


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'supplier', 'order_date', 'status', 'description', 'po_image']
        widgets = {
            'po_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã PO'}),
            'supplier': forms.Select(attrs={'class': 'form-control select2'}),
            'order_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập mô tả', 'rows': 3}),
            'po_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_po_number(self):
        po_number = self.cleaned_data.get('po_number')
        if po_number:
            # Chuyển mã thành chữ in hoa và loại bỏ khoảng trắng
            return po_number.strip().upper()
        return po_number