from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum, F, Q
from django.core.paginator import Paginator
from django.urls import reverse
import json

from .stock_models import StockReceipt, StockReceiptItem
from .stock_forms import StockReceiptForm, StockReceiptItemFormSet
from suppliers.models import PurchaseOrder, PurchaseOrderItem
from inventory.models import Product


@login_required
def stock_receipt_list(request):
    """Hiển thị danh sách các phiếu nhập kho"""
    search_query = request.GET.get('search', '')
    po_number = request.GET.get('po_number', '')
    
    receipts = StockReceipt.objects.select_related('purchase_order', 'created_by').all()
    
    if search_query:
        receipts = receipts.filter(
            Q(receipt_number__icontains=search_query) | 
            Q(purchase_order__po_number__icontains=search_query) |
            Q(purchase_order__supplier__name__icontains=search_query)
        )
    
    if po_number:
        receipts = receipts.filter(purchase_order__po_number__icontains=po_number)
    
    paginator = Paginator(receipts, 10)  # 10 phiếu nhập mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventory/stock_receipt_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'po_number': po_number,
        'title': 'Danh sách phiếu nhập kho'
    })


@login_required
def stock_receipt_create(request):
    """Tạo phiếu nhập kho mới (Đơn giản hóa) với thêm debug"""
    if request.method == 'POST':
        form = StockReceiptForm(request.POST)
        formset = StockReceiptItemFormSet(request.POST, prefix='items')
        
        # Debug thông tin form và formset
        print("=== DEBUG TẠO PHIẾU NHẬP KHO ===")
        print(f"Form hợp lệ: {form.is_valid()}")
        if not form.is_valid():
            print(f"Lỗi form: {form.errors}")
        
        print(f"Formset hợp lệ: {formset.is_valid()}")
        if not formset.is_valid():
            print(f"Lỗi formset: {formset.errors}")
            
        # Nếu form và formset đều hợp lệ
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Lưu phiếu nhập
                    receipt = form.save(commit=False)
                    receipt.created_by = request.user
                    # Tạo mã phiếu nhập mới
                    if not receipt.receipt_number:
                        receipt.receipt_number = receipt.generate_receipt_number()
                    print(f"Mã phiếu nhập trước khi lưu: {receipt.receipt_number}")
                    
                    # Debug thông tin phiếu nhập kho
                    print(f"Thông tin phiếu nhập trước khi lưu:")
                    print(f"- ID: {receipt.id}")
                    print(f"- Mã phiếu nhập: {receipt.receipt_number}")
                    print(f"- Đơn đặt hàng: {receipt.purchase_order}")
                    print(f"- Ngày nhập: {receipt.receipt_date}")
                    print(f"- Người tạo: {receipt.created_by}")
                    
                    # Lưu phiếu nhập
                    try:
                        receipt.save()
                        print(f"Đã tạo phiếu nhập kho mới: {receipt.receipt_number} (ID: {receipt.id})")
                    except Exception as e:
                        print(f"Lỗi khi lưu phiếu nhập kho: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        raise e
                    
                    # Xử lý từng form sản phẩm
                    product_count = 0
                    for item_form in formset:
                        if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                            product = item_form.cleaned_data.get('product')
                            quantity = item_form.cleaned_data.get('quantity')
                            notes = item_form.cleaned_data.get('notes', '')
                            
                            print(f"Đang xử lý sản phẩm: {product} - SL: {quantity}")
                            
                            if not product:
                                print("ERROR: Không có sản phẩm được chọn!")
                                continue
                                
                            # Tạo và lưu chi tiết phiếu nhập
                            item = item_form.save(commit=False)
                            item.receipt = receipt
                            
                            # Đảm bảo sản phẩm được gán đúng
                            item.product = product
                            
                            # Tìm mục trong đơn đặt hàng tương ứng với sản phẩm này
                            if receipt.purchase_order:
                                po_item = PurchaseOrderItem.objects.filter(
                                    purchase_order=receipt.purchase_order,
                                    product=product
                                ).first()
                                
                                if po_item:
                                    print(f"Đã tìm thấy chi tiết đơn hàng tương ứng với sản phẩm {product.name}")
                                    item.purchase_order_item = po_item
                                else:
                                    # Nếu sản phẩm chưa tồn tại trong đơn hàng, tạo mới
                                    try:
                                        po_item = PurchaseOrderItem.objects.create(
                                            purchase_order=receipt.purchase_order,
                                            product=product,
                                            quantity=quantity,
                                            unit_price=product.latest_purchase_price or 0
                                        )
                                        print(f"Đã tạo chi tiết đơn hàng mới cho sản phẩm {product.name}")
                                        item.purchase_order_item = po_item
                                    except Exception as e:
                                        print(f"Không thể tạo chi tiết đơn hàng: {str(e)}")
                                        item.purchase_order_item = None
                            else:
                                print(f"Phiếu nhập kho không liên kết với đơn đặt hàng nào")
                                item.purchase_order_item = None
                            
                            print(f"Đã gán sản phẩm {product.name} (ID: {product.id}) cho StockReceiptItem")
                            
                            try:
                                # Thay vì sử dụng StockReceiptItem.objects.create, sử dụng SQL trực tiếp
                                from django.db import connection
                                cursor = connection.cursor()
                                
                                # Lấy purchase_order_item_id nếu có
                                po_item_id = item.purchase_order_item.id if item.purchase_order_item else None
                                
                                cursor.execute("""
                                    INSERT INTO inventory_stockreceiptitem 
                                    (product_id, receipt_id, quantity, notes, created_at, purchase_order_item_id)
                                    VALUES (%s, %s, %s, %s, NOW(), %s)
                                """, [product.id, receipt.id, quantity, notes, po_item_id])
                                print("Đã thêm chi tiết phiếu nhập trực tiếp vào DB sử dụng SQL")
                                print(f"Đã tạo chi tiết phiếu nhập cho sản phẩm {product.name}")
                                product_count += 1
                                
                                # Cập nhật số lượng sản phẩm trong kho
                                product.current_quantity += quantity
                                product.save(update_fields=['current_quantity'])
                                print(f"Đã cập nhật số lượng sản phẩm {product.name}: {product.current_quantity}")
                            except Exception as e:
                                print(f"Lỗi khi lưu chi tiết phiếu nhập: {str(e)}")
                                import traceback
                                traceback.print_exc()
                                raise e
                    
                    print(f"Tổng số sản phẩm đã nhập kho: {product_count}")
                    
                    # Xóa tất cả messages cũ (từ việc tạo nhà cung cấp, đơn hàng, sản phẩm, v.v.)
                    storage = messages.get_messages(request)
                    storage.used = True
                    
                    # Tạo thông báo thành công duy nhất
                    messages.success(request, f'Phiếu nhập kho {receipt.receipt_number} đã được tạo thành công với {product_count} sản phẩm!')
                    
                    # Kiểm tra phiếu nhập đã tạo
                    try:
                        verify_receipt = StockReceipt.objects.get(id=receipt.id)
                        print(f"Đã xác minh phiếu nhập tồn tại: {verify_receipt.receipt_number} (ID: {verify_receipt.id})")
                        return redirect('stock_receipt_detail', pk=receipt.id)
                    except StockReceipt.DoesNotExist:
                        print(f"ERROR: Không thể tìm thấy phiếu nhập vừa tạo với ID: {receipt.id}")
                        messages.error(request, f"Lỗi: Không thể tạo phiếu nhập kho.")
                        return redirect('stock_receipt_list')
            except Exception as e:
                print(f"Lỗi khi tạo phiếu nhập kho: {str(e)}")
                import traceback
                traceback.print_exc()
                messages.error(request, f"Lỗi: {str(e)}")
    else:
        form = StockReceiptForm()
        formset = StockReceiptItemFormSet(prefix='items')
    
    po_id = request.GET.get('po_id')
    if po_id:
        po = get_object_or_404(PurchaseOrder, id=po_id)
        form = StockReceiptForm(initial={'purchase_order': po})
        
    purchase_orders = PurchaseOrder.objects.filter(
        status__in=['approved', 'pending']
    ).select_related('supplier')
    
    # Kiểm tra xem có đơn đặt hàng nào không
    if not purchase_orders.exists():
        messages.warning(request, 'Không có đơn đặt hàng nào để nhập kho. Vui lòng tạo đơn đặt hàng trước.')
    
    # Kiểm tra xem có đơn đặt hàng nào có sản phẩm không
    has_products = False
    for po in purchase_orders:
        if po.items.exists():
            has_products = True
            break
    
    if purchase_orders.exists() and not has_products:
        messages.warning(request, 'Các đơn đặt hàng hiện tại chưa có sản phẩm nào. Vui lòng thêm sản phẩm vào đơn đặt hàng.')
    
    # Lấy tất cả sản phẩm để truyền vào template
    products = Product.objects.all().select_related('unit')
    products_data = {}
    for product in products:
        products_data[str(product.id)] = {  # Chuyển ID thành string để làm key trong JSON
            'name': product.name,
            'code': product.product_code,
            'current_quantity': product.current_quantity,
            'unit': product.unit.name if product.unit else ''
        }
    
    return render(request, 'inventory/stock_receipt_form_simple.html', {
        'form': form,
        'formset': formset,
        'purchase_orders': purchase_orders,
        'title': 'Tạo phiếu nhập kho',
        'has_products': has_products,
        'products_data': json.dumps(products_data)  # Chuyển thành JSON string
    })


@login_required
def stock_receipt_detail(request, pk):
    """Hiển thị chi tiết phiếu nhập kho"""
    receipt = get_object_or_404(StockReceipt, pk=pk)
    
    try:
        # Trực tiếp lấy sản phẩm từ trường product
        items = receipt.items.select_related('product', 'product__unit').all()
        
        print(f"=== CHI TIẾT PHIẾU NHẬP KHO ===")
        print(f"Phiếu nhập: {receipt.receipt_number} (ID: {receipt.id})")
        print(f"Số lượng chi tiết: {items.count()}")
        for item in items:
            print(f"- Sản phẩm: {item.product.name if item.product else 'Không có'}")
            print(f"  Số lượng: {item.quantity}")
        
        return render(request, 'inventory/stock_receipt_detail.html', {
            'receipt': receipt,
            'items': items,
            'title': f'Chi tiết phiếu nhập kho: {receipt.receipt_number}'
        })
    except Exception as e:
        print(f"Lỗi khi hiển thị chi tiết phiếu nhập kho: {str(e)}")
        import traceback
        traceback.print_exc()
        messages.error(request, f"Có lỗi xảy ra khi hiển thị chi tiết phiếu nhập kho: {str(e)}")
        return redirect('stock_receipt_list')


@login_required
def get_purchase_order_items(request):
    """API để lấy danh sách sản phẩm cho phiếu nhập kho"""
    po_id = request.GET.get('po_id')
    if not po_id:
        print("Lỗi: Không có ID đơn đặt hàng")
        return JsonResponse({'error': 'Không có ID đơn đặt hàng'}, status=400)
    
    try:
        print(f"=== Lấy danh sách sản phẩm cho đơn đặt hàng ID: {po_id} ===")
        
        # Kiểm tra xem đơn đặt hàng có tồn tại không
        po = PurchaseOrder.objects.filter(id=po_id).first()
        if not po:
            print(f"Không tìm thấy đơn đặt hàng với ID {po_id}")
            return JsonResponse({
                'error': f'Đơn đặt hàng với ID {po_id} không tồn tại',
                'items': []
            }, status=404)
            
        print(f"Đã tìm thấy đơn đặt hàng: {po.po_number} - Nhà cung cấp: {po.supplier.name}")
        
        # Lấy các sản phẩm đã có trong đơn hàng
        po_items = PurchaseOrderItem.objects.filter(purchase_order_id=po_id).select_related('product', 'product__unit')
        print(f"Số sản phẩm trong đơn hàng {po.po_number}: {po_items.count()}")
        
        # Nếu đơn hàng không có sản phẩm nào, lấy tất cả sản phẩm trong hệ thống
        all_products = []
        if not po_items.exists():
            print("Đơn hàng không có sản phẩm nào, lấy tất cả sản phẩm trong hệ thống")
            all_products = Product.objects.all().select_related('unit')
            print(f"Tổng số sản phẩm trong hệ thống: {all_products.count()}")
            
            if not all_products.exists():
                print("Không có sản phẩm nào trong hệ thống")
                return JsonResponse({
                    'message': 'Không có sản phẩm nào trong hệ thống. Vui lòng thêm sản phẩm trước.',
                    'items': []
                })
        
        items_data = []
        
        # Trước tiên, thêm các sản phẩm đã có trong đơn hàng
        for po_item in po_items:
            product = po_item.product
            item_data = {
                'id': po_item.id,  # Sử dụng ID của mục đơn hàng
                'po_item_id': po_item.id,
                'product_id': product.id,
                'product_code': product.product_code,
                'product_name': product.name,
                'unit': product.unit.name if product.unit else '',
                'current_quantity': product.current_quantity,
                'order_quantity': po_item.quantity,  # Số lượng đã đặt
                'received_quantity': 0,  # Sẽ tính toán sau
                'unit_price': str(po_item.unit_price) or str(product.latest_purchase_price) or '0',
                'is_in_po': True  # Đánh dấu sản phẩm đã có trong đơn hàng
            }
            
            # Tính số lượng đã nhập kho
            from django.db.models import Sum
            received_qty = StockReceiptItem.objects.filter(
                purchase_order_item=po_item
            ).aggregate(total=Sum('quantity'))['total'] or 0
            item_data['received_quantity'] = received_qty
            
            print(f"Sản phẩm trong PO: {product.name}, Mã: {product.product_code}, SL đặt: {po_item.quantity}, SL đã nhập: {received_qty}")
            items_data.append(item_data)
            print(f"Đã thêm sản phẩm {product.name} từ đơn hàng vào danh sách trả về")
            
        # Sau đó, thêm các sản phẩm khác trong hệ thống (nếu cần)
        if all_products:
            for product in all_products:
                item_data = {
                    'id': product.id,  # Sử dụng ID của sản phẩm trực tiếp
                    'product_id': product.id,
                    'product_code': product.product_code,
                    'product_name': product.name,
                    'unit': product.unit.name if product.unit else '',
                    'current_quantity': product.current_quantity,
                    'unit_price': str(product.latest_purchase_price) if product.latest_purchase_price else '0',
                    'is_in_po': False  # Đánh dấu sản phẩm không có trong đơn hàng
                }
                
                print(f"Sản phẩm: {product.name}, Mã: {product.product_code}, SL hiện tại: {product.current_quantity}")
                items_data.append(item_data)
                print(f"Đã thêm sản phẩm {product.name} vào danh sách trả về")
        
        print(f"Trả về {len(items_data)} sản phẩm để chọn")
        return JsonResponse({'items': items_data})
        
    except Exception as e:
        import traceback
        print("Lỗi khi lấy danh sách sản phẩm:", str(e))
        print(traceback.format_exc())
        return JsonResponse({
            'error': f'Có lỗi xảy ra: {str(e)}',
            'items': []
        }, status=500)
    
    except Exception as e:
        import traceback
        print("Lỗi khi lấy danh sách sản phẩm:", str(e))
        print(traceback.format_exc())
        return JsonResponse({
            'error': f'Có lỗi xảy ra: {str(e)}',
            'items': []
        }, status=500)


def update_purchase_order_status(purchase_order):
    """Cập nhật trạng thái đơn đặt hàng dựa trên số lượng đã nhập kho"""
    po_items = purchase_order.items.all()
    all_items_received = True
    
    for po_item in po_items:
        # Tính số lượng đã nhập kho của sản phẩm này
        received_quantity = StockReceiptItem.objects.filter(
            purchase_order_item=po_item
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        if received_quantity < po_item.quantity:
            all_items_received = False
            break
    
    # Nếu tất cả sản phẩm đã được nhập đủ, cập nhật trạng thái đơn hàng thành "completed"
    if all_items_received and purchase_order.status != 'completed':
        purchase_order.status = 'completed'
        purchase_order.save(update_fields=['status'])