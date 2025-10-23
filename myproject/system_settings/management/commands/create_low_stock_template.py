from django.core.management.base import BaseCommand
from django.utils import timezone
from system_settings.models import EmailTemplate


DEFAULT_HTML = '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Cảnh báo tồn kho thấp</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
    <!-- Wrapper Table -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <!-- Main Container -->
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden;">
                    
                    <!-- Header with Icon -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); padding: 30px 40px; text-align: center;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center">
                                        <!-- Warning Icon -->
                                        <div style="background-color: rgba(255,255,255,0.2); width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 15px; padding: 15px;">
                                            <div style="font-size: 32px; color: #ffffff;">⚠️</div>
                                        </div>
                                        <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600; letter-spacing: -0.5px;">
                                            Cảnh báo tồn kho thấp
                                        </h1>
                                        <p style="margin: 8px 0 0 0; color: rgba(255,255,255,0.9); font-size: 14px;">
                                            Hệ thống quản lý kho GA
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Alert Summary Box -->
                    <tr>
                        <td style="padding: 30px 40px 20px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                                <tr>
                                    <td style="padding: 15px 20px;">
                                        <p style="margin: 0; color: #856404; font-size: 15px; line-height: 1.6;">
                                            <strong style="font-size: 16px;">🔔 Thông báo quan trọng!</strong><br/>
                                            Hiện có <strong style="color: #dc3545;">{{ count }}</strong> sản phẩm đang có mức tồn kho <strong>bằng hoặc dưới ngưỡng tối thiểu</strong>. Vui lòng xem xét và lên kế hoạch nhập hàng kịp thời.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Greeting -->
                    <tr>
                        <td style="padding: 0 40px 20px;">
                            <p style="margin: 0; color: #333333; font-size: 15px; line-height: 1.6;">
                                Xin chào,
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Products Table -->
                    <tr>
                        <td style="padding: 0 40px 30px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden;">
                                <!-- Table Header -->
                                <tr style="background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);">
                                    <th align="left" style="padding: 12px 15px; font-size: 13px; font-weight: 600; color: #495057; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #dee2e6;">
                                        Mã SP
                                    </th>
                                    <th align="left" style="padding: 12px 15px; font-size: 13px; font-weight: 600; color: #495057; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #dee2e6;">
                                        Tên sản phẩm
                                    </th>
                                    <th align="center" style="padding: 12px 15px; font-size: 13px; font-weight: 600; color: #495057; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #dee2e6;">
                                        Tồn kho
                                    </th>
                                    <th align="center" style="padding: 12px 15px; font-size: 13px; font-weight: 600; color: #495057; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #dee2e6;">
                                        Tối thiểu
                                    </th>
                                    <th align="center" style="padding: 12px 15px; font-size: 13px; font-weight: 600; color: #495057; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #dee2e6;">
                                        Trạng thái
                                    </th>
                                </tr>
                                <!-- Table Body -->
                                {% for p in products %}
                                <tr style="background-color: {% cycle '#ffffff' '#f8f9fa' %};">
                                    <td style="padding: 12px 15px; font-size: 14px; color: #333333; border-bottom: 1px solid #e9ecef;">
                                        <strong style="color: #0d6efd;">{{ p.product_code }}</strong>
                                    </td>
                                    <td style="padding: 12px 15px; font-size: 14px; color: #333333; border-bottom: 1px solid #e9ecef;">
                                        {{ p.name }}
                                    </td>
                                    <td align="center" style="padding: 12px 15px; font-size: 14px; color: #dc3545; font-weight: 600; border-bottom: 1px solid #e9ecef;">
                                        {{ p.current_quantity }} {{ p.unit }}
                                    </td>
                                    <td align="center" style="padding: 12px 15px; font-size: 14px; color: #6c757d; border-bottom: 1px solid #e9ecef;">
                                        {{ p.minimum_quantity }} {{ p.unit }}
                                    </td>
                                    <td align="center" style="padding: 12px 15px; border-bottom: 1px solid #e9ecef;">
                                        <span style="display: inline-block; padding: 4px 10px; background-color: #dc3545; color: #ffffff; font-size: 11px; font-weight: 600; border-radius: 12px; text-transform: uppercase;">
                                            Thấp
                                        </span>
                                    </td>
                                </tr>
                                {% endfor %}
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Action Recommendation -->
                    <tr>
                        <td style="padding: 0 40px 30px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #e7f3ff; border-left: 4px solid #0d6efd; border-radius: 4px;">
                                <tr>
                                    <td style="padding: 15px 20px;">
                                        <p style="margin: 0 0 10px 0; color: #004085; font-size: 14px; font-weight: 600;">
                                            💡 Khuyến nghị hành động:
                                        </p>
                                        <ul style="margin: 0; padding-left: 20px; color: #004085; font-size: 14px; line-height: 1.8;">
                                            <li>Kiểm tra lại số lượng tồn kho thực tế</li>
                                            <li>Liên hệ nhà cung cấp để lên kế hoạch nhập hàng</li>
                                            <li>Cập nhật dự báo nhu cầu trong thời gian tới</li>
                                        </ul>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Closing -->
                    <tr>
                        <td style="padding: 0 40px 30px;">
                            <p style="margin: 0 0 15px 0; color: #333333; font-size: 15px; line-height: 1.6;">
                                Nếu có bất kỳ thắc mắc nào, vui lòng liên hệ với bộ phận quản lý kho.
                            </p>
                            <p style="margin: 0; color: #333333; font-size: 15px; line-height: 1.6;">
                                Trân trọng,<br/>
                                <strong style="color: #0d6efd;">Hệ thống quản lý kho GA</strong>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 20px 40px; border-top: 1px solid #e0e0e0;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center">
                                        <p style="margin: 0 0 8px 0; color: #6c757d; font-size: 12px;">
                                            📧 Email tự động được gửi lúc: <strong>{{ date }}</strong>
                                        </p>
                                        <p style="margin: 0; color: #adb5bd; font-size: 11px; line-height: 1.6;">
                                            Đây là email tự động từ hệ thống quản lý kho. Vui lòng không trả lời email này.<br/>
                                            © 2025 GA Inventory Management System. All rights reserved.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
'''


class Command(BaseCommand):
    help = 'Tạo mẫu email low_stock_alert nếu chưa tồn tại'

    def handle(self, *args, **options):
        template_code = 'low_stock_alert'
        template, created = EmailTemplate.objects.update_or_create(
            code=template_code,
            defaults={
                'type': 'low_stock_alert',
                'name': 'Cảnh báo tồn kho thấp',
                'subject': '[GA] ⚠️ Cảnh báo tồn kho thấp - {{ count }} sản phẩm cần nhập hàng',
                'content': DEFAULT_HTML,
                'description': 'Mẫu email tự động gửi cảnh báo khi có sản phẩm đạt ngưỡng tồn kho tối thiểu. Hệ thống sẽ gửi danh sách các sản phẩm cần nhập hàng đến người quản lý kho và các bên liên quan.',
                'is_html': True,
                'is_active': True,
                'variables': {'products': 'Danh sách sản phẩm (list)', 'date': 'Ngày giờ gửi email', 'count': 'Số lượng sản phẩm cảnh báo'},
                'default_recipients': '',  # Người dùng có thể điền vào form
                'default_cc': ''  # Người dùng có thể điền vào form
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Tạo mẫu low_stock_alert thành công.'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Mẫu low_stock_alert đã được cập nhật.'))
