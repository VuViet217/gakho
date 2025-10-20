from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate


class Command(BaseCommand):
    help = 'Cập nhật email templates cho approved và rejected'

    def handle(self, *args, **kwargs):
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
            border-left: 4px solid #28a745;
            padding: 20px;
            margin-bottom: 25px;
        }
        .message-box.rejected {
            border-left-color: #dc3545;
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
            color: #28a745;
            font-size: 16px;
            border-bottom: 2px solid #28a745;
            padding-bottom: 10px;
        }
        .info-box.rejected h3 {
            color: #dc3545;
            border-bottom-color: #dc3545;
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
            background: #28a745;
        }
        .product-table thead.rejected {
            background: #dc3545;
        }
        .product-table th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            color: #ffffff;
            border: 1px solid #1e7e34;
        }
        .product-table.rejected th {
            border-color: #bd2130;
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
            background: #28a745;
            color: #ffffff;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
        }
        .product-code.rejected {
            background: #dc3545;
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
                'code': 'request_approved',
                'name': 'Thông báo yêu cầu được phê duyệt',
                'description': 'Email gửi cho người tạo yêu cầu khi yêu cầu được phê duyệt',
                'subject': 'Yêu cầu #{{ request.request_code }} đã được phê duyệt',
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
        <div class="header" style="border-bottom-color: #28a745;">
            <h1>YÊU CẦU ĐÃ ĐƯỢC PHÊ DUYỆT</h1>
            <p>Mã yêu cầu: #{{{{ request.request_code }}}}</p>
        </div>

        <div class="content-box">
            <div class="message-box">
                <h2>Xin chào {{{{ request.requester.get_full_name }}}},</h2>
                <p>Yêu cầu cấp phát vật tư của bạn đã được phê duyệt bởi {{{{ request.approved_by.get_full_name }}}}.</p>
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
                    <span class="label">Người phê duyệt:</span>
                    <span class="value">{{{{ request.approved_by.get_full_name }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày phê duyệt:</span>
                    <span class="value">{{{{ request.approved_at|date:"d/m/Y H:i" }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="value"><span class="status-badge status-approved">Đã phê duyệt</span></span>
                </div>
            </div>

            <h3 style="color: #28a745; margin-top: 30px; border-bottom: 2px solid #28a745; padding-bottom: 10px;">DANH SÁCH VẬT TƯ ĐÃ DUYỆT</h3>
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
                        <td style="text-align: center;"><strong style="color: #28a745; font-size: 16px;">{{{{ employee_product.quantity }}}}</strong></td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>

            {{% if request.approval_note %}}
            <div style="background: #d4edda; border: 1px solid #28a745; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <strong style="color: #155724;">Ghi chú từ người phê duyệt:</strong>
                <p style="margin: 5px 0; color: #333;">{{{{ request.approval_note }}}}</p>
            </div>
            {{% endif %}}

            <div style="background: #e7f5ed; border: 1px solid #28a745; border-left: 4px solid #28a745; padding: 20px; margin: 20px 0; border-radius: 4px;">
                <h3 style="margin-top: 0; color: #155724; font-size: 16px;">CÁC BƯỚC TIẾP THEO</h3>
                <ul style="margin: 10px 0; padding-left: 25px;">
                    <li style="margin: 8px 0; color: #333;">Yêu cầu đang chờ bộ phận kho lên lịch cấp phát</li>
                    <li style="margin: 8px 0; color: #333;">Bạn sẽ nhận được thông báo khi lịch cấp phát được xác nhận</li>
                    <li style="margin: 8px 0; color: #333;">Vui lòng sắp xếp thời gian nhận hàng theo lịch đã được thông báo</li>
                </ul>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/inventory/requests/{{{{ request.id }}}}/" class="button" style="background: #28a745;">Xem chi tiết yêu cầu</a>
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
                'code': 'request_rejected',
                'name': 'Thông báo yêu cầu bị từ chối',
                'description': 'Email gửi cho người tạo yêu cầu khi yêu cầu bị từ chối',
                'subject': 'Yêu cầu #{{ request.request_code }} đã bị từ chối',
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
        <div class="header" style="border-bottom-color: #dc3545;">
            <h1>YÊU CẦU BỊ TỪ CHỐI</h1>
            <p>Mã yêu cầu: #{{{{ request.request_code }}}}</p>
        </div>

        <div class="content-box">
            <div class="message-box rejected">
                <h2>Xin chào {{{{ request.requester.get_full_name }}}},</h2>
                <p>Rất tiếc, yêu cầu cấp phát vật tư của bạn đã bị từ chối bởi {{{{ request.approved_by.get_full_name }}}}.</p>
            </div>

            <div class="info-box rejected">
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
                    <span class="label">Người từ chối:</span>
                    <span class="value">{{{{ request.approved_by.get_full_name }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày từ chối:</span>
                    <span class="value">{{{{ request.approved_at|date:"d/m/Y H:i" }}}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="value"><span class="status-badge status-rejected">Đã từ chối</span></span>
                </div>
            </div>

            {{% if request.approval_note %}}
            <div style="background: #f8d7da; border: 1px solid #dc3545; border-left: 4px solid #dc3545; padding: 20px; margin: 20px 0; border-radius: 4px;">
                <strong style="color: #721c24; font-size: 16px;">Lý do từ chối:</strong>
                <p style="margin: 10px 0; color: #333; font-size: 14px; line-height: 1.6;">{{{{ request.approval_note }}}}</p>
            </div>
            {{% endif %}}

            <h3 style="color: #dc3545; margin-top: 30px; border-bottom: 2px solid #dc3545; padding-bottom: 10px;">DANH SÁCH VẬT TƯ</h3>
            <table class="product-table rejected">
                <thead class="rejected">
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
                            <span class="product-code rejected">{{{{ employee_product.product.product_code }}}}</span><br>
                            {{{{ employee_product.product.name }}}}
                        </td>
                        <td style="text-align: center;"><strong style="color: #dc3545; font-size: 16px;">{{{{ employee_product.quantity }}}}</strong></td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>

            <div style="background: #fff3e0; border: 1px solid #ff9800; border-left: 4px solid #ff9800; padding: 20px; margin: 20px 0; border-radius: 4px;">
                <h3 style="margin-top: 0; color: #e65100; font-size: 16px;">BẠN CÓ THỂ</h3>
                <ul style="margin: 10px 0; padding-left: 25px;">
                    <li style="margin: 8px 0; color: #333;">Liên hệ với người quản lý để hiểu rõ hơn về lý do từ chối</li>
                    <li style="margin: 8px 0; color: #333;">Điều chỉnh yêu cầu theo phản hồi và tạo yêu cầu mới</li>
                    <li style="margin: 8px 0; color: #333;">Kiểm tra lại quy trình và điều kiện cấp phát vật tư</li>
                </ul>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/inventory/requests/{{{{ request.id }}}}/" class="button">Xem chi tiết yêu cầu</a>
                <a href="http://127.0.0.1:8000/inventory/requests/create/" class="button" style="background: #28a745;">Tạo yêu cầu mới</a>
            </div>
        </div>

        <div class="footer">
            <p><strong>OVNC Inventory Management System</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p>Nếu có thắc mắc, vui lòng liên hệ: support@ovnc.com</p>
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
