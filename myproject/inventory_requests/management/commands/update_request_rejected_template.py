from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Cập nhật template email request_rejected với thiết kế đẹp và chuyên nghiệp'

    def handle(self, *args, **options):
        # Template: Thông báo yêu cầu bị từ chối
        request_rejected_template = {
            'code': 'request_rejected',
            'name': 'Yêu cầu bị từ chối',
            'subject': 'Yêu cầu #{request.request_code} đã bị từ chối',
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
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
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
            color: #dc2626;
        }
        .rejected-message {
            background: #fee2e2;
            border-left: 4px solid #ef4444;
            padding: 20px;
            margin: 25px 0;
            border-radius: 6px;
        }
        .rejected-message h2 {
            margin: 0 0 10px 0;
            color: #991b1b;
            font-size: 20px;
        }
        .rejected-message p {
            margin: 5px 0;
            color: #b91c1c;
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
            border-bottom: 2px solid #ef4444;
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
            color: #dc2626;
            font-size: 16px;
        }
        .status-badge { 
            display: inline-block; 
            padding: 6px 16px; 
            border-radius: 20px; 
            font-size: 13px; 
            font-weight: 600;
            background: #fee2e2;
            color: #991b1b;
        }
        .rejection-reason-box {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 20px;
            margin: 25px 0;
            border-radius: 6px;
        }
        .rejection-reason-box h3 {
            margin: 0 0 10px 0;
            color: #92400e;
            font-size: 17px;
        }
        .rejection-reason-box .reason-text {
            background: white;
            padding: 15px;
            border-radius: 6px;
            color: #78350f;
            font-size: 15px;
            font-style: italic;
            border: 1px solid #fbbf24;
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
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
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
            background: #e0f2fe;
            border-left: 4px solid #0284c7;
            padding: 20px;
            margin: 25px 0;
            border-radius: 6px;
        }
        .next-steps h3 {
            margin: 0 0 15px 0;
            color: #075985;
            font-size: 17px;
        }
        .next-steps ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .next-steps li {
            margin: 8px 0;
            color: #0c4a6e;
            font-size: 14px;
        }
        .button-container {
            text-align: center;
            margin: 30px 0;
        }
        .button { 
            display: inline-block; 
            padding: 14px 35px; 
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white !important; 
            text-decoration: none; 
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
            transition: all 0.3s;
            margin: 0 10px;
        }
        .button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(99, 102, 241, 0.4);
        }
        .button.secondary {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
        }
        .button.secondary:hover {
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
            color: #ef4444;
        }
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, #e5e7eb, transparent);
            margin: 25px 0;
        }
        .contact-info {
            background: #f0fdfa;
            border: 1px solid #99f6e4;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
            text-align: center;
        }
        .contact-info p {
            margin: 5px 0;
            color: #115e59;
            font-size: 14px;
        }
        .contact-info strong {
            color: #0d9488;
            font-size: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">X</div>
            <h1>Yêu cầu bị từ chối</h1>
            <p>Yêu cầu cấp phát của bạn không được chấp thuận</p>
        </div>
        
        <div class="content">
            <div class="greeting">
                Kính gửi <strong>{{ user.get_full_name }}</strong>,
            </div>
            
            <div class="rejected-message">
                <h2>Thông báo từ chối</h2>
                <p>Rất tiếc, yêu cầu cấp phát của bạn đã bị <strong>{{ approver.get_full_name }}</strong> từ chối.</p>
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
                    <span class="value"><span class="status-badge">Bị từ chối</span></span>
                </div>
                <div class="info-row">
                    <span class="label">Người từ chối:</span>
                    <span class="value">{{ approver.get_full_name }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày từ chối:</span>
                    <span class="value">{{ request.approved_date|date:"d/m/Y H:i" }}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày tạo yêu cầu:</span>
                    <span class="value">{{ request.created_at|date:"d/m/Y H:i" }}</span>
                </div>
            </div>

            <div class="rejection-reason-box">
                <h3>Lý do từ chối</h3>
                <div class="reason-text">
                    {{ rejection_reason }}
                </div>
            </div>

            <div class="info-box">
                <h3>Danh sách sản phẩm trong yêu cầu</h3>
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
                                <td><strong style="color: #dc2626; font-size: 16px;">{{ employee_product.quantity }}</strong></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="next-steps">
                <h3>Các bước tiếp theo</h3>
                <ul>
                    <li>Xem lại lý do từ chối và thông tin yêu cầu của bạn</li>
                    <li>Liên hệ với <strong>{{ approver.get_full_name }}</strong> để hiểu rõ hơn về lý do từ chối</li>
                    <li>Bạn có thể <strong>chỉnh sửa</strong> và <strong>gửi lại</strong> yêu cầu sau khi điều chỉnh</li>
                    <li>Hoặc tạo một yêu cầu mới với thông tin phù hợp hơn</li>
                </ul>
            </div>

            <div class="contact-info">
                <p><strong>Cần hỗ trợ?</strong></p>
                <p>Liên hệ người quản lý: <strong>{{ approver.get_full_name }}</strong></p>
                {% if approver.email %}
                <p>Email: <strong>{{ approver.email }}</strong></p>
                {% endif %}
            </div>

            <div class="divider"></div>

            <div class="button-container">
                <a href="http://127.0.0.1:8000/inventory/requests/{{ request.id }}/" class="button">
                    Xem chi tiết yêu cầu
                </a>
                <a href="http://127.0.0.1:8000/inventory/requests/create/" class="button secondary">
                    Tạo yêu cầu mới
                </a>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Email tự động từ hệ thống GA Inventory Management</strong></p>
            <p>Nếu có bất kỳ thắc mắc nào, vui lòng liên hệ với người quản lý của bạn</p>
            <p style="margin-top: 15px; color: #9ca3af; font-size: 12px;">
                2025 GA Corporation. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
            ''',
            'is_active': True,
            'is_html': True,
            'type': 'request_rejected',
            'description': 'Template email thông báo yêu cầu cấp phát bị từ chối - Thiết kế đẹp và chuyên nghiệp với thông tin đầy đủ'
        }

        # Cập nhật template
        template, created = EmailTemplate.objects.update_or_create(
            code=request_rejected_template['code'],
            defaults=request_rejected_template
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Đã tạo mới template: {template.code}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Đã cập nhật template: {template.code}'))
        
        self.stdout.write(self.style.SUCCESS(f'Template "{template.name}" đã sẵn sàng sử dụng!'))
