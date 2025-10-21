from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from inventory_requests.models import InventoryRequest, EmployeeProductRequest

@login_required
@user_passes_test(lambda u: u.is_superuser)
def fix_issued_quantity(request):
    """Fix issued_quantity for completed requests"""
    
    if request.method == 'POST':
        # Lấy tất cả yêu cầu đã hoàn thành
        completed_requests = InventoryRequest.objects.filter(status='completed')
        
        updated_count = 0
        details = []
        
        for req in completed_requests:
            for ep in req.employee_products.all():
                # Nếu issued_quantity = 0 hoặc None, cập nhật = approved_quantity (hoặc quantity)
                if ep.issued_quantity == 0 or ep.issued_quantity is None:
                    old_value = ep.issued_quantity
                    ep.issued_quantity = ep.approved_quantity if ep.approved_quantity else ep.quantity
                    ep.save()
                    
                    details.append(f"{req.request_code} - {ep.product.name}: {old_value} → {ep.issued_quantity}")
                    updated_count += 1
        
        if updated_count > 0:
            messages.success(request, f'Đã cập nhật {updated_count} employee_product. Refresh dashboard để xem biểu đồ!')
        else:
            messages.info(request, 'Tất cả issued_quantity đã được cập nhật.')
        
        return render(request, 'admin/fix_issued_result.html', {
            'updated_count': updated_count,
            'details': details
        })
    
    # Hiển thị form xác nhận
    completed_requests = InventoryRequest.objects.filter(status='completed')
    zero_issued = EmployeeProductRequest.objects.filter(
        request__status='completed',
        issued_quantity=0
    ).count()
    
    return render(request, 'admin/fix_issued_confirm.html', {
        'completed_count': completed_requests.count(),
        'zero_issued_count': zero_issued
    })
