from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Cập nhật template email pending_approval có bảng sản phẩm, phù hợp Outlook'

    def handle(self, *args, **options):
        template_code = 'pending_approval'
        
        # Nội dung template với bảng sản phẩm
        new_content = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="650" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border: 1px solid #dddddd;">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #ff9800; padding: 20px; text-align: center;">
                            <h1 style="margin: 0; color: #333333; font-size: 22px; font-weight: bold;">YÊU CẦU CHỜ PHÊ DUYỆT</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 30px;">
                            <p style="margin: 0 0 15px 0; font-size: 15px; color: #333333;">
                                Xin chào <strong>{{ approver_name }}</strong>,
                            </p>
                            
                            <p style="margin: 0 0 20px 0; font-size: 15px; color: #333333;">
                                Có một yêu cầu cấp phát đang chờ bạn phê duyệt:
                            </p>
                            
                            <!-- Info Table -->
                            <table width="100%" cellpadding="10" cellspacing="0" border="1" style="border-collapse: collapse; margin: 20px 0; border-color: #dddddd;">
                                <tr>
                                    <td width="35%" style="font-weight: bold; color: #555555; background-color: #f5f5f5;">Mã yêu cầu:</td>
                                    <td style="color: #333333;"><strong>#{{ request_id }}</strong></td>
                                </tr>
                                <tr>
                                    <td style="font-weight: bold; color: #555555; background-color: #f5f5f5;">Người yêu cầu:</td>
                                    <td style="color: #333333;">{{ requester_name }}</td>
                                </tr>
                                <tr>
                                    <td style="font-weight: bold; color: #555555; background-color: #f5f5f5;">Email:</td>
                                    <td style="color: #333333;">{{ requester_email }}</td>
                                </tr>
                                <tr>
                                    <td style="font-weight: bold; color: #555555; background-color: #f5f5f5;">Thời gian tạo:</td>
                                    <td style="color: #333333;">{{ created_at }}</td>
                                </tr>
                                <tr>
                                    <td style="font-weight: bold; color: #555555; background-color: #f5f5f5;">Ngày mong muốn:</td>
                                    <td style="color: #333333;">{{ requested_date }}</td>
                                </tr>
                                <tr>
                                    <td style="font-weight: bold; color: #555555; background-color: #f5f5f5;">Trạng thái:</td>
                                    <td style="color: #ff9800; font-weight: bold;">Chờ phê duyệt</td>
                                </tr>
                            </table>

                            <!-- Product Details Section -->
                            {% if employee_products_with_history %}
                            <h3 style="margin: 30px 0 15px 0; color: #333333; font-size: 18px; border-bottom: 2px solid #ff9800; padding-bottom: 8px;">
                                Chi tiết phân bổ sản phẩm cho nhân viên
                            </h3>
                            
                            <table width="100%" cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse; margin: 15px 0; border-color: #dddddd;">
                                <thead>
                                    <tr style="background-color: #e91e63;">
                                        <th style="color: #333333; text-align: center; padding: 10px; font-size: 13px; border: 1px solid #d81b60;">#</th>
                                        <th style="color: #333333; text-align: left; padding: 10px; font-size: 13px; border: 1px solid #d81b60;">Nhân viên</th>
                                        <th style="color: #333333; text-align: left; padding: 10px; font-size: 13px; border: 1px solid #d81b60;">Sản phẩm</th>
                                        <th style="color: #333333; text-align: center; padding: 10px; font-size: 13px; border: 1px solid #d81b60;">SL</th>
                                        <th style="color: #333333; text-align: left; padding: 10px; font-size: 13px; border: 1px solid #d81b60;">Lần lấy gần nhất</th>
                                        <th style="color: #333333; text-align: left; padding: 10px; font-size: 13px; border: 1px solid #d81b60;">Ghi chú</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for item in employee_products_with_history %}
                                    <tr style="background-color: {% cycle '#ffffff' '#fafafa' %};">
                                        <td style="text-align: center; color: #333333; padding: 8px; border: 1px solid #dddddd;">{{ forloop.counter }}</td>
                                        <td style="color: #333333; padding: 8px; border: 1px solid #dddddd;">
                                            <strong>{{ item.employee_name }}</strong><br>
                                            <span style="font-size: 12px; color: #666666;">{{ item.employee_code }}</span>
                                        </td>
                                        <td style="color: #333333; padding: 8px; border: 1px solid #dddddd;">
                                            {{ item.product_name }}<br>
                                            <span style="font-size: 12px; color: #666666;">Mã: {{ item.product_code }}</span>
                                        </td>
                                        <td style="text-align: center; color: #333333; font-weight: bold; padding: 8px; border: 1px solid #dddddd;">{{ item.quantity }}</td>
                                        <td style="color: #333333; padding: 8px; border: 1px solid #dddddd;">
                                            {% if item.last_delivery_date %}
                                            <div style="background-color: #e8f5e9; padding: 6px; border-left: 3px solid #4caf50; font-size: 12px;">
                                                <strong>SL:</strong> {{ item.last_delivery_quantity }}<br>
                                                <strong>Ngày:</strong> {{ item.last_delivery_date }}<br>
                                                <strong>YC:</strong> {{ item.last_delivery_request }}
                                            </div>
                                            {% else %}
                                            <em style="color: #999999; font-size: 12px;">Chưa có lịch sử</em>
                                            {% endif %}
                                        </td>
                                        <td style="color: #333333; padding: 8px; border: 1px solid #dddddd;">
                                            {% if item.notes %}{{ item.notes }}{% else %}—{% endif %}
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                            {% endif %}

                            <!-- Action Buttons -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <table cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{ approve_url }}" style="display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">PHÊ DUYỆT</a>
                                                </td>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{ reject_url }}" style="display: inline-block; padding: 12px 24px; background-color: #f44336; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">TỪ CHỐI</a>
                                                </td>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{ request_url }}" style="display: inline-block; padding: 12px 24px; background-color: #2196F3; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">XEM CHI TIẾT</a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Note -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 20px 0;">
                                <tr>
                                    <td style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px;">
                                        <p style="margin: 0; color: #856404; font-size: 14px;">
                                            <strong>Lưu ý:</strong> Vui lòng đăng nhập vào hệ thống để xem chi tiết và xử lý yêu cầu này.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 20px 0 0 0; color: #666666; font-size: 13px;">
                                Đây là email tự động, vui lòng không trả lời email này.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f5f5f5; padding: 20px; text-align: center; border-top: 1px solid #dddddd;">
                            <p style="margin: 5px 0; color: #666666; font-size: 13px;"><strong>Hệ thống Quản lý Kho</strong></p>
                            <p style="margin: 5px 0; color: #666666; font-size: 12px;">Email này được gửi tự động, vui lòng không trả lời.</p>
                            <p style="margin: 5px 0; color: #666666; font-size: 12px;">&copy; 2025 OVNC Inventory Management System</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''
        
        try:
            template = EmailTemplate.objects.get(code=template_code)
            template.content = new_content
            template.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Đã cập nhật template "{template_code}" thành công với bảng sản phẩm!')
            )
        except EmailTemplate.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Không tìm thấy template với mã: {template_code}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Lỗi khi cập nhật template: {str(e)}')
            )
