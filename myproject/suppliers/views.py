from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Supplier, PurchaseOrder, PurchaseOrderItem
from .forms import SupplierForm, PurchaseOrderForm, PurchaseOrderItemForm

# Supplier Views
@login_required
def supplier_list(request):
    search_query = request.GET.get('search', '')
    suppliers = Supplier.objects.all()
    
    if search_query:
        suppliers = suppliers.filter(
            Q(code__icontains=search_query) | 
            Q(name__icontains=search_query) | 
            Q(address__icontains=search_query) |
            Q(contact_name__icontains=search_query) |
            Q(contact_phone__icontains=search_query) |
            Q(contact_email__icontains=search_query)
        )
    
    paginator = Paginator(suppliers, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'title': 'Danh sách nhà cung cấp'
    }
    return render(request, 'suppliers/supplier_list.html', context)


@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nhà cung cấp đã được tạo thành công!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'suppliers/supplier_form.html', {
        'form': form,
        'title': 'Thêm nhà cung cấp mới'
    })


@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nhà cung cấp đã được cập nhật thành công!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'suppliers/supplier_form.html', {
        'form': form,
        'supplier': supplier,
        'title': 'Cập nhật nhà cung cấp'
    })


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        try:
            supplier.delete()
            messages.success(request, 'Nhà cung cấp đã được xóa thành công!')
        except Exception as e:
            messages.error(request, f'Không thể xóa nhà cung cấp này. Lỗi: {str(e)}')
        return redirect('supplier_list')
    
    return render(request, 'suppliers/supplier_confirm_delete.html', {
        'supplier': supplier,
        'title': 'Xóa nhà cung cấp'
    })


@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    purchase_orders = supplier.purchase_orders.all()
    
    paginator = Paginator(purchase_orders, 5)  # 5 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'suppliers/supplier_detail.html', {
        'supplier': supplier,
        'page_obj': page_obj,
        'title': f'Thông tin nhà cung cấp: {supplier.name}'
    })


# Purchase Order Views
@login_required
def po_list(request):
    search_query = request.GET.get('search', '')
    supplier_id = request.GET.get('supplier', '')
    status = request.GET.get('status', '')
    
    purchase_orders = PurchaseOrder.objects.all()
    
    # Tìm kiếm
    if search_query:
        purchase_orders = purchase_orders.filter(
            Q(po_number__icontains=search_query) | 
            Q(supplier__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Lọc theo nhà cung cấp
    if supplier_id:
        purchase_orders = purchase_orders.filter(supplier_id=supplier_id)
    
    # Lọc theo trạng thái
    if status:
        purchase_orders = purchase_orders.filter(status=status)
    
    # Phân trang
    paginator = Paginator(purchase_orders, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Danh sách nhà cung cấp cho bộ lọc
    suppliers = Supplier.objects.all()
    
    context = {
        'page_obj': page_obj,
        'suppliers': suppliers,
        'search_query': search_query,
        'selected_supplier': supplier_id,
        'selected_status': status,
        'title': 'Danh sách đơn đặt hàng'
    }
    return render(request, 'suppliers/po_list.html', context)


@login_required
def po_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đơn đặt hàng đã được tạo thành công!')
            return redirect('po_list')
    else:
        form = PurchaseOrderForm()
    
    return render(request, 'suppliers/po_form.html', {
        'form': form,
        'title': 'Tạo đơn đặt hàng mới'
    })


@login_required
def po_update(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, request.FILES, instance=purchase_order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đơn đặt hàng đã được cập nhật thành công!')
            return redirect('po_list')
    else:
        form = PurchaseOrderForm(instance=purchase_order)
    
    return render(request, 'suppliers/po_form.html', {
        'form': form,
        'purchase_order': purchase_order,
        'title': 'Cập nhật đơn đặt hàng'
    })


@login_required
def po_delete(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    
    if request.method == 'POST':
        try:
            purchase_order.delete()
            messages.success(request, 'Đơn đặt hàng đã được xóa thành công!')
        except Exception as e:
            messages.error(request, f'Không thể xóa đơn đặt hàng này. Lỗi: {str(e)}')
        return redirect('po_list')
    
    return render(request, 'suppliers/po_confirm_delete.html', {
        'purchase_order': purchase_order,
        'title': 'Xóa đơn đặt hàng'
    })


@login_required
def po_detail(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    items = purchase_order.items.all()
    
    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.purchase_order = purchase_order
            item.save()
            messages.success(request, 'Sản phẩm đã được thêm vào đơn hàng!')
            return redirect('po_detail', pk=purchase_order.pk)
    else:
        form = PurchaseOrderItemForm()

    return render(request, 'suppliers/po_detail.html', {
        'purchase_order': purchase_order,
        'items': items,
        'form': form,
        'title': f'Chi tiết đơn đặt hàng: {purchase_order.po_number}'
    })


@login_required
@require_POST
def po_item_delete(request, pk):
    item = get_object_or_404(PurchaseOrderItem, pk=pk)
    po_id = item.purchase_order.id
    
    try:
        item.delete()
        messages.success(request, 'Sản phẩm đã được xóa khỏi đơn hàng!')
    except Exception as e:
        messages.error(request, f'Không thể xóa sản phẩm khỏi đơn hàng. Lỗi: {str(e)}')
    
    return redirect('po_detail', pk=po_id)


@login_required
def po_item_update(request, pk):
    item = get_object_or_404(PurchaseOrderItem, pk=pk)
    po_id = item.purchase_order.id
    
    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chi tiết đơn hàng đã được cập nhật!')
            return redirect('po_detail', pk=po_id)
    else:
        form = PurchaseOrderItemForm(instance=item)
    
    return render(request, 'suppliers/po_item_form.html', {
        'form': form,
        'item': item,
        'purchase_order': item.purchase_order,
        'title': 'Cập nhật chi tiết đơn hàng'
    })
