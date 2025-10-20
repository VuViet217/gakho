from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from django.template.loader import render_to_string
import logging
from io import BytesIO
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.conf import settings
import os

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
    """Danh sách tất cả các yêu cầu cấp phát (không bao gồm bản nháp) - Tất cả người dùng đều thấy"""
    
    # Tất cả người dùng đều thấy tất cả yêu cầu đã submit (trừ draft)
    requests = InventoryRequest.objects.exclude(status='draft').order_by('-created_at')
    
    # Phân trang
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
    
    # Lấy danh sách nhân viên dưới quyền (những người có mình là manager)
    subordinates = request.user.subordinates.all()
    
    # Nếu không có nhân viên dưới quyền, thông báo
    if not subordinates.exists():
        messages.info(request, 'Bạn chưa có nhân viên nào dưới quyền cần phê duyệt.')
    
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
        'subordinates_count': subordinates.count(),
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
                
                # Chuẩn bị danh sách CC (manager của người tạo yêu cầu)
                cc_list = []
                if request_obj.requester.manager and request_obj.requester.manager.email:
                    cc_list.append(request_obj.requester.manager.email)
                
                # Gửi email thông báo đã được phê duyệt cho người tạo yêu cầu (CC manager)
                try:
                    send_template_email(
                        recipient_list=[request_obj.requester.email],
                        template_code='request_approved',
                        context_data={
                            'request': request_obj,
                            'user': request_obj.requester,
                            'approver': request.user,
                        },
                        cc_list=cc_list if cc_list else None
                    )
                except Exception as e:
                    logger.error(f"Lỗi gửi email phê duyệt cho người tạo yêu cầu: {e}")
                
                # Gửi email thông báo cho quản lý kho (SM/Admin) để xử lý xuất kho
                from accounts.models import User
                warehouse_managers = User.objects.filter(
                    role__in=['sm', 'admin'],
                    is_active=True,
                    email__isnull=False
                ).exclude(email='')
                
                warehouse_manager_emails = [wm.email for wm in warehouse_managers]
                
                if warehouse_manager_emails:
                    try:
                        send_template_email(
                            recipient_list=warehouse_manager_emails,
                            template_code='warehouse_approval_required',
                            context_data={
                                'request': request_obj,
                                'user': warehouse_managers.first(),  # User đại diện cho email
                                'approver': request.user,
                            }
                        )
                    except Exception as e:
                        logger.error(f"Lỗi gửi email cho quản lý kho: {e}")
                
                messages.success(request, 'Yêu cầu cấp phát đã được phê duyệt.')
            else:
                # Từ chối yêu cầu
                request_obj.reject(request.user, rejection_reason)
                
                # Chuẩn bị danh sách CC (manager của người tạo yêu cầu)
                cc_list = []
                if request_obj.requester.manager and request_obj.requester.manager.email:
                    cc_list.append(request_obj.requester.manager.email)
                
                # Gửi email thông báo đã bị từ chối (CC manager)
                try:
                    send_template_email(
                        recipient_list=[request_obj.requester.email],
                        template_code='request_rejected',
                        context_data={
                            'request': request_obj,
                            'user': request_obj.requester,
                            'approver': request.user,
                            'rejection_reason': rejection_reason,
                        },
                        cc_list=cc_list if cc_list else None
                    )
                except Exception as e:
                    logger.error(f"Lỗi gửi email từ chối yêu cầu: {e}")
                
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
def inventory_request_reject(request, request_id):
    """Từ chối yêu cầu cấp phát"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Kiểm tra quyền từ chối
    if request.user != request_obj.requester.manager or request_obj.status != InventoryRequest.STATUS_PENDING:
        messages.error(request, 'Bạn không có quyền từ chối yêu cầu này hoặc yêu cầu không ở trạng thái chờ phê duyệt.')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        
        if rejection_reason:
            # Từ chối yêu cầu
            request_obj.reject(request.user, rejection_reason)
            
            # Chuẩn bị danh sách CC (manager của người tạo yêu cầu)
            cc_list = []
            if request_obj.requester.manager and request_obj.requester.manager.email:
                cc_list.append(request_obj.requester.manager.email)
            
            # Gửi email thông báo đã bị từ chối (không làm gián đoạn nếu lỗi)
            try:
                send_template_email(
                    recipient_list=[request_obj.requester.email],
                    template_code='request_rejected',
                    context_data={
                        'request': request_obj,
                        'user': request_obj.requester,
                        'approver': request.user,
                        'rejection_reason': rejection_reason,
                    },
                    cc_list=cc_list if cc_list else None
                )
            except Exception as e:
                logger.error(f"Không thể gửi email thông báo từ chối: {str(e)}")
            
            messages.warning(request, 'Yêu cầu cấp phát đã bị từ chối.')
        else:
            messages.error(request, 'Vui lòng nhập lý do từ chối.')
            return redirect('inventory_requests:my_approval_requests')
    
    return redirect('inventory_requests:my_approval_requests')


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
            
            # Kiểm tra tồn kho trước khi lên lịch
            insufficient_products = []
            for employee_product in request_obj.employee_products.all():
                product = employee_product.product
                requested_quantity = employee_product.quantity
                available_quantity = product.current_quantity
                
                if requested_quantity > available_quantity:
                    insufficient_products.append({
                        'product': product,
                        'requested': requested_quantity,
                        'available': available_quantity,
                        'shortage': requested_quantity - available_quantity
                    })
            
            # Nếu có sản phẩm không đủ tồn kho
            if insufficient_products:
                for item in insufficient_products:
                    messages.error(
                        request,
                        f'Không đủ tồn kho cho sản phẩm "{item["product"].name}" '
                        f'(Mã: {item["product"].product_code}). '
                        f'Yêu cầu: {item["requested"]}, '
                        f'Tồn kho: {item["available"]}, '
                        f'Thiếu: {item["shortage"]}'
                    )
                
                # Trả về form với thông báo lỗi
                context = {
                    'form': form,
                    'request_obj': request_obj,
                    'insufficient_products': insufficient_products,
                    'title': f'Lên lịch cấp phát cho yêu cầu #{request_obj.request_code}',
                }
                return render(request, 'inventory_requests/schedule.html', context)
            
            # Nếu đủ tồn kho, tiếp tục lên lịch
            request_obj.schedule(request.user, scheduled_date)
            
            if note:
                request_obj.schedule_notes = note
                request_obj.save()
            
            # Chuẩn bị danh sách CC: quản lý của người yêu cầu + quản lý kho
            cc_list = []
            if request_obj.requester.manager and request_obj.requester.manager.email:
                cc_list.append(request_obj.requester.manager.email)
            if request.user.email:
                cc_list.append(request.user.email)
            
            # Gửi email thông báo đã lên lịch
            try:
                send_template_email(
                    recipient_list=[request_obj.requester.email],
                    template_code='warehouse_scheduled',
                    context_data={
                        'request': request_obj,
                        'user': request_obj.requester,
                        'warehouse_manager': request.user,
                        'scheduled_date': scheduled_date,
                        'schedule_notes': note,
                    },
                    cc_list=cc_list
                )
            except Exception as e:
                # Log error nhưng không làm gián đoạn quy trình
                print(f"Error sending email: {e}")
            
            messages.success(request, 'Yêu cầu đã được lên lịch cấp phát thành công.')
            return redirect('inventory_requests:warehouse_requests_list')
    else:
        # Mặc định là ngày mai lúc 8h sáng
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        tomorrow = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
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
        # Lấy note từ form
        note = request.POST.get('note', '')
        
        # Thu thập dữ liệu số lượng cấp phát
        issued_data = []
        
        with transaction.atomic():
            # Cập nhật số lượng đã cấp phát cho từng employee_product
            for employee_product in request_obj.employee_products.all():
                field_name = f'issued_quantity_{employee_product.id}'
                issued_quantity = int(request.POST.get(field_name, 0))
                
                if issued_quantity > 0:
                    # Giảm số lượng tồn kho
                    product = employee_product.product
                    product.current_quantity -= issued_quantity
                    product.save()
                    
                    # Lưu thông tin để in phiếu xuất
                    issued_data.append({
                        'employee': employee_product.employee,
                        'product': employee_product.product,
                        'requested_quantity': employee_product.quantity,
                        'issued_quantity': issued_quantity,
                    })
            
            # Đánh dấu hoàn thành yêu cầu
            request_obj.complete()
            
            if note:
                request_obj.notes = (request_obj.notes or '') + f"\n\nGhi chú hoàn thành ({timezone.now().strftime('%Y-%m-%d %H:%M')}): {note}"
                request_obj.save()
        
        # Lưu dữ liệu vào session để dùng cho PDF
        request.session['issued_data'] = {
            'request_id': request_obj.id,
            'request_code': request_obj.request_code,
            'requester': request_obj.requester.get_full_name(),
            'warehouse_manager': request.user.get_full_name(),
            'completed_date': timezone.now().strftime('%d/%m/%Y %H:%M'),
            'items': [
                {
                    'employee_code': item['employee'].employee_id,
                    'employee_name': item['employee'].full_name,
                    'employee_dept': item['employee'].department.code if item['employee'].department else 'N/A',
                    'product_code': item['product'].product_code,
                    'product_name': item['product'].name,
                    'requested_quantity': item['requested_quantity'],
                    'issued_quantity': item['issued_quantity'],
                }
                for item in issued_data
            ]
        }
        
        messages.success(request, 'Yêu cầu đã được đánh dấu hoàn thành thành công.')
        
        # Gửi email thông báo hoàn thành
        try:
            # Email context
            email_context = {
                'request_code': request_obj.request_code,
                'requester_name': request_obj.requester.get_full_name(),
                'title': request_obj.title,
                'completed_date': timezone.now().strftime('%d/%m/%Y %H:%M'),
                'warehouse_manager': request.user.get_full_name(),
                'note': note if note else 'Không có ghi chú',
                'detail_url': request.build_absolute_uri(
                    reverse('inventory_requests:inventory_request_detail', args=[request_obj.id])
                ),
            }
            
            # Danh sách CC
            cc_list = []
            
            # Thêm quản lý của người tạo yêu cầu (nếu có)
            if hasattr(request_obj.requester, 'manager') and request_obj.requester.manager:
                cc_list.append(request_obj.requester.manager.email)
            
            # Thêm quản lý kho
            cc_list.append(request.user.email)
            
            # Loại bỏ email trùng
            cc_list = list(set(filter(None, cc_list)))
            
            send_template_email(
                recipient_list=[request_obj.requester.email],
                template_code='request_completed',
                context_data=email_context,
                cc_list=cc_list
            )
        except Exception as e:
            logger.error(f"Error sending completion email for request {request_obj.request_code}: {str(e)}")
        
        # Chuyển hướng về chi tiết yêu cầu (không tự động in)
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)
    
    context = {
        'request_obj': request_obj,
        'title': f'Hoàn thành yêu cầu cấp phát #{request_obj.request_code}',
    }
    
    return render(request, 'inventory_requests/complete.html', context)


@login_required
@role_required(['sm', 'admin', 'manager'])
def print_delivery_note(request, request_id):
    """In phiếu xuất kho A5"""
    
    request_obj = get_object_or_404(InventoryRequest, id=request_id)
    
    # Lấy dữ liệu từ session (nếu mới hoàn thành)
    issued_data = request.session.get('issued_data', None)
    
    # Nếu không có trong session, lấy từ database
    if not issued_data or issued_data.get('request_id') != request_obj.id:
        issued_data = {
            'request_code': request_obj.request_code,
            'requester': request_obj.requester.get_full_name(),
            'warehouse_manager': request.user.get_full_name(),
            'completed_date': request_obj.completed_date.strftime('%d/%m/%Y %H:%M') if request_obj.completed_date else timezone.now().strftime('%d/%m/%Y %H:%M'),
            'items': [
                {
                    'employee_code': ep.employee.employee_id,
                    'employee_name': ep.employee.full_name,
                    'employee_dept': ep.employee.department.code if ep.employee.department else 'N/A',
                    'product_code': ep.product.product_code,
                    'product_name': ep.product.name,
                    'requested_quantity': ep.quantity,
                    'issued_quantity': ep.quantity,  # Giả định đã cấp đủ
                }
                for ep in request_obj.employee_products.all()
            ]
        }
    
    context = {
        'request_obj': request_obj,
        'issued_data': issued_data,
    }
    
    # Tạo PDF với ReportLab
    try:
        # Đăng ký font Arial hỗ trợ tiếng Việt
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial.ttf')
        font_bold_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial-Bold.ttf')
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdfmetrics.registerFont(TTFont('Arial-Bold', font_bold_path))
        
        # Tạo buffer để lưu PDF
        buffer = BytesIO()
        
        # Tạo PDF A5 ngang (landscape)
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A5),
            rightMargin=10*mm,
            leftMargin=10*mm,
            topMargin=10*mm,
            bottomMargin=10*mm
        )
        
        # Danh sách các elements để thêm vào PDF
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Tiêu đề chính - sử dụng font Arial
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Arial-Bold'
        )
        
        # Tiêu đề
        elements.append(Paragraph('PHIẾU XUẤT KHO', title_style))
        elements.append(Spacer(1, 5*mm))
        
        # Thông tin yêu cầu - Sử dụng text đơn giản thay vì Paragraph
        info_data = [
            ['Mã yêu cầu:', issued_data['request_code'], 'Ngày hoàn thành:', issued_data['completed_date']],
            ['Người yêu cầu:', issued_data['requester'], 'Thủ kho:', issued_data['warehouse_manager']],
        ]
        
        info_table = Table(info_data, colWidths=[30*mm, 60*mm, 30*mm, 60*mm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Arial-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Arial-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 5*mm))
        
        # Bảng sản phẩm
        product_data = [
            ['STT', 'Mã NV', 'Nhân viên', 'BP', 'Mã SP', 'Tên sản phẩm', 'SL yêu cầu', 'SL cấp phát']
        ]
        
        # Style cho Paragraph trong bảng
        cell_style = ParagraphStyle(
            'CellStyle',
            parent=styles['Normal'],
            fontSize=8,
            fontName='Arial',
            leading=10
        )
        
        for idx, item in enumerate(issued_data['items'], 1):
            product_data.append([
                str(idx),
                Paragraph(item.get('employee_code', ''), cell_style),
                Paragraph(item['employee_name'], cell_style),
                Paragraph(item['employee_dept'], cell_style),
                Paragraph(item['product_code'], cell_style),
                Paragraph(item['product_name'], cell_style),
                str(item['requested_quantity']),
                str(item['issued_quantity'])
            ])
        
        product_table = Table(product_data, colWidths=[8*mm, 15*mm, 30*mm, 12*mm, 18*mm, 42*mm, 16*mm, 16*mm])
        product_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # STT
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Mã NV
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Bộ phận
            ('ALIGN', (6, 1), (-1, -1), 'CENTER'),  # Số lượng
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Căn trên
            
            # Borders
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(product_table)
        elements.append(Spacer(1, 10*mm))
        
        # Chữ ký
        signature_data = [
            ['Người lập phiếu', 'Người nhận hàng', 'Thủ kho'],
            ['(Ký, ghi rõ họ tên)', '(Ký, ghi rõ họ tên)', '(Ký, ghi rõ họ tên)'],
            ['', '', ''],
            ['', '', ''],
            ['', '', ''],
        ]
        
        signature_table = Table(signature_data, colWidths=[60*mm, 60*mm, 60*mm])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 2),
        ]))
        
        elements.append(signature_table)
        
        # Build PDF
        doc.build(elements)
        
        # Lấy giá trị PDF từ buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        # Trả về PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="phieu_xuat_kho_{request_obj.request_code}.pdf"'
        
        # Xóa dữ liệu khỏi session
        if 'issued_data' in request.session:
            del request.session['issued_data']
        
        return response
    except Exception as e:
        messages.error(request, f'Lỗi khi tạo PDF: {str(e)}')
        return redirect('inventory_requests:inventory_request_detail', request_id=request_obj.id)


@login_required
def employee_delivery_history(request):
    """Lịch sử giao nhận của nhân viên"""
    from employees.models import Employee
    
    # Lấy tham số tìm kiếm
    search_query = request.GET.get('search', '').strip()
    employee_id = request.GET.get('employee_id', '')
    
    # Khởi tạo biến
    employee = None
    delivery_history = []
    
    # Nếu có tìm kiếm
    if search_query:
        # Tìm nhân viên theo mã hoặc tên
        employees = Employee.objects.filter(
            Q(employee_id__icontains=search_query) | 
            Q(full_name__icontains=search_query)
        )
        
        if employees.count() == 1:
            # Nếu tìm thấy đúng 1 nhân viên
            employee = employees.first()
            employee_id = employee.id
        elif employees.count() > 1:
            # Nếu tìm thấy nhiều nhân viên, hiển thị danh sách để chọn
            context = {
                'title': 'Lịch sử giao nhận nhân viên',
                'search_query': search_query,
                'employees': employees,
            }
            return render(request, 'inventory_requests/employee_delivery_history.html', context)
        else:
            messages.warning(request, f'Không tìm thấy nhân viên với từ khóa: {search_query}')
    
    # Nếu đã chọn nhân viên cụ thể
    if employee_id:
        try:
            employee = Employee.objects.get(id=employee_id)
            
            # Lấy lịch sử giao nhận: Tất cả EmployeeProductRequest của nhân viên này 
            # trong các yêu cầu đã hoàn thành
            employee_products = EmployeeProductRequest.objects.filter(
                employee=employee,
                request__status=InventoryRequest.STATUS_COMPLETED
            ).select_related(
                'request', 'product', 'request__requester'
            ).order_by('-request__completed_date')
            
            # Xây dựng danh sách lịch sử
            for ep in employee_products:
                delivery_history.append({
                    'request_code': ep.request.request_code,
                    'request_id': ep.request.id,
                    'request_title': ep.request.title,
                    'completed_date': ep.request.completed_date,
                    'product_code': ep.product.product_code,
                    'product_name': ep.product.name,
                    'quantity': ep.quantity,
                    'requester': ep.request.requester.get_full_name() if ep.request.requester else 'N/A',
                })
                
        except Employee.DoesNotExist:
            messages.error(request, 'Không tìm thấy nhân viên.')
    
    # Phân trang
    paginator = Paginator(delivery_history, 20)
    page = request.GET.get('page')
    delivery_history_page = paginator.get_page(page)
    
    context = {
        'title': 'Lịch sử giao nhận nhân viên',
        'employee': employee,
        'delivery_history': delivery_history_page,
        'search_query': search_query,
    }
    
    return render(request, 'inventory_requests/employee_delivery_history.html', context)
