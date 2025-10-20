from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate


class Command(BaseCommand):
    help = 'Tạo email template cho thông báo đã lên lịch cấp phát'

    def handle(self, *args, **kwargs):
        warehouse_scheduled_template = {
            'code': 'warehouse_scheduled',
            'name': 'Thông báo đã lên lịch cấp phát',
            'description': 'Email gửi cho người yêu cầu khi yêu cầu đã được lên lịch cấp phát bởi quản lý kho',
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
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 0;
        }
        .header {
            background: #667eea;
            color: #ffffff;
            padding: 30px;
            text-align: center;
            border-radius: 6px 6px 0 0;
        }
        .header h1 {
            margin: 0;
            font-size: 26px;
            font-weight: 600;
            color: #ffffff;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 15px;
            color: #ffffff;
            opacity: 0.95;
        }
        .content-box {
            background: #ffffff;
            padding: 30px;
        }
        .message-box {
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 25px;
        }
        .message-box h2 {
            margin: 0 0 10px 0;
            font-size: 20px;
            color: #333;
        }
        .message-box p {
            margin: 0;
            font-size: 15px;
            color: #555;
        }
        .schedule-highlight {
            background: #fff3e0;
            border: 2px solid #ff9800;
            padding: 25px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
        .schedule-highlight .datetime {
            font-size: 36px;
            font-weight: bold;
            color: #ff6f00;
            margin: 10px 0;
        }
        .schedule-highlight .label {
            color: #666;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
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
            color: #667eea;
            font-size: 18px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .info-row {
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .label {
            font-weight: 600;
            color: #555;
            display: inline-block;
            min-width: 180px;
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
            background: #667eea;
            color: #ffffff;
        }
        .product-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border: 1px solid #e0e0e0;
        }
        .product-table thead {
            background: #667eea;
        }
        .product-table th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            color: #ffffff;
            border: 1px solid #5a6fd8;
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
            background: #667eea;
            color: #ffffff;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
        }
        .note-box {
            background: #fffbf0;
            border: 1px solid #ffc107;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .note-box strong {
            color: #856404;
        }
        .note-box p {
            margin: 5px 0;
            color: #333;
        }
        .next-steps {
            background: #f0f8ff;
            border: 1px solid #2196F3;
            border-left: 4px solid #2196F3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .next-steps h3 {
            margin-top: 0;
            color: #1976D2;
            font-size: 17px;
        }
        .next-steps ul {
            margin: 10px 0;
            padding-left: 25px;
        }
        .next-steps li {
            margin: 8px 0;
            color: #333;
        }
        .button {
            display: inline-block;
            padding: 12px 30px;
            background: #667eea;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            margin: 10px 5px;
        }
        .contact-info {
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            padding: 20px;
            border-radius: 6px;
            margin: 20px 0;
            text-align: center;
        }
        .contact-info p {
            margin: 5px 0;
            color: #333;
        }
        .contact-info strong {
            color: #667eea;
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
        .footer strong {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>THÔNG BÁO LÊN LỊCH CẤP PHÁT</h1>
            <p>Yêu cầu của bạn đã được xác nhận</p>
        </div>

        <div class="content-box">
            <div class="message-box">
                <h2>Yêu cầu đã được lên lịch</h2>
                <p>Yêu cầu cấp phát của bạn đã được quản lý kho xác nhận và lên lịch cấp phát</p>
            </div>

            <div class="schedule-highlight">
                <div class="label">NGÀY GIỜ CẤP PHÁT DỰ KIẾN</div>
                <div class="datetime">{{ request.scheduled_date|date:"d/m/Y" }}</div>
                <div class="datetime" style="font-size: 24px;">{{ request.scheduled_date|date:"H:i" }}</div>
            </div>

            <div class="info-box">
                <h3>THÔNG TIN YÊU CẦU</h3>
                <div class="info-row">
                    <span class="label">Mã yêu cầu:</span>
                    <span class="value"><strong>#{{ request.request_code }}</strong></span>
                </div>
                <div class="info-row">
                    <span class="label">Người yêu cầu:</span>
                    <span class="value">{{ request.requester.get_full_name }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Quản lý kho:</span>
                    <span class="value">{{ warehouse_manager.get_full_name }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày tạo yêu cầu:</span>
                    <span class="value">{{ request.created_at|date:"d/m/Y H:i" }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày phê duyệt:</span>
                    <span class="value">{{ request.approval_date|date:"d/m/Y H:i" }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="value"><span class="status-badge">Đã lên lịch</span></span>
                </div>
            </div>

            <h3 style="color: #667eea; margin-top: 30px; border-bottom: 2px solid #667eea; padding-bottom: 10px;">DANH SÁCH VẬT TƯ</h3>
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
                        <td style="text-align: center;"><strong style="color: #667eea; font-size: 16px;">{{ employee_product.quantity }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            {% if request.schedule_notes %}
            <div class="note-box">
                <strong>Ghi chú từ quản lý kho:</strong>
                <p>{{ request.schedule_notes }}</p>
            </div>
            {% endif %}

            <div class="next-steps">
                <h3>CÁC BƯỚC TIẾP THEO</h3>
                <ul>
                    <li>Vui lòng có mặt tại kho vào đúng thời gian đã lên lịch</li>
                    <li>Mang theo giấy tờ tùy thân để xác nhận</li>
                    <li>Chuẩn bị phương tiện vận chuyển nếu cần</li>
                    <li>Kiểm tra kỹ vật tư trước khi nhận</li>
                    <li>Ký xác nhận vào phiếu xuất kho</li>
                </ul>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/inventory/requests/{{ request.id }}/" class="button">Xem chi tiết yêu cầu</a>
            </div>

            <div class="contact-info">
                <p><strong>CẦN HỖ TRỢ?</strong></p>
                <p>Liên hệ quản lý kho: <strong>{{ warehouse_manager.get_full_name }}</strong></p>
                <p>Email: {{ warehouse_manager.email }}</p>
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
            ''',
            'subject': '[Lên lịch] Yêu cầu #{{ request.request_code }} đã được lên lịch cấp phát',
            'is_active': True
        }

        template, created = EmailTemplate.objects.update_or_create(
            code=warehouse_scheduled_template['code'],
            defaults=warehouse_scheduled_template
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Đã tạo template: {template.code}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Đã cập nhật template: {template.code}'))
