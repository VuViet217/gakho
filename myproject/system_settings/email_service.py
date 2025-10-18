from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import EmailConfiguration
from .utils import render_email_template
import logging

logger = logging.getLogger(__name__)

def get_email_configuration():
    """
    Lấy cấu hình email đang hoạt động.
    """
    try:
        config = EmailConfiguration.objects.filter(is_active=True).first()
        return config
    except Exception as e:
        logger.error(f"Lỗi khi lấy cấu hình email: {str(e)}")
        return None

def send_test_email(recipient, subject, message):
    """
    Gửi email test với cấu hình trong database.
    
    Args:
        recipient: Địa chỉ email người nhận
        subject: Tiêu đề email
        message: Nội dung email
        
    Returns:
        tuple: (success, error_message)
    """
    config = get_email_configuration()
    if not config:
        return False, "Không tìm thấy cấu hình email nào đang hoạt động"
    
    try:
        # Gửi email với nhiều thông tin debug hơn
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=config.from_email,
            to=[recipient],
        )
        
        # In ra thông tin debug
        logger.info(f"SMTP Info - Host: {settings.EMAIL_HOST}, Port: {settings.EMAIL_PORT}")
        logger.info(f"SMTP Auth - User: {settings.EMAIL_HOST_USER}, TLS: {settings.EMAIL_USE_TLS}, SSL: {settings.EMAIL_USE_SSL}")
        
        # Thử gửi với timeout dài hơn
        email.send(fail_silently=False)
        
        # Cập nhật trạng thái test
        config.last_test_success = True
        config.last_test_date = timezone.now()
        config.save(update_fields=['last_test_success', 'last_test_date'])
        
        return True, "Gửi email thành công"
    except Exception as e:
        # Lưu lại lỗi
        error_message = str(e)
        logger.error(f"Lỗi khi gửi email test: {error_message}")
        
        # Cập nhật trạng thái test
        config.last_test_success = False
        config.last_test_date = timezone.now()
        config.save(update_fields=['last_test_success', 'last_test_date'])
        
        return False, f"Lỗi khi gửi email: {error_message}"

def send_system_email(recipient_list, subject, message, html_message=None, attachments=None):
    """
    Gửi email từ hệ thống với cấu hình trong database.
    
    Args:
        recipient_list: Danh sách địa chỉ email người nhận
        subject: Tiêu đề email
        message: Nội dung email dạng text
        html_message: Nội dung email dạng HTML (tùy chọn)
        attachments: Danh sách đường dẫn đến file đính kèm
        
    Returns:
        tuple: (success, error_message)
    """
    config = get_email_configuration()
    if not config:
        return False, "Không tìm thấy cấu hình email nào đang hoạt động"
    
    try:
        email = EmailMessage(
            subject=subject,
            body=html_message or message,
            from_email=config.from_email,
            to=recipient_list
        )
        
        if html_message:
            email.content_subtype = "html"
            
        if attachments:
            for attachment in attachments:
                email.attach_file(attachment)
                
        email.send(fail_silently=False)
        return True, "Gửi email thành công"
    except Exception as e:
        error_message = str(e)
        logger.error(f"Lỗi khi gửi email hệ thống: {error_message}")
        return False, f"Lỗi khi gửi email: {error_message}"