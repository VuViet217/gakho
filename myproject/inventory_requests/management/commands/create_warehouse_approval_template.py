from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Tạo template email thông báo yêu cầu đã được phê duyệt cần xử lý xuất kho cho quản lý kho'

    def handle(self, *args, **options):
        # Template: Thông báo cho quản lý kho cần xử lý xuất kho
        warehouse_approval_template = {
            'code': 'warehouse_approval_required',
            'name': 'Yêu cầu cần xử lý xuất kho',
            'subject': '[Quản lý kho] Yêu cầu #{{ request.request_code }} cần xử lý xuất kho',
            'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
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
            border-bottom: 3px solid #6c5ce7;
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
            border-left: 4px solid #6c5ce7;
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
        .urgent-box {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
        }
        .urgent-box h3 {
            margin-top: 0;
            color: #856404;
            font-size: 16px;
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
            color: #6c5ce7;
            font-size: 16px;
            border-bottom: 2px solid #6c5ce7;
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
        .status-approved {
            background: #d4edda;
            color: #155724;
            border: 1px solid #28a745;
        }
        .product-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border: 1px solid #e0e0e0;
        }
        .product-table thead {
            background: #6c5ce7;
        }
        .product-table th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            color: #ffffff;
            border: 1px solid #5b4cce;
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
            background: #6c5ce7;
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
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>YÊU CẦU CẦN XỬ LÝ XUẤT KHO</h1>
            <p>Mã yêu cầu: #{{ request.request_code }}</p>
        </div>

        <div class="content-box">
            <div class="urgent-box">
                <h3>⚠️ THÔNG BÁO QUAN TRỌNG</h3>
                <p style="margin: 5px 0; color: #333;">Yêu cầu cấp phát vật tư đã được phê duyệt và cần xử lý xuất kho ngay.</p>
            </div>

            <div class="message-box">
                <h2>Xin chào {{ warehouse_manager.get_full_name }},</h2>
                <p>Bạn có một yêu cầu cấp phát vật tư mới đã được phê duyệt và cần xử lý xuất kho.</p>
            </div>

            <div class="info-box">
                <h3>THÔNG TIN YÊU CẦU</h3>
                <div class="info-row">
                    <span class="label">Mã yêu cầu:</span>
                    <span class="value"><strong>#{{ request.request_code }}</strong></span>
                </div>
                <div class="info-row">
                    <span class="label">Tiêu đề:</span>
                    <span class="value">{{ request.title }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Người yêu cầu:</span>
                    <span class="value">{{ request.requester.get_full_name }} ({{ request.requester.email }})</span>
                </div>
                <div class="info-row">
                    <span class="label">Người phê duyệt:</span>
                    <span class="value">{{ request.approver.get_full_name }} ({{ request.approver.email }})</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày tạo:</span>
                    <span class="value">{{ request.created_at|date:"d/m/Y H:i" }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày phê duyệt:</span>
                    <span class="value">{{ request.approval_date|date:"d/m/Y H:i" }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="value"><span class="status-badge status-approved">Đã phê duyệt</span></span>
                </div>
            </div>

            <h3 style="color: #6c5ce7; margin-top: 30px; border-bottom: 2px solid #6c5ce7; padding-bottom: 10px;">DANH SÁCH VẬT TƯ CẦN XUẤT KHO</h3>
            <table class="product-table">
                <thead>
                    <tr>
                        <th>Nhân viên</th>
                        <th>Sản phẩm</th>
                        <th style="text-align: center;">Số lượng</th>
                    </tr>
                </thead>
                <tbody>
                    {% for employee_product in request.employee_products.all %}
                    <tr>
                        <td>
                            <strong>{{ employee_product.employee.full_name }}</strong><br>
                            <small style="color: #666;">{{ employee_product.employee.department.name|default:"N/A" }}</small>
                        </td>
                        <td>
                            <span class="product-code">{{ employee_product.product.product_code }}</span><br>
                            {{ employee_product.product.name }}
                        </td>
                        <td style="text-align: center;"><strong style="color: #6c5ce7; font-size: 16px;">{{ employee_product.quantity }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            {% if request.approval_note %}
            <div style="background: #d4edda; border: 1px solid #28a745; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <strong style="color: #155724;">Ghi chú từ người phê duyệt:</strong>
                <p style="margin: 5px 0; color: #333;">{{ request.approval_note }}</p>
            </div>
            {% endif %}

            {% if request.note %}
            <div style="background: #e7f3ff; border: 1px solid #2196F3; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <strong style="color: #0d47a1;">Ghi chú từ người yêu cầu:</strong>
                <p style="margin: 5px 0; color: #333;">{{ request.note }}</p>
            </div>
            {% endif %}

            <div style="background: #fff3e0; border: 1px solid #ff9800; border-left: 4px solid #ff9800; padding: 20px; margin: 20px 0; border-radius: 4px;">
                <h3 style="margin-top: 0; color: #e65100; font-size: 16px;">BƯỚC TIẾP THEO</h3>
                <ul style="margin: 10px 0; padding-left: 25px;">
                    <li style="margin: 8px 0; color: #333;">Kiểm tra danh sách vật tư cần xuất</li>
                    <li style="margin: 8px 0; color: #333;">Xác nhận tồn kho đủ để cấp phát</li>
                    <li style="margin: 8px 0; color: #333;">Lên lịch cấp phát và thông báo cho người yêu cầu</li>
                    <li style="margin: 8px 0; color: #333;">Chuẩn bị vật tư theo thời gian đã hẹn</li>
                </ul>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/inventory/requests/{{ request.id }}/" class="button" style="background: #6c5ce7;">Xem chi tiết và lên lịch</a>
            </div>
        </div>

        <div class="footer">
            <p><strong>GA Inventory Management System</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p>Vui lòng xử lý yêu cầu xuất kho sớm nhất có thể.</p>
            <p>&copy; 2025 GA. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
            ''',
            'is_active': True,
            'description': 'Template email thông báo cho quản lý kho khi có yêu cầu được phê duyệt cần xử lý xuất kho'
        }

        # Tạo hoặc cập nhật template
        template, created = EmailTemplate.objects.update_or_create(
            code=warehouse_approval_template['code'],
            defaults=warehouse_approval_template
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Đã tạo template: {template.code}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Đã cập nhật template: {template.code}'))
