from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
import logging

from myproject.decorators import role_required
from system_settings.template_email_service import send_template_email

logger = logging.getLogger(__name__)

from .models import InventoryRequest, RequestEmployee, RequestItem, EmployeeProductRequest
from .forms import (
    InventoryRequestForm, RequestEmployeeFormSet, RequestItemFormSet,
    RequestApprovalForm, RequestScheduleForm, RequestCompletionForm,
    EmployeeProductFormSet
)

# Import User model cho các email CC
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def inventory_request_list(request):
    """Danh sách tất cả các yêu cầu cấp phát (cho admin/quản lý)"""
    
    # Lọc theo quyền người dùng
    if request.user.is_superuser or request.user.role in ['sm', 'admin']:
        requests = InventoryRequest.objects.all()
    elif request.user.role == 'manager':
        # Quản lý thấy yêu cầu của nhân viên mình quản lý + của chính mình
        subordinates = request.user.subordinates.all()
        requests = InventoryRequest.objects.filter(
            Q(requester__in=subordinates) | Q(requester=request.user)
        )
    else:
        # Nhân viên chỉ thấy yêu cầu của mình
        requests = InventoryRequest.objects.filter(requester=request.user)
    
    # Sắp xếp và phân trang
    requests = requests.order_by('-created_at')
    paginator = Paginator(requests, 10)
    page = request.GET.get('page')
    requests = paginator.get_page(page)
    
    context = {
        'requests': requests,
        'title': 'Danh sách yêu cầu cấp phát',
    }
    
    return render(request, 'inventory_requests/request_list.html', context)


@login_required
def my_requests_list(request):
    """Danh sách yêu cầu cấp phát của tôi"""
    
    requests = InventoryRequest.objects.filter(requester=request.user).order_by('-created_at')
    
    # Sắp xếp và phân trang
    paginator = Paginator(requests, 10)
    page = request.GET.get('page')
    requests = paginator.get_page(page)
    
    context = {
        'requests': requests,
        'title': 'Yêu cầu cấp phát của tôi',
    }
    
    return render(request, 'inventory_requests/my_requests.html', context)


@login_required
def my_approvals_list(request):
    """Danh sách yêu cầu cần tôi phê duyệt"""
    
    # Chỉ quản lý mới thấy yêu cầu cần phê duyệt
    if not (request.user.is_superuser or request.user.role in ['sm', 'admin', 'manager']):
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('inventory_requests:my_requests')
    
    # Lấy danh sách nhân viên dưới quyền
    subordinates = request.user.subordinates.all()
    
    # Lấy các yêu cầu chờ phê duyệt của nhân viên dưới quyền
    requests = InventoryRequest.objects.filter(
        requester__in=subordinates,
        status=InventoryRequest.STATUS_PENDING
    ).order_by('-created_at')
    
    # Sắp xếp và phân trang
    paginator = Paginator(requests, 10)
    page = request.GET.get('page')
    requests = paginator.get_page(page)
    
    context = {
        'requests': requests,
        'title': 'Yêu cầu cần phê duyệt',
    }
    
    return render(request, 'inventory_requests/my_approvals.html', context)


@login_required
def inventory_request_create(request):
    """Tạo yêu cầu cấp phát mới"""
    
    if request.method == 'POST':
        form = InventoryRequestForm(request.POST)
        
        if form.is_valid():
            # Tạo request object nhưng chưa lưu vào DB
            request_obj = form.save(commit=False)
            request_obj.requester = request.user
            request_obj.status = InventoryRequest.STATUS_DRAFT
            request_obj.save()  # Phải save trước khi tạo formset
            
            # Giờ mới tạo formset với instance
            employee_formset = RequestEmployeeFormSet(request.POST, instance=request_obj)
            item_formset = RequestItemFormSet(request.POST, instance=request_obj)
            employee_product_formset = EmployeeProductFormSet(request.POST, instance=request_obj)
            
            # Debug: Kiểm tra số lượng form trong formset
            print(f"DEBUG: Total forms in employee_product_formset: {len(employee_product_formset.forms)}")
            for i, form in enumerate(employee_product_formset.forms):
                if form.cleaned_data if hasattr(form, 'cleaned_data') else None:
                    print(f"DEBUG: Form {i} data: {form.cleaned_data}")
            
            # Validate các formset
            employee_valid = employee_formset.is_valid()
            item_valid = item_formset.is_valid()
            employee_product_valid = employee_product_formset.is_valid()
            
            # Debug: Hiển thị lỗi nếu có
            if not employee_product_valid:
                print(f"DEBUG: employee_product_formset errors: {employee_product_formset.errors}")
                print(f"DEBUG: employee_product_formset non_form_errors: {employee_product_formset.non_form_errors()}")
            
            if employee_valid and item_valid and employee_product_valid:
                with transaction.atomic():
                    # Lưu các formset
                    employee_formset.save()
                    item_formset.save()
                    employee_product_formset.save()
                
                messages.success(request, 'Yêu cầu cấp phát đã được tạo thành công.')
                
                if 'save_draft' in request.POST:
                    return redirect('inventory_requests:my_requests')
                else:
                    # Kiểm tra xem người dùng đã có người quản lý chưa
                    if not request.user.manager:
                        messages.error(request, 'Bạn chưa được gán người quản lý. Vui lòng liên hệ quản trị viên để được gán người quản lý trước khi gửi yêu cầu.')
                        return redirect('inventory_requests:inventory_request_edit', request_id=request_obj.id)
                    
                    if not request.user.manager.email:
                        messages.error(request, 'Người quản lý của bạn chưa có email. Vui lòng liên hệ quản trị viên để cập nhật email cho người quản lý.')
                        return redirect('inventory_requests:inventory_request_edit', request_id=request_obj.id)
                    
                    # Chuyển trạng thái thành chờ phê duyệt và gửi email
                    request_obj.mark_as_pending()
                    
                    # Gửi email thông báo cho người tạo yêu cầu (không làm gián đoạn nếu lỗi)
                    try:
                        send_template_email(
                            recipient_list=[request.user.email],
                            template_code='request_created',
                            context_data={
                                'request': request_obj,
                                'user': request.user,
                                'employee_products': request_obj.employee_products.all(),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Không thể gửi email thông báo cho người tạo yêu cầu: {str(e)}")
                    
                    # Gửi email cho người quản lý để phê duyệt (không làm gián đoạn nếu lỗi)
                    try:
                        send_template_email(
                            recipient_list=[request.user.manager.email],
                            template_code='pending_approval',
                            context_data={
                                'request': request_obj,
                                'user': request.user,
                                'manager': request.user.manager,
                                'employee_products': request_obj.employee_products.all(),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Không thể gửi email cho người quản lý: {str(e)}")
                    
                    messages.success(request, f'Yêu cầu cấp phát đã được gửi đến người quản lý {request.user.manager.get_full_name()} để phê duyệt.')
                    return redirect('inventory_requests:my_requests')
            else:
                # Có lỗi validation trong formset
                if not employee_valid:
                    messages.error(request, 'Có lỗi trong danh sách nhân viên.')
                    
                if not item_valid:
                    messages.error(request, 'Có lỗi trong danh sách sản phẩm.')
                    
                if not employee_product_valid:
                    messages.error(request, 'Có lỗi trong phân bổ sản phẩm cho nhân viên.')
        else:
            # Form chính không valid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            
            # Vẫn tạo formset để hiển thị
            employee_formset = RequestEmployeeFormSet(request.POST)
            item_formset = RequestItemFormSet(request.POST)
            employee_product_formset = EmployeeProductFormSet(request.POST)
    else:
        form = InventoryRequestForm()
        employee_formset = RequestEmployeeFormSet()
        item_formset = RequestItemFormSet()
        employee_product_formset = EmployeeProductFormSet()
        employee_product_formset = EmployeeProductFormSet()
    
    context = {
        'form': form,
        'employee_formset': employee_formset,
        'item_formset': item_formset,
        'employee_product_formset': employee_product_formset,
        'title': 'Tạo yêu cầu cấp phát mới',
        'use_employee_product': True,  # Flag để hiển thị tab phân bổ sản phẩm
    }
    
    return render(request, 'inventory_requests/request_form.html', context)


@login_required
def inventory_request_edit(request, request_id):
    """Chỉnh sửa yêu cầu cấp phát"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra quyền chỉnh sửa
    if request_obj.requester != request.user or not request_obj.can_be_edited:
        messages.error(request, 'Bạn không có quyền chỉnh sửa yêu cầu này hoặc yêu cầu không thể chỉnh sửa.')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    if request.method == 'POST':
        form = InventoryRequestForm(request.POST, instance=request_obj)
        employee_formset = RequestEmployeeFormSet(request.POST, instance=request_obj)
        item_formset = RequestItemFormSet(request.POST, instance=request_obj)
        employee_product_formset = EmployeeProductFormSet(request.POST, instance=request_obj)
        
        # Validate tất cả forms
        form_valid = form.is_valid()
        employee_valid = employee_formset.is_valid()
        item_valid = item_formset.is_valid()
        employee_product_valid = employee_product_formset.is_valid()
        
        if form_valid and employee_valid and item_valid and employee_product_valid:
            with transaction.atomic():
                # Lưu yêu cầu cơ bản
                request_obj = form.save()
                
                # Lưu các formset
                employee_formset.save()
                item_formset.save()
                employee_product_formset.save()
            
            messages.success(request, 'Yêu cầu cấp phát đã được cập nhật thành công.')
            
            if 'save_draft' in request.POST:
                return redirect('inventory_requests:my_requests')
            else:
                # Kiểm tra xem người dùng đã có người quản lý chưa
                if not request.user.manager:
                    messages.error(request, 'Bạn chưa được gán người quản lý. Vui lòng liên hệ quản trị viên để được gán người quản lý trước khi gửi yêu cầu.')
                    return redirect('inventory_requests:inventory_request_edit', request_id=request_obj.id)
                
                if not request.user.manager.email:
                    messages.error(request, 'Người quản lý của bạn chưa có email. Vui lòng liên hệ quản trị viên để cập nhật email cho người quản lý.')
                    return redirect('inventory_requests:inventory_request_edit', request_id=request_obj.id)
                
                # Chuyển trạng thái thành chờ phê duyệt và gửi email
                request_obj.mark_as_pending()
                
                # Gửi email thông báo cho người tạo yêu cầu
                send_template_email(
                    recipient_list=[request.user.email],
                    template_code='request_created',
                    context_data={
                        'request': request_obj,
                        'user': request.user,
                    }
                )
                
                # Gửi email cho người quản lý để phê duyệt
                send_template_email(
                    recipient_list=[request.user.manager.email],
                    template_code='pending_approval',
                    context_data={
                        'request': request_obj,
                        'user': request.user,
                        'manager': request.user.manager,
                    }
                )
                
                messages.success(request, f'Yêu cầu cấp phát đã được gửi đến người quản lý {request.user.manager.get_full_name()} để phê duyệt.')
                return redirect('inventory_requests:my_requests')
        else:
            # Có lỗi validation - hiển thị lỗi
            if not form_valid:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
            
            if not employee_valid:
                messages.error(request, 'Có lỗi trong danh sách nhân viên.')
                
            if not item_valid:
                messages.error(request, 'Có lỗi trong danh sách sản phẩm.')
                
            if not employee_product_valid:
                messages.error(request, 'Có lỗi trong phân bổ sản phẩm cho nhân viên.')
    else:
        form = InventoryRequestForm(instance=request_obj)
        employee_formset = RequestEmployeeFormSet(instance=request_obj)
        item_formset = RequestItemFormSet(instance=request_obj)
        employee_product_formset = EmployeeProductFormSet(instance=request_obj)
    
    context = {
        'form': form,
        'employee_formset': employee_formset,
        'item_formset': item_formset,
        'employee_product_formset': employee_product_formset,
        'request_obj': request_obj,
        'title': 'Chỉnh sửa yêu cầu cấp phát',
        'use_employee_product': True,  # Flag để hiển thị tab phân bổ sản phẩm
    }
    
    return render(request, 'inventory_requests/request_form.html', context)


@login_required
def inventory_request_detail(request, request_id):
    """Xem chi tiết yêu cầu cấp phát"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra quyền xem chi tiết
    can_view = False
    
    # Người tạo yêu cầu có thể xem
    if request_obj.requester == request.user:
        can_view = True
    
    # Người quản lý của người tạo yêu cầu có thể xem
    elif request.user == request_obj.requester.manager:
        can_view = True
    
    # Admin/SM luôn có thể xem
    elif request.user.is_superuser or request.user.role in ['sm', 'admin']:
        can_view = True
    
    # Người quản lý kho có thể xem yêu cầu đã được phê duyệt
    elif request.user.role in ['manager'] and request_obj.status in [
        InventoryRequest.STATUS_APPROVED,
        InventoryRequest.STATUS_SCHEDULED,
        InventoryRequest.STATUS_COMPLETED
    ]:
        can_view = True
        
    if not can_view:
        messages.error(request, 'Bạn không có quyền xem chi tiết yêu cầu này.')
        return redirect('inventory_requests:my_requests')
    
    # Xác định xem người dùng có quyền phê duyệt không
    can_approve = (
        request_obj.status == InventoryRequest.STATUS_PENDING
        and request.user == request_obj.requester.manager
    )
    
    # Kiểm tra xem người dùng hiện tại có phải là quản lý kho không
    is_warehouse_manager = request.user.role in ['sm', 'admin', 'manager']
    
    # Kiểm tra xem yêu cầu có thể lên lịch không
    can_schedule = (
        request_obj.status == InventoryRequest.STATUS_APPROVED
        and is_warehouse_manager
    )
    
    # Kiểm tra xem yêu cầu có thể đánh dấu hoàn thành không
    can_complete = (
        request_obj.status == InventoryRequest.STATUS_SCHEDULED
        and is_warehouse_manager
    )
    
    # Kiểm tra xem có phân bổ sản phẩm cho nhân viên không
    has_employee_products = request_obj.employee_products.exists()
    
    context = {
        'request_obj': request_obj,
        'can_approve': can_approve,
        'can_schedule': can_schedule,
        'can_complete': can_complete,
        'is_warehouse_manager': is_warehouse_manager,
        'has_employee_products': has_employee_products,
        'title': f'Chi tiết yêu cầu cấp phát #{request_obj.request_code}',
    }
    
    return render(request, 'inventory_requests/request_detail.html', context)


@login_required
def inventory_request_delete(request, request_id):
    """Xóa yêu cầu cấp phát"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra quyền xóa
    if request_obj.requester != request.user or not request_obj.can_be_deleted:
        messages.error(request, 'Bạn không có quyền xóa yêu cầu này hoặc yêu cầu không thể xóa.')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    if request.method == 'POST':
        request_obj.delete()
        messages.success(request, 'Yêu cầu cấp phát đã được xóa thành công.')
        return redirect('inventory_requests:my_requests')
    
    context = {
        'request_obj': request_obj,
        'title': f'Xóa yêu cầu cấp phát #{request_obj.request_code}',
    }
    
    return render(request, 'inventory_requests/request_detail.html', context)


@login_required
def inventory_request_submit(request, request_id):
    """Gửi yêu cầu cấp phát để phê duyệt"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra quyền gửi yêu cầu
    if request_obj.requester != request.user or request_obj.status != InventoryRequest.STATUS_DRAFT:
        messages.error(request, 'Bạn không có quyền gửi yêu cầu này hoặc yêu cầu không thể gửi.')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    # Kiểm tra xem người dùng đã có người quản lý chưa
    if not request.user.manager:
        messages.error(request, 'Bạn chưa được gán người quản lý. Vui lòng liên hệ quản trị viên để được gán người quản lý trước khi gửi yêu cầu.')
        return redirect('inventory_requests:inventory_request_edit', request_id=request_obj.id)
    
    if not request.user.manager.email:
        messages.error(request, 'Người quản lý của bạn chưa có email. Vui lòng liên hệ quản trị viên để cập nhật email cho người quản lý.')
        return redirect('inventory_requests:inventory_request_edit', request_id=request_obj.id)
    
    # Kiểm tra xem yêu cầu có ít nhất một phân bổ sản phẩm cho nhân viên không
    if request_obj.employee_products.count() == 0:
        messages.error(request, 'Yêu cầu cần có ít nhất một phân bổ sản phẩm cho nhân viên.')
        return redirect('inventory_requests:inventory_request_edit', request_id=request_obj.id)
    
    # Chuyển trạng thái thành chờ phê duyệt và gửi email
    request_obj.mark_as_pending()
    
    # Gửi email thông báo cho người tạo yêu cầu
    send_template_email(
        recipient_list=[request.user.email],
        template_code='request_created',
        context_data={
            'request': request_obj,
            'user': request.user,
        }
    )
    
    # Gửi email cho người quản lý để phê duyệt
    send_template_email(
        recipient_list=[request.user.manager.email],
        template_code='pending_approval',
        context_data={
            'request': request_obj,
            'user': request.user,
            'manager': request.user.manager,
        }
    )
    
    messages.success(request, f'Yêu cầu cấp phát đã được gửi đến người quản lý {request.user.manager.get_full_name()} để phê duyệt.')
    return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)


@login_required
def inventory_request_approve(request, request_id):
    """Phê duyệt hoặc từ chối yêu cầu cấp phát"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra quyền phê duyệt
    if request.user != request_obj.requester.manager or request_obj.status != InventoryRequest.STATUS_PENDING:
        messages.error(request, 'Bạn không có quyền phê duyệt yêu cầu này hoặc yêu cầu không ở trạng thái chờ phê duyệt.')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    if request.method == 'POST':
        form = RequestApprovalForm(request.POST)
        
        if form.is_valid():
            decision = form.cleaned_data['decision']
            note = form.cleaned_data['note']
            rejection_reason = form.cleaned_data['rejection_reason']
            
            if decision == 'approve':
                # Phê duyệt yêu cầu
                request_obj.approve(request.user, note)
                
                # Gửi email thông báo đã được phê duyệt
                send_template_email(
                    recipient_list=[request_obj.requester.email],
                    template_code='request_approved',
                    context_data={
                        'request': request_obj,
                        'user': request_obj.requester,
                        'approver': request.user,
                    }
                )
                
                messages.success(request, 'Yêu cầu cấp phát đã được phê duyệt.')
            else:
                # Từ chối yêu cầu
                request_obj.reject(request.user, rejection_reason)
                
                # Gửi email thông báo đã bị từ chối
                send_template_email(
                    recipient_list=[request_obj.requester.email],
                    template_code='request_rejected',
                    context_data={
                        'request': request_obj,
                        'user': request_obj.requester,
                        'approver': request.user,
                        'rejection_reason': rejection_reason,
                    }
                )
                
                messages.warning(request, 'Yêu cầu cấp phát đã bị từ chối.')
            
            return redirect('inventory_requests:my_approval_requests')
    else:
        form = RequestApprovalForm()
    
    context = {
        'form': form,
        'request_obj': request_obj,
        'title': f'Phê duyệt yêu cầu cấp phát #{request_obj.request_code}',
    }
    
    return render(request, 'inventory_requests/approve.html', context)


@login_required
@role_required(['sm', 'admin', 'manager'])
def warehouse_requests_list(request):
    """Danh sách yêu cầu cấp phát đã được phê duyệt cho quản lý kho"""
    
    # Lọc các yêu cầu đã được phê duyệt
    requests = InventoryRequest.objects.filter(
        status__in=[
            InventoryRequest.STATUS_APPROVED,
            InventoryRequest.STATUS_SCHEDULED
        ]
    ).order_by('-approval_date')
    
    # Phân loại yêu cầu
    approved_requests = requests.filter(status=InventoryRequest.STATUS_APPROVED)
    scheduled_requests = requests.filter(status=InventoryRequest.STATUS_SCHEDULED)
    
    # Sắp xếp và phân trang
    paginator_approved = Paginator(approved_requests, 10)
    paginator_scheduled = Paginator(scheduled_requests, 10)
    
    page_approved = request.GET.get('page_approved')
    page_scheduled = request.GET.get('page_scheduled')
    
    approved_requests = paginator_approved.get_page(page_approved)
    scheduled_requests = paginator_scheduled.get_page(page_scheduled)
    
    context = {
        'approved_requests': approved_requests,
        'scheduled_requests': scheduled_requests,
        'title': 'Quản lý cấp phát vật tư',
    }
    
    return render(request, 'inventory_requests/warehouse_requests.html', context)


@login_required
@role_required(['sm', 'admin', 'manager'])
def inventory_request_schedule(request, request_id):
    """Lên lịch cấp phát cho yêu cầu"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra xem yêu cầu có thể lên lịch không
    if request_obj.status != InventoryRequest.STATUS_APPROVED:
        messages.error(request, 'Yêu cầu này không thể lên lịch cấp phát.')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    if request.method == 'POST':
        form = RequestScheduleForm(request.POST)
        
        if form.is_valid():
            scheduled_date = form.cleaned_data['scheduled_date']
            note = form.cleaned_data['note']
            
            # Lên lịch cấp phát
            request_obj.schedule(request.user, scheduled_date)
            
            if note:
                request_obj.notes = (request_obj.notes or '') + f"\n\nGhi chú lên lịch ({timezone.now().strftime('%Y-%m-%d %H:%M')}): {note}"
                request_obj.save()
            
            # Gửi email thông báo đã lên lịch
            send_template_email(
                recipient_list=[request_obj.requester.email],
                template_code='warehouse_scheduled',
                context_data={
                    'request': request_obj,
                    'user': request_obj.requester,
                    'warehouse_manager': request.user,
                    'scheduled_date': scheduled_date,
                }
            )
            
            messages.success(request, 'Yêu cầu đã được lên lịch cấp phát thành công.')
            return redirect('inventory_requests:warehouse_requests_list')
    else:
        # Mặc định là ngày mai
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        form = RequestScheduleForm(initial={'scheduled_date': tomorrow})
    
    context = {
        'form': form,
        'request_obj': request_obj,
        'title': f'Lên lịch cấp phát cho yêu cầu #{request_obj.request_code}',
    }
    
    return render(request, 'inventory_requests/schedule.html', context)


@login_required
@role_required(['sm', 'admin', 'manager'])
def inventory_request_complete(request, request_id):
    """Đánh dấu hoàn thành yêu cầu cấp phát"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra xem yêu cầu có thể đánh dấu hoàn thành không
    if request_obj.status != InventoryRequest.STATUS_SCHEDULED:
        messages.error(request, 'Yêu cầu này không thể đánh dấu hoàn thành.')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    if request.method == 'POST':
        form = RequestCompletionForm(request.POST, request=request_obj)
        
        if form.is_valid():
            note = form.cleaned_data['note']
            
            with transaction.atomic():
                # Cập nhật số lượng đã cấp phát cho từng sản phẩm
                for item in request_obj.items.all():
                    field_name = f'issued_quantity_{item.id}'
                    issued_quantity = form.cleaned_data.get(field_name, 0)
                    
                    if issued_quantity > 0:
                        # Cập nhật số lượng đã cấp phát
                        item.issued_quantity = issued_quantity
                        item.save()
                        
                        # Giảm số lượng tồn kho
                        product = item.product
                        product.current_quantity -= issued_quantity
                        product.save()
                
                # Đánh dấu hoàn thành yêu cầu
                request_obj.complete()
                
                if note:
                    request_obj.notes = (request_obj.notes or '') + f"\n\nGhi chú hoàn thành ({timezone.now().strftime('%Y-%m-%d %H:%M')}): {note}"
                    request_obj.save()
            
            # Gửi email thông báo đã hoàn thành
            send_template_email(
                recipient_list=[request_obj.requester.email],
                template_code='request_completed',
                context_data={
                    'request': request_obj,
                    'user': request_obj.requester,
                    'warehouse_manager': request.user,
                }
            )
            
            messages.success(request, 'Yêu cầu đã được đánh dấu hoàn thành thành công.')
            return redirect('inventory_requests:warehouse_requests_list')
    else:
        form = RequestCompletionForm(request=request_obj)
    
    context = {
        'form': form,
        'request_obj': request_obj,
        'title': f'Hoàn thành yêu cầu cấp phát #{request_obj.request_code}',
    }
    
    return render(request, 'inventory_requests/complete.html', context)
