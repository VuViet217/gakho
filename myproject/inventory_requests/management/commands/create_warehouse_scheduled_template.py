from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate


class Command(BaseCommand):
    help = 'Tạo email template cho thông báo đã lên lịch cấp phát'

    def handle(self, *args, **kwargs):
        warehouse_scheduled_template = {
            'code': 'warehouse_scheduled',
            'name': 'Thông báo đã lên lịch cấp phát',
            'description': 'Email gửi cho người yêu cầu khi yêu cầu đã được lên lịch cấp phát bởi quản lý kho',
            'subject': 'Đã lên lịch cấp phát #{{ request.request_code }}',
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
            border-bottom: 3px solid #ff9800;
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
            border-left: 4px solid #ff9800;
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
            color: #ff9800;
            font-size: 16px;
            border-bottom: 2px solid #ff9800;
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
        .schedule-highlight {
            background: #fff3e0;
            border: 2px solid #ff9800;
            border-left: 4px solid #ff9800;
            padding: 25px;
            margin: 25px 0;
            border-radius: 6px;
        }
        .schedule-highlight h3 {
            margin-top: 0;
            color: #e65100;
            font-size: 18px;
        }
        .schedule-datetime {
            background: #ffffff;
            border: 2px solid #ff9800;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            margin: 15px 0;
        }
        .schedule-datetime .date {
            font-size: 24px;
            font-weight: 700;
            color: #ff9800;
            margin: 0;
        }
        .schedule-datetime .time {
            font-size: 18px;
            color: #666;
            margin: 5px 0 0 0;
        }
        .product-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border: 1px solid #e0e0e0;
        }
        .product-table thead {
            background: #ff9800;
        }
        .product-table th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            color: #ffffff;
            border: 1px solid #f57c00;
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
            background: #ff9800;
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
            <h1>ĐÃ LÊN LỊCH CẤP PHÁT</h1>
            <p>Mã yêu cầu: #{{ request.request_code }}</p>
        </div>

        <div class="content-box">
            <div class="message-box">
                <h2>Xin chào {{ request.requester.get_full_name }},</h2>
                <p>Yêu cầu cấp phát vật tư của bạn đã được lên lịch bởi {{ warehouse_manager.get_full_name }}.</p>
            </div>

            <div class="schedule-highlight">
                <h3>THỜI GIAN CẤP PHÁT ĐÃ ĐẶT LỊCH</h3>
                <div class="schedule-datetime">
                    <p class="date">{{ scheduled_date|date:"d/m/Y" }}</p>
                    <p class="time">{{ scheduled_date|date:"H:i" }}</p>
                </div>
                <p style="text-align: center; color: #666; margin: 10px 0; font-size: 14px;">
                    Vui lòng đến nhận vật tư đúng giờ đã định
                </p>
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
                    <span class="label">Người lên lịch:</span>
                    <span class="value">{{ warehouse_manager.get_full_name }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày lên lịch:</span>
                    <span class="value">{{ request.scheduled_at|date:"d/m/Y H:i" }}</span>
                </div>
            </div>

            <h3 style="color: #ff9800; margin-top: 30px; border-bottom: 2px solid #ff9800; padding-bottom: 10px;">DANH SÁCH VẬT TƯ SẼ CẤP PHÁT</h3>
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
                        <td style="text-align: center;"><strong style="color: #ff9800; font-size: 16px;">{{ employee_product.quantity }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            {% if schedule_notes %}
            <div style="background: #fff3e0; border: 1px solid #ff9800; border-left: 4px solid #ff9800; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <strong style="color: #e65100;">Ghi chú từ quản lý kho:</strong>
                <p style="margin: 5px 0; color: #333;">{{ schedule_notes }}</p>
            </div>
            {% endif %}

            <div style="background: #e8f4f8; border: 1px solid #2196F3; border-left: 4px solid #2196F3; padding: 20px; margin: 20px 0; border-radius: 4px;">
                <h3 style="margin-top: 0; color: #1976D2; font-size: 16px;">LƯU Ý QUAN TRỌNG</h3>
                <ul style="margin: 10px 0; padding-left: 25px;">
                    <li style="margin: 8px 0; color: #333;">Vui lòng đến nhận hàng đúng thời gian đã định</li>
                    <li style="margin: 8px 0; color: #333;">Mang theo giấy tờ xác minh danh tính khi nhận hàng</li>
                    <li style="margin: 8px 0; color: #333;">Kiểm tra số lượng và chất lượng vật tư trước khi nhận</li>
                    <li style="margin: 8px 0; color: #333;">Nếu có vấn đề, liên hệ ngay với bộ phận kho</li>
                </ul>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/inventory/requests/{{ request.id }}/" class="button" style="background: #ff9800;">Xem chi tiết yêu cầu</a>
            </div>
        </div>

        <div class="footer">
            <p><strong>GA Inventory Management System</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p>Liên hệ bộ phận kho: warehouse@ovnc.com | Hotline: 1900 xxxx</p>
            <p>&copy; 2025 GA. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
            '''
        }

        template, created = EmailTemplate.objects.update_or_create(
            code='warehouse_scheduled',
            defaults=warehouse_scheduled_template
        )

        action = 'Đã tạo' if created else 'Đã cập nhật'
        self.stdout.write(self.style.SUCCESS(f'{action} template: warehouse_scheduled'))
