from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate


class Command(BaseCommand):
    help = 'Cập nhật tất cả email templates với thiết kế phù hợp Outlook'

    def handle(self, *args, **kwargs):
        # Common styles cho tất cả emails
        common_style = '''
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
        }
        .email-container {
            background: #ffffff;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 0;
        }
        .header {
            padding: 30px;
            text-align: center;
            border-radius: 6px 6px 0 0;
            border-bottom: 3px solid #ddd;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
            color: #333;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 14px;
            color: #666;
        }
        .content-box {
            background: #ffffff;
            padding: 30px;
        }
        .message-box {
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 20px;
            margin-bottom: 25px;
        }
        .message-box h2 {
            margin: 0 0 10px 0;
            font-size: 18px;
            color: #333;
        }
        .message-box p {
            margin: 0;
            font-size: 14px;
            color: #555;
        }
        .info-box {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
        }
        .info-box h3 {
            margin-top: 0;
            color: #007bff;
            font-size: 16px;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .info-row {
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .label {
            font-weight: 600;
            color: #555;
            display: inline-block;
            min-width: 150px;
        }
        .value {
            color: #333;
        }
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-pending {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffc107;
        }
        .status-approved {
            background: #d4edda;
            color: #155724;
            border: 1px solid #28a745;
        }
        .status-rejected {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #dc3545;
        }
        .product-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border: 1px solid #e0e0e0;
        }
        .product-table thead {
            background: #007bff;
        }
        .product-table th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            color: #ffffff;
            border: 1px solid #0056b3;
        }
        .product-table td {
            padding: 12px;
            border: 1px solid #e0e0e0;
            color: #333;
        }
        .product-table tbody tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .product-code {
            display: inline-block;
            background: #007bff;
            color: #ffffff;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
        }
        .button {
            display: inline-block;
            padding: 12px 30px;
            background: #007bff;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            margin: 10px 5px;
        }
        .footer {
            text-align: center;
            color: #666;
            margin-top: 30px;
            padding: 20px;
            border-top: 2px solid #e0e0e0;
            font-size: 12px;
        }
        .footer p {
            margin: 5px 0;
        }
        '''

        templates = [
            {
                'code': 'request_created',
                'name': 'Thông báo tạo yêu cầu thành công',
                'description': 'Email gửi cho người tạo yêu cầu khi yêu cầu được tạo thành công',
                'subject': 'Yêu cầu #{{ request.request_code }} đã được tạo thành công',
                'content': f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        {common_style}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>YÊU CẦU ĐÃ ĐƯỢC TẠO THÀNH CÔNG</h1>
            <p>Mã yêu cầu: #{{{{ request.request_code }}}}</p>
        </div>

        <div class="content-box">
            <div class="message-box">
                <h2>Xin chào {{{{ user.get_full_name }}}},</h2>
                <p>Yêu cầu cấp phát vật tư của bạn đã được tạo thành công trong hệ thống.</p>
            </div>

            <div class="info-box">
                <h3>THÔNG TIN YÊU CẦU</h3>
                <div class="info-row">
                    <span class="label">Mã yêu cầu:</span>
                    <span class="value"><strong>#{{{{ request.request_code }}}}</strong></span>
                </div>
                <div class="info-row">
                    <span class="label">Tiêu đề:</span>
                    <span class="value">{{{{ request.title }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Người tạo:</span>
                    <span class="value">{{{{ request.requester.get_full_name }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày tạo:</span>
                    <span class="value">{{{{ request.created_at|date:"d/m/Y H:i" }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="value"><span class="status-badge status-pending">Bản nháp</span></span>
                </div>
            </div>

            <h3 style="color: #007bff; margin-top: 30px; border-bottom: 2px solid #007bff; padding-bottom: 10px;">DANH SÁCH VẬT TƯ</h3>
            <table class="product-table">
                <thead>
                    <tr>
                        <th>Nhân viên</th>
                        <th>Sản phẩm</th>
                        <th style="text-align: center;">Số lượng</th>
                    </tr>
                </thead>
                <tbody>
                    {{% for employee_product in request.employee_products.all %}}
                    <tr>
                        <td>
                            <strong>{{{{ employee_product.employee.full_name }}}}</strong><br>
                            <small style="color: #666;">{{{{ employee_product.employee.department.name|default:"N/A" }}}}</small>
                        </td>
                        <td>
                            <span class="product-code">{{{{ employee_product.product.product_code }}}}</span><br>
                            {{{{ employee_product.product.name }}}}
                        </td>
                        <td style="text-align: center;"><strong style="color: #007bff; font-size: 16px;">{{{{ employee_product.quantity }}}}</strong></td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>

            <div style="background: #f0f8ff; border: 1px solid #007bff; border-left: 4px solid #007bff; padding: 20px; margin: 20px 0; border-radius: 4px;">
                <h3 style="margin-top: 0; color: #0056b3; font-size: 16px;">CÁC BƯỚC TIẾP THEO</h3>
                <ul style="margin: 10px 0; padding-left: 25px;">
                    <li style="margin: 8px 0; color: #333;">Kiểm tra lại thông tin yêu cầu</li>
                    <li style="margin: 8px 0; color: #333;">Nhấn "Gửi yêu cầu" để chuyển đến quản lý phê duyệt</li>
                    <li style="margin: 8px 0; color: #333;">Theo dõi trạng thái qua email hoặc hệ thống</li>
                </ul>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/inventory/requests/{{{{ request.id }}}}/" class="button">Xem chi tiết yêu cầu</a>
            </div>
        </div>

        <div class="footer">
            <p><strong>OVNC Inventory Management System</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p>&copy; 2025 OVNC. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
                '''
            },
            {
                'code': 'pending_approval',
                'name': 'Thông báo yêu cầu chờ phê duyệt',
                'description': 'Email gửi cho quản lý khi có yêu cầu cần phê duyệt',
                'subject': 'Yêu cầu #{{ request.request_code }} cần phê duyệt',
                'content': f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        {common_style}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header" style="border-bottom-color: #ffc107;">
            <h1>YÊU CẦU CẦN PHÊ DUYỆT</h1>
            <p>Mã yêu cầu: #{{{{ request.request_code }}}}</p>
        </div>

        <div class="content-box">
            <div class="message-box" style="border-left-color: #ffc107;">
                <h2>Xin chào {{{{ manager.get_full_name }}}},</h2>
                <p>Bạn có một yêu cầu cấp phát vật tư mới cần phê duyệt từ {{{{ request.requester.get_full_name }}}}.</p>
            </div>

            <div class="info-box">
                <h3 style="color: #ffc107; border-bottom-color: #ffc107;">THÔNG TIN YÊU CẦU</h3>
                <div class="info-row">
                    <span class="label">Mã yêu cầu:</span>
                    <span class="value"><strong>#{{{{ request.request_code }}}}</strong></span>
                </div>
                <div class="info-row">
                    <span class="label">Tiêu đề:</span>
                    <span class="value">{{{{ request.title }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Người yêu cầu:</span>
                    <span class="value">{{{{ request.requester.get_full_name }}}} ({{{{ request.requester.email }}}})</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày tạo:</span>
                    <span class="value">{{{{ request.created_at|date:"d/m/Y H:i" }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày mong muốn:</span>
                    <span class="value">{{{{ request.expected_date|date:"d/m/Y" }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="value"><span class="status-badge status-pending">Chờ phê duyệt</span></span>
                </div>
            </div>

            <h3 style="color: #ffc107; margin-top: 30px; border-bottom: 2px solid #ffc107; padding-bottom: 10px;">DANH SÁCH VẬT TƯ</h3>
            <table class="product-table">
                <thead style="background: #ffc107;">
                    <tr>
                        <th style="border-color: #e0a800;">Nhân viên</th>
                        <th style="border-color: #e0a800;">Sản phẩm</th>
                        <th style="text-align: center; border-color: #e0a800;">Số lượng</th>
                    </tr>
                </thead>
                <tbody>
                    {{% for employee_product in request.employee_products.all %}}
                    <tr>
                        <td>
                            <strong>{{{{ employee_product.employee.full_name }}}}</strong><br>
                            <small style="color: #666;">{{{{ employee_product.employee.department.name|default:"N/A" }}}}</small>
                        </td>
                        <td>
                            <span class="product-code" style="background: #ffc107;">{{{{ employee_product.product.product_code }}}}</span><br>
                            {{{{ employee_product.product.name }}}}
                        </td>
                        <td style="text-align: center;"><strong style="color: #ffc107; font-size: 16px;">{{{{ employee_product.quantity }}}}</strong></td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>

            {{% if request.note %}}
            <div style="background: #fffbf0; border: 1px solid #ffc107; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <strong style="color: #856404;">Ghi chú từ người yêu cầu:</strong>
                <p style="margin: 5px 0; color: #333;">{{{{ request.note }}}}</p>
            </div>
            {{% endif %}}

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/inventory/requests/{{{{ request.id }}}}/approve/" class="button" style="background: #28a745;">Phê duyệt ngay</a>
                <a href="http://127.0.0.1:8000/inventory/requests/{{{{ request.id }}}}/" class="button">Xem chi tiết</a>
            </div>
        </div>

        <div class="footer">
            <p><strong>OVNC Inventory Management System</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p>&copy; 2025 OVNC. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
                '''
            }
        ]

        for template_data in templates:
            template, created = EmailTemplate.objects.update_or_create(
                code=template_data['code'],
                defaults=template_data
            )
            action = 'Đã tạo' if created else 'Đã cập nhật'
            self.stdout.write(self.style.SUCCESS(f'{action} template: {template.code}'))
