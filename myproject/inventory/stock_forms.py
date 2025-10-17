from django import forms
from django.forms import inlineformset_factory, formset_factory, BaseFormSet

from .stock_models import StockReceipt, StockReceiptItem
from suppliers.models import PurchaseOrder, PurchaseOrderItem
from inventory.models import Product


class StockReceiptForm(forms.ModelForm):
    """Form cho phiếu nhập kho"""
    class Meta:
        model = StockReceipt
        fields = ['purchase_order', 'receipt_date', 'notes']
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_order': forms.Select(attrs={'class': 'form-control select2'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cập nhật lựa chọn đơn đặt hàng để hiển thị thêm thông tin nhà cung cấp
        purchase_orders = PurchaseOrder.objects.filter(status__in=['approved', 'pending']).select_related('supplier')
        self.fields['purchase_order'].queryset = purchase_orders
        self.fields['purchase_order'].label_from_instance = lambda obj: f"{obj.po_number} - {obj.supplier.name}"


class StockReceiptItemForm(forms.ModelForm):
    """Form cho chi tiết phiếu nhập kho đơn giản hóa"""
    current_quantity = forms.IntegerField(
        label="SL hiện tại",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
    )
    
    class Meta:
        model = StockReceiptItem
        fields = ['product', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control select2 product-select',
                'placeholder': 'Chọn sản phẩm',
                'data-width': '100%'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Nhập số lượng'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ghi chú'
            })
        }
    
    def __init__(self, *args, **kwargs):
        po_id = kwargs.pop('po_id', None)
        super().__init__(*args, **kwargs)
        
        # Lấy tất cả sản phẩm trong hệ thống
        products = Product.objects.all().select_related('unit').order_by('name')
        self.fields['product'].queryset = products
        
        # Chỉ hiển thị tên sản phẩm
        self.fields['product'].label_from_instance = lambda obj: obj.name
        
        # Nếu có instance và product đã được chọn, cập nhật current_quantity
        if self.instance and self.instance.product_id:
            self.initial['current_quantity'] = self.instance.product.current_quantity
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Lấy sản phẩm từ form và gán trực tiếp vào instance
        product = self.cleaned_data.get('product')
        if product:
            instance.product = product
            print(f"Đã gán sản phẩm {product.name} (ID: {product.id}) cho StockReceiptItem")
        else:
            print("CẢNH BÁO: Không có sản phẩm được gán cho StockReceiptItem")
            
        if commit:
            try:
                instance.save()
                print(f"Đã lưu StockReceiptItem với ID: {instance.id} - Sản phẩm: {instance.product.name if instance.product else 'Không có'}")
            except Exception as e:
                print(f"Lỗi khi lưu StockReceiptItem: {str(e)}")
                import traceback
                traceback.print_exc()
                raise e
        
        return instance


# Tạo formset cho StockReceiptItem
class BaseStockReceiptItemFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        # Kiểm tra xem có ít nhất một sản phẩm được thêm vào
        if any(self.errors):
            return
            
        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                for form in self.forms):
            raise forms.ValidationError('Vui lòng thêm ít nhất một sản phẩm vào phiếu nhập kho.')
            
        # Kiểm tra sản phẩm trùng lặp
        products = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                po_item = form.cleaned_data.get('purchase_order_item')
                if po_item:
                    if po_item in products:
                        raise forms.ValidationError(f'Sản phẩm {po_item.product.name} đã được thêm vào phiếu nhập kho.')
                    products.append(po_item)


StockReceiptItemFormSet = inlineformset_factory(
    StockReceipt,
    StockReceiptItem,
    form=StockReceiptItemForm,
    formset=BaseStockReceiptItemFormSet,
    extra=1,
    can_delete=True
)