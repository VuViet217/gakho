from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Department, Employee

@login_required
def employee_list_new(request):
    search_query = request.GET.get('search', '')
    department_id = request.GET.get('department', '')
    status = request.GET.get('status', '')
    
    employees = Employee.objects.all()
    
    # Tìm kiếm
    if search_query:
        employees = employees.filter(
            Q(employee_id__icontains=search_query) | 
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) | 
            Q(full_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Lọc theo bộ phận
    if department_id:
        employees = employees.filter(department_id=department_id)
    
    # Lọc theo trạng thái
    if status:
        employees = employees.filter(status=(status == 'active'))
    
    # Phân trang
    paginator = Paginator(employees, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Danh sách bộ phận cho bộ lọc
    departments = Department.objects.all()
    
    context = {
        'page_obj': page_obj,
        'departments': departments,
        'search_query': search_query,
        'selected_department': department_id,
        'selected_status': status,
        'title': 'Danh sách nhân viên (New)'
    }
    return render(request, 'employees/employee_list_new.html', context)