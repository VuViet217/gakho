from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
import logging

from system_settings.models import EmailTemplate
from system_settings.forms import EmailTemplateForm, EmailTemplateTestForm
from system_settings.utils import extract_variables_from_template, render_email_template
from system_settings.template_email_service import send_template_email

logger = logging.getLogger(__name__)

# Hàm kiểm tra quyền admin - giống với file views.py
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role in ['sm', 'admin'])

@login_required
@user_passes_test(is_admin)
def email_template_list(request):
    """
    Hiển thị danh sách các mẫu email
    """
    templates = EmailTemplate.objects.all().order_by('type', 'name')
    
    # Nhóm template theo loại để hiển thị
    template_groups = {}
    for template in templates:
        type_name = template.get_type_display()
        if type_name not in template_groups:
            template_groups[type_name] = []
        template_groups[type_name].append(template)
    
    return render(request, 'system_settings/email_templates/list.html', {
        'template_groups': template_groups,
        'title': 'Quản lý mẫu email',
        'hide_header_title': True,  # Thêm biến flag để ẩn tiêu đề trong header
        'hide_breadcrumb': True,  # Thêm biến flag để ẩn breadcrumb
    })

@login_required
@user_passes_test(is_admin)
def email_template_create(request):
    """
    Tạo mới mẫu email
    """
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo mới mẫu email thành công!')
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm()
    
    return render(request, 'system_settings/email_templates/form.html', {
        'form': form,
        'title': 'Thêm mẫu email mới',
        'is_new': True,
    })

@login_required
@user_passes_test(is_admin)
def email_template_edit(request, template_id):
    """
    Chỉnh sửa mẫu email
    """
    template = get_object_or_404(EmailTemplate, id=template_id)
    
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật mẫu email thành công!')
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm(instance=template)
    
    return render(request, 'system_settings/email_templates/form.html', {
        'form': form,
        'template': template,
        'title': f'Chỉnh sửa mẫu: {template.name}',
        'is_new': False,
    })

@login_required
@user_passes_test(is_admin)
def email_template_delete(request, template_id):
    """
    Xóa mẫu email
    """
    template = get_object_or_404(EmailTemplate, id=template_id)
    
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Đã xóa mẫu email thành công!')
        return redirect('email_template_list')
    
    return render(request, 'system_settings/email_templates/delete.html', {
        'template': template,
        'title': f'Xóa mẫu: {template.name}',
    })

@login_required
@user_passes_test(is_admin)
def email_template_test(request, template_id):
    """
    Test gửi email với mẫu đã chọn
    """
    template = get_object_or_404(EmailTemplate, id=template_id)
    
    # Khởi tạo dữ liệu test mặc định từ variables trong template
    default_test_data = {}
    for var, default_value in template.variables.items():
        if not default_value:
            default_test_data[var] = f'[Giá trị mẫu cho {var}]'
        else:
            default_test_data[var] = default_value
    
    if request.method == 'POST':
        form = EmailTemplateTestForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            
            # Parse dữ liệu test
            try:
                test_data_str = form.cleaned_data['test_data']
                if not test_data_str:
                    test_data = default_test_data
                else:
                    test_data = json.loads(test_data_str)
            except json.JSONDecodeError:
                messages.error(request, 'Dữ liệu test không hợp lệ. Vui lòng kiểm tra định dạng JSON.')
                test_data = default_test_data
            
            # Render mẫu email và gửi test
            subject, html_content, text_content = render_email_template(template.code, test_data)
            
            if not subject or not html_content:
                messages.error(request, 'Không thể render mẫu email. Vui lòng kiểm tra cú pháp.')
            else:
                # Gửi email test
                success, msg = send_template_email(recipient, template.code, test_data)
                
                if success:
                    messages.success(request, f'Gửi email test thành công đến {recipient}!')
                else:
                    messages.error(request, f'Lỗi khi gửi email: {msg}')
                
            return redirect('email_template_test', template_id=template.id)
    else:
        initial_data = {'test_data': json.dumps(default_test_data, indent=2, ensure_ascii=False)}
        form = EmailTemplateTestForm(initial=initial_data)
    
    # Render mẫu với dữ liệu mặc định để hiển thị preview
    subject, html_preview, _ = render_email_template(template.code, default_test_data)
    
    return render(request, 'system_settings/email_templates/test.html', {
        'form': form,
        'template': template,
        'title': f'Test mẫu: {template.name}',
        'preview_subject': subject or 'Không thể render tiêu đề',
        'preview_content': html_preview or 'Không thể render nội dung',
        'available_variables': list(template.variables.keys()),
    })
    
@require_POST
@login_required
@user_passes_test(is_admin)
def get_template_variables(request):
    """
    API để lấy các biến trong nội dung mẫu email
    Sử dụng cho việc cập nhật form động khi người dùng thay đổi nội dung template
    """
    try:
        data = json.loads(request.body)
        content = data.get('content', '')
        variables = extract_variables_from_template(content)
        return JsonResponse({
            'success': True,
            'variables': variables
        })
    except Exception as e:
        logger.error(f"Lỗi khi trích xuất biến từ template: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)