from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, F

from .models import Category, Unit, Warehouse, WarehouseRow, WarehouseColumn, Product, StockTransaction
from .forms import (
    CategoryForm, UnitForm, WarehouseForm, WarehouseRowForm, WarehouseColumnForm, ProductForm
)

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'inventory/category_detail.html'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Danh mục đã được tạo thành công.")
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Danh mục đã được cập nhật thành công.")
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Danh mục đã được xóa thành công.")
        return super().delete(request, *args, **kwargs)

# Unit Views
class UnitListView(LoginRequiredMixin, ListView):
    model = Unit
    template_name = 'inventory/unit_list.html'
    context_object_name = 'units'

class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Unit
    template_name = 'inventory/unit_detail.html'

class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'inventory/unit_form.html'
    success_url = reverse_lazy('unit_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Đơn vị tính đã được tạo thành công.")
        return super().form_valid(form)

class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'inventory/unit_form.html'
    success_url = reverse_lazy('unit_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Đơn vị tính đã được cập nhật thành công.")
        return super().form_valid(form)

class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    template_name = 'inventory/unit_confirm_delete.html'
    success_url = reverse_lazy('unit_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Đơn vị tính đã được xóa thành công.")
        return super().delete(request, *args, **kwargs)

# Warehouse Views
class WarehouseListView(LoginRequiredMixin, ListView):
    model = Warehouse
    template_name = 'inventory/warehouse_list.html'
    context_object_name = 'warehouses'

class WarehouseDetailView(LoginRequiredMixin, DetailView):
    model = Warehouse
    template_name = 'inventory/warehouse_detail.html'

class WarehouseCreateView(LoginRequiredMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'inventory/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Kho đã được tạo thành công.")
        return super().form_valid(form)

class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'inventory/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Kho đã được cập nhật thành công.")
        return super().form_valid(form)

class WarehouseDeleteView(LoginRequiredMixin, DeleteView):
    model = Warehouse
    template_name = 'inventory/warehouse_confirm_delete.html'
    success_url = reverse_lazy('warehouse_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Kho đã được xóa thành công.")
        return super().delete(request, *args, **kwargs)

# WarehouseRow Views
class WarehouseRowListView(LoginRequiredMixin, ListView):
    model = WarehouseRow
    template_name = 'inventory/warehouse_row_list.html'
    context_object_name = 'rows'

class WarehouseRowDetailView(LoginRequiredMixin, DetailView):
    model = WarehouseRow
    template_name = 'inventory/warehouse_row_detail.html'

class WarehouseRowCreateView(LoginRequiredMixin, CreateView):
    model = WarehouseRow
    form_class = WarehouseRowForm
    template_name = 'inventory/warehouse_row_form.html'
    success_url = reverse_lazy('warehouse_row_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Dãy kho đã được tạo thành công.")
        return super().form_valid(form)

class WarehouseRowUpdateView(LoginRequiredMixin, UpdateView):
    model = WarehouseRow
    form_class = WarehouseRowForm
    template_name = 'inventory/warehouse_row_form.html'
    success_url = reverse_lazy('warehouse_row_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Dãy kho đã được cập nhật thành công.")
        return super().form_valid(form)

class WarehouseRowDeleteView(LoginRequiredMixin, DeleteView):
    model = WarehouseRow
    template_name = 'inventory/warehouse_row_confirm_delete.html'
    success_url = reverse_lazy('warehouse_row_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Dãy kho đã được xóa thành công.")
        return super().delete(request, *args, **kwargs)

# WarehouseColumn Views
class WarehouseColumnListView(LoginRequiredMixin, ListView):
    model = WarehouseColumn
    template_name = 'inventory/warehouse_column_list.html'
    context_object_name = 'columns'

class WarehouseColumnDetailView(LoginRequiredMixin, DetailView):
    model = WarehouseColumn
    template_name = 'inventory/warehouse_column_detail.html'

class WarehouseColumnCreateView(LoginRequiredMixin, CreateView):
    model = WarehouseColumn
    form_class = WarehouseColumnForm
    template_name = 'inventory/warehouse_column_form.html'
    success_url = reverse_lazy('warehouse_column_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Cột kho đã được tạo thành công.")
        return super().form_valid(form)

class WarehouseColumnUpdateView(LoginRequiredMixin, UpdateView):
    model = WarehouseColumn
    form_class = WarehouseColumnForm
    template_name = 'inventory/warehouse_column_form.html'
    success_url = reverse_lazy('warehouse_column_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Cột kho đã được cập nhật thành công.")
        return super().form_valid(form)

class WarehouseColumnDeleteView(LoginRequiredMixin, DeleteView):
    model = WarehouseColumn
    template_name = 'inventory/warehouse_column_confirm_delete.html'
    success_url = reverse_lazy('warehouse_column_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cột kho đã được xóa thành công.")
        return super().delete(request, *args, **kwargs)

# Product Views
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        low_stock = self.request.GET.get('low_stock', '')
        
        if search:
            queryset = queryset.filter(
                Q(product_code__icontains=search) | 
                Q(name__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
            
        if low_stock:
            queryset = queryset.filter(current_quantity__lte=F('minimum_quantity'))
            
        return queryset.select_related('category', 'unit', 'column__row__warehouse')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'category', 'unit', 'column__row__warehouse'
        )

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Sản phẩm đã được tạo thành công.")
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Sản phẩm đã được cập nhật thành công.")
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Sản phẩm đã được xóa thành công.")
        return super().delete(request, *args, **kwargs)

class LowStockProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/low_stock_products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(
            current_quantity__lte=F('minimum_quantity')
        ).select_related('category', 'unit', 'column__row__warehouse')


# Stock Transaction Views
class StockTransactionListView(LoginRequiredMixin, ListView):
    model = StockTransaction
    template_name = 'inventory/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('product', 'created_by')
        
        # Filter by transaction type
        transaction_type = self.request.GET.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(transaction_code__icontains=search) |
                Q(product__name__icontains=search) |
                Q(reference_code__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_type'] = self.request.GET.get('type', '')
        context['search'] = self.request.GET.get('search', '')
        return context


class StockTransactionCreateView(LoginRequiredMixin, CreateView):
    model = StockTransaction
    template_name = 'inventory/transaction_create.html'
    fields = ['product', 'transaction_type', 'quantity', 'reference_code', 'notes']
    success_url = reverse_lazy('inventory:transaction_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Kiểm tra số lượng xuất
        if form.instance.transaction_type == 'OUT' and form.instance.quantity > form.instance.product.current_quantity:
            messages.error(self.request, f'Số lượng xuất vượt quá tồn kho hiện tại ({form.instance.product.current_quantity})')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Đã tạo giao dịch thành công!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('name')
        return context


class StockTransactionDetailView(LoginRequiredMixin, DetailView):
    model = StockTransaction
    template_name = 'inventory/transaction_detail.html'
    context_object_name = 'transaction'
    
    def get_queryset(self):
        return super().get_queryset().select_related('product', 'created_by')
