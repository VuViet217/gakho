from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Tạo template email thông báo yêu cầu đã được phê duyệt cần xử lý xuất kho cho quản lý kho'

    def handle(self, *args, **options):
        # Template: Thông báo cho quản lý kho cần xử lý xuất kho
        warehouse_approval_template = {
            'code': 'warehouse_approval_required',
            'name': 'Yêu cầu cần xử lý xuất kho',
            'subject': '[Quản lý kho] Yêu cầu #{request.request_code} cần xử lý xuất kho',
            'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .info-box { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #667eea; }
        .info-row { margin: 10px 0; }
        .label { font-weight: bold; color: #667eea; display: inline-block; min-width: 150px; }
        .value { color: #333; }
        .status-badge { display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .status-approved { background: #d4edda; color: #155724; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; background: white; }
        th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px; text-align: left; font-weight: bold; }
        td { padding: 12px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f5f5f5; }
        .product-code { font-family: monospace; background: #e9ecef; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
        .button { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .button:hover { background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); }
        .footer { text-align: center; color: #888; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }
        .urgent { background: #fff3cd; border-left-color: #ffc107; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Yêu cầu cần xử lý xuất kho</h1>
            <p>Một yêu cầu cấp phát đã được phê duyệt và cần xử lý</p>
        </div>
        
        <div class="content">
            <div class="info-box urgent">
                <h2>Thông tin yêu cầu</h2>
                <div class="info-row">
                    <span class="label">Mã yêu cầu:</span>
                    <span class="value"><strong>#{request.request_code}</strong></span>
                </div>
                <div class="info-row">
                    <span class="label">Người yêu cầu:</span>
                    <span class="value">{request.requester.get_full_name} ({request.requester.email})</span>
                </div>
                <div class="info-row">
                    <span class="label">Người phê duyệt:</span>
                    <span class="value">{approver.get_full_name}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày tạo:</span>
                    <span class="value">{request.created_at|date:"d/m/Y H:i"}</span>
                </div>
                <div class="info-row">
                    <span class="label">Ngày phê duyệt:</span>
                    <span class="value">{request.approved_date|date:"d/m/Y H:i"}</span>
                </div>
                <div class="info-row">
                    <span class="label">Trạng thái:</span>
                    <span class="status-badge status-approved">Đã phê duyệt</span>
                </div>
            </div>

            <div class="info-box">
                <h3>Danh sách nhân viên và sản phẩm cần xuất kho</h3>
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
                                <strong>{employee_product.employee.full_name}</strong><br>
                                <small>{employee_product.employee.department.name if employee_product.employee.department else 'N/A'}</small>
                            </td>
                            <td>
                                <span class="product-code">{employee_product.product.product_code}</span><br>
                                {employee_product.product.name}
                            </td>
                            <td><strong>{employee_product.quantity}</strong></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            {% if request.note %}
            <div class="info-box">
                <h3>Ghi chú</h3>
                <p>{request.note}</p>
            </div>
            {% endif %}

            <div style="text-align: center;">
                <a href="{request.get_absolute_url}" class="button">Xem chi tiết và xử lý xuất kho</a>
            </div>
        </div>
        
        <div class="footer">
            <p>Email này được gửi tự động từ hệ thống OVNC Inventory Management</p>
            <p>Vui lòng xử lý yêu cầu xuất kho sớm nhất có thể</p>
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
