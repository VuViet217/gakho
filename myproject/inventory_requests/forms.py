from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory, BaseFormSet

from employees.models import Employee
from inventory.models import Product
from .models import InventoryRequest, RequestEmployee, RequestItem, EmployeeProductRequest

class InventoryRequestForm(forms.ModelForm):
    """
    Form cho việc tạo và chỉnh sửa yêu cầu cấp phát
    """
    expected_date = forms.DateField(
        label=_('Ngày mong muốn nhận'), 
        required=True,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        )
    )
    
    class Meta:
        model = InventoryRequest
        fields = ['title', 'description', 'expected_date', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RequestEmployeeForm(forms.ModelForm):
    """
    Form cho việc thêm nhân viên vào yêu cầu cấp phát
    """
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(status=True).order_by('full_name'),
        label=_('Nhân viên'),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    class Meta:
        model = RequestEmployee
        fields = ['employee', 'notes']
        widgets = {
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ghi chú (nếu có)'})
        }


class RequestItemForm(forms.ModelForm):
    """
    Form cho việc thêm sản phẩm vào yêu cầu cấp phát
    """
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(current_quantity__gt=0).order_by('name'),
        label=_('Sản phẩm'),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    class Meta:
        model = RequestItem
        fields = ['product', 'requested_quantity', 'notes']
        widgets = {
            'requested_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ghi chú (nếu có)'})
        }


# Formset để thêm nhiều nhân viên vào một yêu cầu
RequestEmployeeFormSet = inlineformset_factory(
    InventoryRequest, 
    RequestEmployee, 
    form=RequestEmployeeForm,
    extra=1, 
    can_delete=True
)

# Formset để thêm nhiều sản phẩm vào một yêu cầu
RequestItemFormSet = inlineformset_factory(
    InventoryRequest, 
    RequestItem, 
    form=RequestItemForm, 
    extra=1, 
    can_delete=True
)


class RequestApprovalForm(forms.Form):
    """
    Form cho việc phê duyệt yêu cầu cấp phát
    """
    APPROVAL_CHOICES = [
        ('approve', _('Phê duyệt')),
        ('reject', _('Từ chối')),
    ]
    
    decision = forms.ChoiceField(
        choices=APPROVAL_CHOICES, 
        label=_('Quyết định'),
        widget=forms.RadioSelect
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label=_('Ghi chú')
    )
    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label=_('Lý do từ chối')
    )
    
    def clean(self):
        cleaned_data = super().clean()
        decision = cleaned_data.get('decision')
        rejection_reason = cleaned_data.get('rejection_reason')
        
        if decision == 'reject' and not rejection_reason:
            self.add_error('rejection_reason', _('Vui lòng nhập lý do từ chối.'))
        
        return cleaned_data


class RequestScheduleForm(forms.Form):
    """
    Form cho việc lên lịch cấp phát
    """
    scheduled_date = forms.DateField(
        label=_('Ngày dự kiến cấp phát'),
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        required=True
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label=_('Ghi chú')
    )


class EmployeeProductRequestForm(forms.ModelForm):
    """
    Form cho việc phân bổ sản phẩm cho từng nhân viên
    """
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(status=True).order_by('full_name'),
        label=_('Nhân viên'),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(current_quantity__gt=0).order_by('name'),
        label=_('Sản phẩm'),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    class Meta:
        model = EmployeeProductRequest
        fields = ['employee', 'product', 'quantity', 'notes']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ghi chú (nếu có)'})
        }


from django.forms import BaseInlineFormSet

class BaseEmployeeProductFormSet(BaseInlineFormSet):
    """
    Base formset cho việc phân bổ sản phẩm cho nhân viên
    """
    def clean(self):
        """
        Kiểm tra xem mỗi cặp (nhân viên, sản phẩm) chỉ xuất hiện một lần
        """
        if any(self.errors):
            return
        
        employee_products = []
        duplicates = False
        
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                employee = form.cleaned_data.get('employee')
                product = form.cleaned_data.get('product')
                
                if (employee, product) in employee_products:
                    duplicates = True
                    form.add_error('employee', _('Mỗi nhân viên chỉ được phân bổ một loại sản phẩm một lần'))
                    form.add_error('product', _('Mỗi sản phẩm chỉ được phân bổ cho một nhân viên một lần'))
                employee_products.append((employee, product))
        
        if duplicates:
            raise forms.ValidationError(_('Vui lòng sửa các lỗi trùng lặp trong form'))


# Formset để phân bổ sản phẩm cho từng nhân viên
EmployeeProductFormSet = inlineformset_factory(
    InventoryRequest,
    EmployeeProductRequest,
    form=EmployeeProductRequestForm,
    formset=BaseEmployeeProductFormSet,
    extra=1,
    can_delete=True
)


class RequestCompletionForm(forms.Form):
    """
    Form cho việc hoàn thành cấp phát
    """
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label=_('Ghi chú')
    )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request:
            # Thêm trường số lượng thực tế cấp phát cho từng sản phẩm
            for item in self.request.items.all():
                field_name = f'issued_quantity_{item.id}'
                max_value = min(item.product.current_quantity, item.approved_quantity)
                
                self.fields[field_name] = forms.IntegerField(
                    label=f'{item.product.name}',
                    min_value=0,
                    max_value=max_value,
                    initial=item.approved_quantity,
                    required=True,
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control',
                        'min': '0',
                        'max': str(max_value)
                    })
                )