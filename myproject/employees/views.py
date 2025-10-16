from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from import_export.formats import base_formats
from tablib import Dataset
from django import forms
from .models import Department, Employee
from .forms import DepartmentForm, EmployeeForm, ImportForm
from .admin import DepartmentResource, EmployeeResource
from .views_new import employee_list_new


# Department Views
@login_required
def department_list(request):
    search_query = request.GET.get('search', '')
    departments = Department.objects.all()
    
    if search_query:
        departments = departments.filter(
            Q(code__icontains=search_query) | 
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(departments, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'title': 'Danh sách bộ phận'
    }
    return render(request, 'employees/department_list.html', context)


@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bộ phận đã được tạo thành công!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'employees/department_form.html', {
        'form': form,
        'title': 'Thêm bộ phận mới'
    })


@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bộ phận đã được cập nhật thành công!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'employees/department_form.html', {
        'form': form,
        'department': department,
        'title': 'Cập nhật bộ phận'
    })


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        try:
            department.delete()
            messages.success(request, 'Bộ phận đã được xóa thành công!')
        except Exception as e:
            messages.error(request, f'Không thể xóa bộ phận này. Lỗi: {str(e)}')
        return redirect('department_list')
    
    return render(request, 'employees/department_confirm_delete.html', {
        'department': department,
        'title': 'Xóa bộ phận'
    })


# Employee Views
@login_required
def employee_list(request):
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
        'title': 'Danh sách nhân viên'
    }
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_create(request):
    class SimpleEmployeeForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = ['employee_id', 'first_name', 'last_name', 'department']
    
    if request.method == 'POST':
        form = SimpleEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nhân viên đã được tạo thành công!')
            return redirect('employee_list')
    else:
        form = SimpleEmployeeForm()
    
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Thêm nhân viên mới'
    })


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    class SimpleEmployeeForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = ['employee_id', 'first_name', 'last_name', 'department']
    
    if request.method == 'POST':
        form = SimpleEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nhân viên đã được cập nhật thành công!')
            return redirect('employee_list')
    else:
        form = SimpleEmployeeForm(instance=employee)
    
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'employee': employee,
        'title': 'Cập nhật thông tin nhân viên'
    })


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'title': f'Thông tin nhân viên: {employee.full_name}'
    })


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        try:
            employee.delete()
            messages.success(request, 'Nhân viên đã được xóa thành công!')
        except Exception as e:
            messages.error(request, f'Không thể xóa nhân viên này. Lỗi: {str(e)}')
        return redirect('employee_list')
    
    return render(request, 'employees/employee_confirm_delete.html', {
        'employee': employee,
        'title': 'Xóa nhân viên'
    })


# Import/Export Views
@login_required
def import_employees(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = EmployeeResource()
            dataset = Dataset()
            import_file = request.FILES['import_file']
            
            file_format = base_formats.XLSX
            if import_file.name.endswith('.csv'):
                file_format = base_formats.CSV
            elif import_file.name.endswith('.xls'):
                file_format = base_formats.XLS
            
            imported_data = dataset.load(import_file.read(), format=file_format.get_title())
            result = resource.import_data(dataset, dry_run=True)  # Test import
            
            if not result.has_errors():
                resource.import_data(dataset, dry_run=False)  # Actual import
                messages.success(request, f'Đã nhập thành công {len(result.rows)} nhân viên!')
                return redirect('employee_list')
            else:
                messages.error(request, f'Có lỗi xảy ra khi nhập dữ liệu: {result.errors}')
    else:
        form = ImportForm()
    
    return render(request, 'employees/import.html', {
        'form': form,
        'title': 'Nhập danh sách nhân viên'
    })


@login_required
def export_employees(request):
    format_param = request.GET.get('format', 'xlsx')
    
    resource = EmployeeResource()
    dataset = resource.export()
    
    if format_param == 'csv':
        file_format = base_formats.CSV()
        response = file_format.export_response(dataset, 'danh_sach_nhan_vien')
    elif format_param == 'xls':
        file_format = base_formats.XLS()
        response = file_format.export_response(dataset, 'danh_sach_nhan_vien')
    else:  # Default: xlsx
        file_format = base_formats.XLSX()
        response = file_format.export_response(dataset, 'danh_sach_nhan_vien')
    
    return response


@login_required
def import_departments(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = DepartmentResource()
            dataset = Dataset()
            import_file = request.FILES['import_file']
            
            file_format = base_formats.XLSX
            if import_file.name.endswith('.csv'):
                file_format = base_formats.CSV
            elif import_file.name.endswith('.xls'):
                file_format = base_formats.XLS
            
            imported_data = dataset.load(import_file.read(), format=file_format.get_title())
            result = resource.import_data(dataset, dry_run=True)  # Test import
            
            if not result.has_errors():
                resource.import_data(dataset, dry_run=False)  # Actual import
                messages.success(request, f'Đã nhập thành công {len(result.rows)} bộ phận!')
                return redirect('department_list')
            else:
                messages.error(request, f'Có lỗi xảy ra khi nhập dữ liệu: {result.errors}')
    else:
        form = ImportForm()
    
    return render(request, 'employees/import.html', {
        'form': form,
        'title': 'Nhập danh sách bộ phận'
    })


@login_required
def export_departments(request):
    format_param = request.GET.get('format', 'xlsx')
    
    resource = DepartmentResource()
    dataset = resource.export()
    
    if format_param == 'csv':
        file_format = base_formats.CSV()
        response = file_format.export_response(dataset, 'danh_sach_bo_phan')
    elif format_param == 'xls':
        file_format = base_formats.XLS()
        response = file_format.export_response(dataset, 'danh_sach_bo_phan')
    else:  # Default: xlsx
        file_format = base_formats.XLSX()
        response = file_format.export_response(dataset, 'danh_sach_bo_phan')
    
    return response
