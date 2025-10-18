from .utils import render_email_template
from .email_service import send_system_email

def send_template_email(recipient_list, template_code, context_data, attachments=None):
    """
    Gửi email dựa trên mẫu đã định nghĩa.
    
    Args:
        recipient_list: Danh sách địa chỉ email người nhận (list hoặc string)
        template_code: Mã mẫu email cần sử dụng
        context_data: Dict chứa dữ liệu để render vào mẫu
        attachments: Danh sách đường dẫn đến file đính kèm
        
    Returns:
        tuple: (success, error_message)
    """
    # Chuyển đổi recipient thành list nếu là string
    if isinstance(recipient_list, str):
        recipient_list = [recipient_list]
    
    # Render mẫu email
    subject, html_content, text_content = render_email_template(template_code, context_data)
    
    if not subject or not html_content:
        return False, f"Không thể render mẫu email với mã: {template_code}"
    
    # Gửi email
    return send_system_email(
        recipient_list=recipient_list,
        subject=subject,
        message=text_content,
        html_message=html_content,
        attachments=attachments
    )