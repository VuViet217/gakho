import logging
import re
from django.template import Template, Context
from django.utils.html import strip_tags
from system_settings.models import EmailTemplate

logger = logging.getLogger(__name__)

def get_template_by_code(template_code):
    """
    Lấy mẫu email theo mã.
    
    Args:
        template_code: Mã mẫu email
        
    Returns:
        EmailTemplate hoặc None nếu không tìm thấy
    """
    try:
        return EmailTemplate.objects.get(code=template_code, is_active=True)
    except EmailTemplate.DoesNotExist:
        logger.error(f"Không tìm thấy mẫu email với mã: {template_code}")
        return None

def render_email_template(template_code, context_data=None):
    """
    Render mẫu email với dữ liệu context.
    
    Args:
        template_code: Mã mẫu email
        context_data: Dict chứa dữ liệu để render vào mẫu
        
    Returns:
        tuple: (subject, html_content, text_content) hoặc (None, None, None) nếu có lỗi
    """
    if context_data is None:
        context_data = {}
    
    template = get_template_by_code(template_code)
    if not template:
        return None, None, None
    
    try:
        # Render subject
        subject_template = Template(template.subject)
        subject = subject_template.render(Context(context_data))
        
        # Render content
        content_template = Template(template.content)
        html_content = content_template.render(Context(context_data))
        
        # Tạo phiên bản text nếu cần
        text_content = strip_tags(html_content) if template.is_html else html_content
        
        return subject, html_content, text_content
    
    except Exception as e:
        logger.error(f"Lỗi khi render mẫu email {template_code}: {str(e)}")
        return None, None, None

def extract_variables_from_template(template_content):
    """
    Trích xuất các biến từ một nội dung mẫu.
    
    Args:
        template_content: Nội dung mẫu cần phân tích
        
    Returns:
        list: Danh sách tên các biến tìm thấy
    """
    pattern = r'{{\s*(\w+)\s*}}'
    matches = re.findall(pattern, template_content)
    return list(set(matches))  # Remove duplicates