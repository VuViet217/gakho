import socket
import smtplib
import logging
from django.conf import settings
from django.utils import timezone
from .models import EmailConfiguration

logger = logging.getLogger(__name__)

def check_smtp_connection(config):
    """
    Kiểm tra kết nối đến SMTP server.
    
    Args:
        config: EmailConfiguration object
        
    Returns:
        tuple: (success, error_message)
    """
    try:
        # Kiểm tra kết nối socket cơ bản trước
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Timeout 10s
        
        result = sock.connect_ex((config.smtp_host, config.smtp_port))
        
        if result != 0:
            sock.close()
            return False, f"Không thể kết nối đến SMTP server {config.smtp_host}:{config.smtp_port}. Lỗi kết nối: {result}"
            
        sock.close()
        
        # Thử thiết lập kết nối SMTP
        if config.use_ssl:
            server = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=10)
        
        server.set_debuglevel(1)  # Enable debug để theo dõi chi tiết
        
        # Bắt đầu TLS nếu được yêu cầu
        if config.use_tls:
            server.starttls()
        
        # Login nếu cần xác thực
        if config.auth_method == 'normal' and config.smtp_username and config.smtp_password:
            server.login(config.smtp_username, config.smtp_password)
        
        # Thử gửi NOOP (No Operation) để đảm bảo kết nối hoạt động
        server.noop()
        
        # Đóng kết nối
        server.quit()
        
        return True, "Kết nối SMTP thành công"
        
    except socket.timeout as e:
        return False, f"Timeout khi kết nối đến SMTP server: {str(e)}"
    except socket.gaierror as e:
        return False, f"Lỗi DNS khi kết nối đến SMTP server: {str(e)}"
    except smtplib.SMTPException as e:
        return False, f"Lỗi SMTP: {str(e)}"
    except Exception as e:
        return False, f"Lỗi không xác định: {str(e)}"