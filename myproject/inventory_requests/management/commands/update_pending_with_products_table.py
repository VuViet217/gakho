from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Cập nhật email pending_approval với bảng chi tiết sản phẩm có tiếng Việt dấu'

    def handle(self, *args, **kwargs):
        template_data = {
            'code': 'pending_approval',
            'type': 'pending_approval',
            'name': 'Thông báo yêu cầu chờ phê duyệt',
            'subject': '[Cần phê duyệt] Yêu cầu cấp phát #{{ request_id }}',
            'content': '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yêu cầu chờ phê duyệt</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 0; }
        .container { max-width: 900px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; }
        .header { background: #dc3545; color: #333; padding: 25px; text-align: center; border-bottom: 3px solid #c82333; }
        .header h1 { margin: 0; font-size: 22px; font-weight: 600; color: #fff; }
        .urgent-badge { display: inline-block; background: #fff; color: #dc3545; padding: 6px 18px; border-radius: 15px; font-size: 13px; font-weight: 700; margin-top: 8px; border: 2px solid #fff; }
        .content { padding: 25px; }
        .greeting { font-size: 15px; margin-bottom: 18px; color: #555; }
        .alert-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 18px; margin: 18px 0; border-radius: 4px; }
        .alert-box strong { color: #856404; }
        .info-box { background: #f8f9fa; border: 1px solid #dee2e6; padding: 18px; margin: 18px 0; border-radius: 4px; }
        .info-box h3 { margin-top: 0; color: #dc3545; font-size: 17px; margin-bottom: 12px; }
        .info-row { padding: 8px 0; border-bottom: 1px solid #e9ecef; }
        .info-row:last-child { border-bottom: none; }
        .info-label { font-weight: 600; color: #555; display: inline-block; width: 180px; }
        .info-value { color: #333; display: inline-block; }
        .status-badge { display: inline-block; padding: 4px 12px; background: #ffc107; color: #000; border-radius: 12px; font-size: 13px; font-weight: 600; }
        .table-container { margin: 25px 0; overflow-x: auto; }
        .table-title { font-size: 17px; font-weight: 600; color: #333; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #dc3545; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; background: white; border: 1px solid #dee2e6; }
        thead { background: #dc3545; color: white; }
        th { padding: 12px 8px; text-align: left; font-weight: 600; font-size: 13px; border: 1px solid #c82333; }
        td { padding: 12px 8px; border: 1px solid #dee2e6; font-size: 13px; }
        tbody tr:nth-child(even) { background-color: #f8f9fa; }
        tbody tr:hover { background-color: #fff5f5; }
        .text-center { text-align: center; }
        .history-badge { display: inline-block; padding: 3px 8px; background: #28a745; color: white; border-radius: 3px; font-size: 11px; margin-top: 3px; }
        .no-history { color: #999; font-size: 11px; font-style: italic; }
        .action-buttons { text-align: center; margin: 28px 0; padding: 20px; background: #f8f9fa; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; margin: 0 8px; text-decoration: none; border-radius: 4px; font-weight: 600; font-size: 14px; border: 2px solid transparent; color: white; }
        .button-approve { background: #28a745; border-color: #28a745; }
        .button-view { background: #007bff; border-color: #007bff; }
        .footer { background: #f8f9fa; padding: 18px 25px; text-align: center; color: #777; font-size: 13px; border-top: 1px solid #dee2e6; }
        .footer p { margin: 4px 0; }
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
                Kính gửi <strong>{{ approver_name }}</strong>,
            </div>
            
            <div class="alert-box">
                <strong>Bạn có một yêu cầu cấp phát mới cần phê duyệt!</strong><br>
                Yêu cầu từ <strong>{{ requester_name }}</strong> ({{ requester_email }}) đang chờ bạn xem xét và phê duyệt.
            </div>
            
            <div class="info-box">
                <h3>Thông tin yêu cầu</h3>
                <div class="info-row">
                    <span class="info-label">Mã yêu cầu:</span>
                    <span class="info-value"><strong>#{{ request_id }}</strong></span>
                </div>
                <div class="info-row">
                    <span class="info-label">Trạng thái:</span>
                    <span class="info-value"><span class="status-badge">Chờ phê duyệt</span></span>
                </div>
                <div class="info-row">
                    <span class="info-label">Người yêu cầu:</span>
                    <span class="info-value">{{ requester_name }} ({{ requester_email }})</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Ngày tạo:</span>
                    <span class="info-value">{{ created_at }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Ngày mong muốn:</span>
                    <span class="info-value"><strong>{{ requested_date }}</strong></span>
                </div>
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
                                    Ngày: {{ item.last_delivery.request.completed_date|date:"d/m/Y" }}<br>
                                    SL: {{ item.last_delivery.quantity }}<br>
                                    <span class="history-badge">{{ item.last_delivery.request.request_code }}</span>
                                </small>
                                {% else %}
                                <small class="no-history">Chưa có lịch sử</small>
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
                <a href="{{ approve_url }}" class="button button-approve">PHÊ DUYỆT YÊU CẦU</a>
                <a href="{{ request_url }}" class="button button-view">XEM CHI TIẾT</a>
            </div>
            
            <p style="text-align: center; color: #777; font-size: 13px; margin-top: 18px;">
                Hoặc đăng nhập vào hệ thống và truy cập phần <strong>"Phê duyệt của tôi"</strong> để xử lý yêu cầu này.
            </p>
        </div>
        
        <div class="footer">
            <p><strong>Hệ thống Quản lý Kho</strong></p>
            <p>Email này được gửi tự động, vui lòng không trả lời.</p>
            <p style="color: #999; font-size: 12px;">(c) 2025 OVNC Inventory Management System</p>
        </div>
    </div>
</body>
</html>''',
            'is_html': True,
            'is_active': True
        }
        
        template, created = EmailTemplate.objects.update_or_create(
            code=template_data['code'],
            defaults=template_data
        )
        status = 'Tạo mới' if created else 'Cập nhật'
        self.stdout.write(self.style.SUCCESS(f"{status} mẫu email '{template.name}' với bảng chi tiết sản phẩm"))
        self.stdout.write(self.style.SUCCESS('✓ Đã cập nhật email template pending_approval với tiếng Việt có dấu'))
