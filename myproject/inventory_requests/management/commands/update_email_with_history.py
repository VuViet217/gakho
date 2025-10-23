from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Cập nhật email template request_created và pending_approval với cột lịch sử lấy hàng'

    def handle(self, *args, **kwargs):
        templates = [
            # Mẫu thông báo tạo yêu cầu mới - CÓ LỊCH SỬ
            {
                'code': 'request_created',
                'type': 'notification',
                'name': 'Thông báo tạo yêu cầu mới',
                'subject': 'Yêu cầu cấp phát #{{ request.request_code }} đã được tạo thành công',
                'content': '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yêu cầu cấp phát mới</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 900px;
            margin: 20px auto;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }
        .content {
            padding: 30px;
        }
        .greeting {
            font-size: 16px;
            margin-bottom: 20px;
            color: #555;
        }
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .info-box h3 {
            margin-top: 0;
            color: #667eea;
            font-size: 18px;
        }
        .info-row {
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .info-label {
            font-weight: 600;
            width: 180px;
            color: #555;
        }
        .info-value {
            flex: 1;
            color: #333;
        }
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            background: #ffc107;
            color: #000;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }
        .table-container {
            margin: 30px 0;
            overflow-x: auto;
        }
        .table-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background: white;
        }
        thead {
            background: #667eea;
            color: white;
        }
        th {
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
        }
        td {
            padding: 12px 8px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 13px;
        }
        tbody tr:hover {
            background-color: #f8f9fa;
        }
        tbody tr:last-child td {
            border-bottom: none;
        }
        .text-right {
            text-align: right;
        }
        .text-center {
            text-align: center;
        }
        .history-badge {
            display: inline-block;
            padding: 3px 8px;
            background: #28a745;
            color: white;
            border-radius: 3px;
            font-size: 11px;
            margin-top: 3px;
        }
        .no-history {
            color: #999;
            font-size: 11px;
        }
        .note {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #777;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
        }
        .footer p {
            margin: 5px 0;
        }
        .button {
            display: inline-block;
            padding: 12px 30px;
            background: #667eea;
            color: white !important;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            margin: 20px 0;
            transition: background 0.3s;
        }
        .button:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Yêu cầu cấp phát đã được tạo thành công</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Kính gửi <strong>{{ user.get_full_name }}</strong>,
            </div>
            
            <p>Yêu cầu cấp phát của bạn đã được tạo thành công và đã được gửi đến người phê duyệt để xem xét.</p>
            
            <div class="info-box">
                <h3>Thông tin yêu cầu</h3>
                <div class="info-row">
                    <div class="info-label">Mã yêu cầu:</div>
                    <div class="info-value"><strong>{{ request.request_code }}</strong></div>
                </div>
                <div class="info-row">
                    <div class="info-label">Tiêu đề:</div>
                    <div class="info-value">{{ request.title }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Trạng thái:</div>
                    <div class="info-value"><span class="status-badge">Chờ phê duyệt</span></div>
                </div>
                <div class="info-row">
                    <div class="info-label">Ngày tạo:</div>
                    <div class="info-value">{{ request.created_at|date:"d/m/Y H:i" }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Ngày mong muốn nhận:</div>
                    <div class="info-value">{{ request.expected_date|date:"d/m/Y" }}</div>
                </div>
                {% if request.notes %}
                <div class="info-row">
                    <div class="info-label">Ghi chú:</div>
                    <div class="info-value">{{ request.notes }}</div>
                </div>
                {% endif %}
            </div>
            
            <div class="table-container">
                <div class="table-title">Chi tiết phân bổ sản phẩm cho nhân viên</div>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 4%;">#</th>
                            <th style="width: 22%;">Nhân viên</th>
                            <th style="width: 25%;">Sản phẩm</th>
                            <th style="width: 10%;" class="text-center">SL</th>
                            <th style="width: 22%;">Lần lấy gần nhất</th>
                            <th style="width: 17%;">Ghi chú</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in employee_products_with_history %}
                        <tr>
                            <td class="text-center">{{ forloop.counter }}</td>
                            <td>
                                <strong>{{ item.employee_product.employee.full_name }}</strong><br>
                                <small style="color: #777;">{{ item.employee_product.employee.employee_id }}</small>
                            </td>
                            <td>
                                <strong>{{ item.employee_product.product.name }}</strong><br>
                                <small style="color: #777;">Mã: {{ item.employee_product.product.product_code }}</small>
                            </td>
                            <td class="text-center"><strong>{{ item.employee_product.quantity }}</strong></td>
                            <td>
                                {% if item.last_delivery %}
                                <small>
                                    📅 {{ item.last_delivery.request.completed_date|date:"d/m/Y" }}<br>
                                    📦 SL: {{ item.last_delivery.quantity }}<br>
                                    <span class="history-badge">{{ item.last_delivery.request.request_code }}</span>
                                </small>
                                {% else %}
                                <small class="no-history">Chưa từng lấy</small>
                                {% endif %}
                            </td>
                            <td><small>{{ item.employee_product.notes|default:"—" }}</small></td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center" style="color: #999;">Chưa có phân bổ nào</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <div class="note">
                <strong>Lưu ý:</strong> Bạn có thể theo dõi trạng thái yêu cầu của mình trong phần <strong>"Yêu cầu của tôi"</strong> trên hệ thống. Bạn sẽ nhận được thông báo qua email khi yêu cầu được phê duyệt hoặc từ chối.
            </div>
            
            <div style="text-align: center;">
                <a href="#" class="button">Xem chi tiết yêu cầu</a>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Hệ thống Quản lý Kho</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p style="color: #999; font-size: 12px;">(c) 2025 GA Inventory Management System</p>
        </div>
    </div>
</body>
</html>''',
                'is_html': True,
                'is_active': True
            },
            
            # Mẫu thông báo chờ phê duyệt gửi đến quản lý - CÓ LỊCH SỬ
            {
                'code': 'pending_approval',
                'type': 'notification',
                'name': 'Thông báo yêu cầu chờ phê duyệt',
                'subject': '[Cần phê duyệt] Yêu cầu cấp phát #{{ request.request_code }}',
                'content': '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yêu cầu chờ phê duyệt</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 900px;
            margin: 20px auto;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }
        .urgent-badge {
            display: inline-block;
            background: #fff;
            color: #f5576c;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 700;
            margin-top: 10px;
        }
        .content {
            padding: 30px;
        }
        .greeting {
            font-size: 16px;
            margin-bottom: 20px;
            color: #555;
        }
        .alert-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .alert-box strong {
            color: #856404;
        }
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #f5576c;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .info-box h3 {
            margin-top: 0;
            color: #f5576c;
            font-size: 18px;
        }
        .info-row {
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .info-label {
            font-weight: 600;
            width: 180px;
            color: #555;
        }
        .info-value {
            flex: 1;
            color: #333;
        }
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            background: #ffc107;
            color: #000;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }
        .table-container {
            margin: 30px 0;
            overflow-x: auto;
        }
        .table-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f5576c;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background: white;
        }
        thead {
            background: #f5576c;
            color: white;
        }
        th {
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
        }
        td {
            padding: 12px 8px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 13px;
        }
        tbody tr:hover {
            background-color: #fff5f5;
        }
        tbody tr:last-child td {
            border-bottom: none;
        }
        .text-right {
            text-align: right;
        }
        .text-center {
            text-align: center;
        }
        .history-badge {
            display: inline-block;
            padding: 3px 8px;
            background: #28a745;
            color: white;
            border-radius: 3px;
            font-size: 11px;
            margin-top: 3px;
        }
        .no-history {
            color: #999;
            font-size: 11px;
        }
        .action-buttons {
            text-align: center;
            margin: 30px 0;
        }
        .button {
            display: inline-block;
            padding: 14px 35px;
            margin: 0 10px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s;
            font-size: 16px;
        }
        .button-approve {
            background: #28a745;
            color: white !important;
        }
        .button-approve:hover {
            background: #218838;
        }
        .button-view {
            background: #007bff;
            color: white !important;
        }
        .button-view:hover {
            background: #0056b3;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #777;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
        }
        .footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Yêu cầu cấp phát cần phê duyệt</h1>
            <span class="urgent-badge">CẦN XỬ LÝ</span>
        </div>
        
        <div class="content">
            <div class="greeting">
                Kính gửi <strong>{{ manager.get_full_name }}</strong>,
            </div>
            
            <div class="alert-box">
                <strong>Bạn có một yêu cầu cấp phát mới cần phê duyệt!</strong><br>
                Yêu cầu từ <strong>{{ user.get_full_name }}</strong> ({{ user.email }}) đang chờ bạn xem xét và phê duyệt.
            </div>
            
            <div class="info-box">
                <h3>Thông tin yêu cầu</h3>
                <div class="info-row">
                    <div class="info-label">Mã yêu cầu:</div>
                    <div class="info-value"><strong>{{ request.request_code }}</strong></div>
                </div>
                <div class="info-row">
                    <div class="info-label">Tiêu đề:</div>
                    <div class="info-value">{{ request.title }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Trạng thái:</div>
                    <div class="info-value"><span class="status-badge">Chờ phê duyệt</span></div>
                </div>
                <div class="info-row">
                    <div class="info-label">Người yêu cầu:</div>
                    <div class="info-value">{{ user.get_full_name }} ({{ user.email }})</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Ngày tạo:</div>
                    <div class="info-value">{{ request.created_at|date:"d/m/Y H:i" }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Ngày mong muốn nhận:</div>
                    <div class="info-value"><strong>{{ request.expected_date|date:"d/m/Y" }}</strong></div>
                </div>
                {% if request.notes %}
                <div class="info-row">
                    <div class="info-label">Ghi chú:</div>
                    <div class="info-value">{{ request.notes }}</div>
                </div>
                {% endif %}
            </div>
            
            <div class="table-container">
                <div class="table-title">Chi tiết phân bổ sản phẩm cho nhân viên (có lịch sử lấy hàng)</div>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 4%;">#</th>
                            <th style="width: 22%;">Nhân viên</th>
                            <th style="width: 25%;">Sản phẩm</th>
                            <th style="width: 10%;" class="text-center">SL</th>
                            <th style="width: 22%;">Lần lấy gần nhất</th>
                            <th style="width: 17%;">Ghi chú</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in employee_products_with_history %}
                        <tr>
                            <td class="text-center">{{ forloop.counter }}</td>
                            <td>
                                <strong>{{ item.employee_product.employee.full_name }}</strong><br>
                                <small style="color: #777;">{{ item.employee_product.employee.employee_id }}</small>
                            </td>
                            <td>
                                <strong>{{ item.employee_product.product.name }}</strong><br>
                                <small style="color: #777;">Mã: {{ item.employee_product.product.product_code }}</small>
                            </td>
                            <td class="text-center"><strong>{{ item.employee_product.quantity }}</strong></td>
                            <td>
                                {% if item.last_delivery %}
                                <small>
                                    📅 {{ item.last_delivery.request.completed_date|date:"d/m/Y" }}<br>
                                    📦 SL: {{ item.last_delivery.quantity }}<br>
                                    <span class="history-badge">{{ item.last_delivery.request.request_code }}</span>
                                </small>
                                {% else %}
                                <small class="no-history">Chưa từng lấy</small>
                                {% endif %}
                            </td>
                            <td><small>{{ item.employee_product.notes|default:"—" }}</small></td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center" style="color: #999;">Chưa có phân bổ nào</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <div class="action-buttons">
                <a href="#" class="button button-approve">PHÊ DUYỆT YÊU CẦU</a>
                <a href="#" class="button button-view">XEM CHI TIẾT</a>
            </div>
            
            <p style="text-align: center; color: #777; font-size: 14px; margin-top: 20px;">
                Hoặc đăng nhập vào hệ thống và truy cập phần <strong>"Phê duyệt của tôi"</strong> để xử lý yêu cầu này.
            </p>
        </div>
        
        <div class="footer">
            <p><strong>Hệ thống Quản lý Kho</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p style="color: #999; font-size: 12px;">(c) 2025 GA Inventory Management System</p>
        </div>
    </div>
</body>
</html>''',
                'is_html': True,
                'is_active': True
            },
        ]
        
        for template_data in templates:
            template, created = EmailTemplate.objects.update_or_create(
                code=template_data['code'],
                defaults=template_data
            )
            status = 'Tạo mới' if created else 'Cập nhật'
            self.stdout.write(self.style.SUCCESS(f"{status} mẫu email '{template.name}' với cột lịch sử"))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Đã cập nhật 2 email template với cột "Lần lấy gần nhất"'))
