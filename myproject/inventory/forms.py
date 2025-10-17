from django import forms
from .models import Category, Unit, Warehouse, WarehouseRow, WarehouseColumn, Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML("<hr>"),
            Submit('submit', 'Lưu', css_class='btn btn-success')
        )

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'abbreviation']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('abbreviation', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML("<hr>"),
            Submit('submit', 'Lưu', css_class='btn btn-success')
        )

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'description', 'active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-9 mb-0'),
                Column('active', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            HTML("<hr>"),
            Submit('submit', 'Lưu', css_class='btn btn-success')
        )

class WarehouseRowForm(forms.ModelForm):
    class Meta:
        model = WarehouseRow
        fields = ['warehouse', 'row_code', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('warehouse', css_class='form-group col-md-6 mb-0'),
                Column('row_code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML("<hr>"),
            Submit('submit', 'Lưu', css_class='btn btn-success')
        )

class WarehouseColumnForm(forms.ModelForm):
    class Meta:
        model = WarehouseColumn
        fields = ['row', 'column_code', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('row', css_class='form-group col-md-6 mb-0'),
                Column('column_code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML("<hr>"),
            Submit('submit', 'Lưu', css_class='btn btn-success')
        )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_code', 'name', 'category', 'unit',
            'column', 'current_quantity', 
            'minimum_quantity', 'description'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('product_code', css_class='form-group col-md-6 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),      
                Column('unit', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('column', css_class='form-group col-md-4 mb-0'),
                Column('current_quantity', css_class='form-group col-md-4 mb-0'),
                Column('minimum_quantity', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML("<hr>"),
            Submit('submit', 'Lưu', css_class='btn btn-success')
        )
        
        # Tùy chỉnh form fields
        if 'column' in self.fields:
            self.fields['column'].queryset = WarehouseColumn.objects.select_related('row', 'row__warehouse')