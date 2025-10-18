from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Cập nhật template email request_approved với thiết kế đẹp và chuyên nghiệp'

    def handle(self, *args, **options):
        # Template: Thông báo yêu cầu đã được phê duyệt
        request_approved_template = {
            'code': 'request_approved',
            'name': 'Yêu cầu đã được phê duyệt',
            'subject': 'Yêu cầu #{request.request_code} đã được phê duyệt',
            'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        .container { 
            max-width: 650px; 
            margin: 30px auto; 
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header { 
            background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
            color: white; 
            padding: 40px 30px; 
            text-align: center;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 600;
        }
        .header .icon {
            font-size: 48px;
            margin-bottom: 10px;
        }
        .header p {
            margin: 5px 0;
            font-size: 16px;
            opacity: 0.95;
        }
        .content { 
            padding: 40px 30px;
        }
        .greeting {
            font-size: 18px;
            color: #1f2937;
            margin-bottom: 20px;
        }
        .greeting strong {
            color: #10b981;
        }
        .success-message {
            background: #d1fae5;
            border-left: 4px solid #10b981;
            padding: 20px;
            margin: 25px 0;
            border-radius: 6px;
        }
        .success-message h2 {
            margin: 0 0 10px 0;
            color: #065f46;
            font-size: 20px;
        }
        .success-message p {
            margin: 5px 0;
            color: #047857;
            font-size: 15px;
        }
        .info-box { 
            background: #f9fafb; 
            padding: 25px; 
            margin: 25px 0; 
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }
        .info-box h3 {
            margin: 0 0 15px 0;
            color: #1f2937;
            font-size: 18px;
            border-bottom: 2px solid #10b981;
            padding-bottom: 10px;
        }
        .info-row { 
            display: flex;
            margin: 12px 0;
            padding: 8px 0;
        }
        .label { 
            font-weight: 600; 
            color: #4b5563;
            min-width: 160px;
            font-size: 14px;
        }
        .value { 
            color: #1f2937;
            flex: 1;
            font-size: 14px;
        }
        .value strong {
            color: #10b981;
            font-size: 16px;
        }
        .status-badge { 
            display: inline-block; 
            padding: 6px 16px; 
            border-radius: 20px; 
            font-size: 13px; 
            font-weight: 600;
            background: #d1fae5;
            color: #065f46;
        }
        .table-container {
            margin: 20px 0;
            overflow-x: auto;
        }
        table { 
            width: 100%; 
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
        }
        th { 
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white; 
            padding: 14px 12px; 
            text-align: left; 
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        td { 
            padding: 14px 12px; 
            border-bottom: 1px solid #e5e7eb;
            font-size: 14px;
        }
        tr:last-child td {
            border-bottom: none;
        }
        tr:hover { 
            background: #f9fafb;
        }
        .product-code { 
            font-family: 'Courier New', monospace; 
            background: #dbeafe; 
            padding: 4px 10px; 
            border-radius: 4px; 
            font-weight: 600;
            color: #1e40af;
            font-size: 13px;
        }
        .next-steps {
            background: #fff7ed;
            border-left: 4px solid #f59e0b;
            padding: 20px;
            margin: 25px 0;
            border-radius: 6px;
        }
        .next-steps h3 {
            margin: 0 0 15px 0;
            color: #92400e;
            font-size: 17px;
        }
        .next-steps ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .next-steps li {
            margin: 8px 0;
            color: #b45309;
            font-size: 14px;
        }
        .button-container {
            text-align: center;
            margin: 30px 0;
        }
        .button { 
            display: inline-block; 
            padding: 14px 35px; 
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white !important; 
            text-decoration: none; 
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
            transition: all 0.3s;
        }
        .button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(16, 185, 129, 0.4);
        }
        .footer { 
            background: #f9fafb;
            text-align: center; 
            color: #6b7280; 
            font-size: 13px; 
            padding: 25px 30px;
            border-top: 1px solid #e5e7eb;
        }
        .footer p {
            margin: 8px 0;
        }
        .footer strong {
            color: #10b981;
        }
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, #e5e7eb, transparent);
            margin: 25px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">OK</div>
            <h1>Yêu cầu đã được phê duyệt</h1>
            <p>Chúc mừng! Yêu cầu cấp phát của bạn đã được chấp thuận</p>
        </div>
        
        <div class="content">
            <div class="greeting">
                Kính gửi <strong>{{ user.get_full_name }}</strong>,
            </div>
            
            <div class="success-message">
                <h2>Tin tốt lành!</h2>
                <p>Yêu cầu cấp phát của bạn đã được <strong>{{ approver.get_full_name }}</strong> phê duyệt thành công.</p>
            </div>

            <div class="info-box">
                <h3>Thông tin yêu cầu</h3>
                <div class="info-row">
                    <span class="label">Mã yêu cầu:</span>
                    <span class="value"><strong>{{ request.request_code }}</strong></span>
                </div>
                <div class="info-row">
                    <span class="label">Tiêu đề:</span>
                    <span class="value">{{ request.title }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="value"><span class="status-badge">Đã phê duyệt</span></span>
                </div>
                <div class="info-row">
                    <span class="label">Người phê duyệt:</span>
                    <span class="value">{{ approver.get_full_name }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày phê duyệt:</span>
                    <span class="value">{{ request.approved_date|date:"d/m/Y H:i" }}</span>
                </div>
                {% if request.note %}
                <div class="info-row">
                    <span class="label">Ghi chú:</span>
                    <span class="value">{{ request.note }}</span>
                </div>
                {% endif %}
            </div>

            <div class="info-box">
                <h3>Danh sách sản phẩm được cấp phát</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Nhân viên</th>
                                <th>Sản phẩm</th>
                                <th>Số lượng</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for employee_product in request.employee_products.all %}
                            <tr>
                                <td>
                                    <strong>{{ employee_product.employee.full_name }}</strong><br>
                                    <small style="color: #6b7280;">{{ employee_product.employee.department.name|default:"N/A" }}</small>
                                </td>
                                <td>
                                    <span class="product-code">{{ employee_product.product.product_code }}</span><br>
                                    <span style="color: #4b5563;">{{ employee_product.product.name }}</span>
                                </td>
                                <td><strong style="color: #10b981; font-size: 16px;">{{ employee_product.quantity }}</strong></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="next-steps">
                <h3>Các bước tiếp theo</h3>
                <ul>
                    <li>Yêu cầu của bạn đã được chuyển đến <strong>bộ phận kho</strong> để xử lý</li>
                    <li>Bộ phận kho sẽ lên lịch cấp phát trong thời gian sớm nhất</li>
                    <li>Bạn sẽ nhận được email thông báo khi có <strong>lịch hẹn cấp phát</strong></li>
                    <li>Vui lòng theo dõi email để biết thông tin chi tiết về lịch nhận hàng</li>
                </ul>
            </div>

            <div class="divider"></div>

            <div class="button-container">
                <a href="http://127.0.0.1:8000/inventory/requests/{{ request.id }}/" class="button">
                    Xem chi tiết yêu cầu
                </a>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Email tự động từ hệ thống OVNC Inventory Management</strong></p>
            <p>Nếu có bất kỳ thắc mắc nào, vui lòng liên hệ bộ phận kho hoặc người phê duyệt</p>
            <p style="margin-top: 15px; color: #9ca3af; font-size: 12px;">
                © 2025 OVNC Corporation. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
            ''',
            'is_active': True,
            'is_html': True,
            'type': 'request_approved',
            'description': 'Template email thông báo yêu cầu cấp phát đã được phê duyệt - Thiết kế đẹp và chuyên nghiệp'
        }

        # Cập nhật template
        template, created = EmailTemplate.objects.update_or_create(
            code=request_approved_template['code'],
            defaults=request_approved_template
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Đã tạo mới template: {template.code}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Đã cập nhật template: {template.code}'))
        
        self.stdout.write(self.style.SUCCESS(f'Template "{template.name}" đã sẵn sàng sử dụng!'))
