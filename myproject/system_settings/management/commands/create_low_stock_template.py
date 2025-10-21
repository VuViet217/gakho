from django.core.management.base import BaseCommand
from django.utils import timezone
from system_settings.models import EmailTemplate


DEFAULT_HTML = '''
<!-- Outlook-friendly HTML email -->
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; margin:0; padding:0;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; margin:20px 0; border-radius:4px; overflow:hidden;">
            <tr style="background:#0d6efd; color:#ffffff;">
              <td style="padding:20px; text-align:left;">
                <h1 style="margin:0; font-size:20px;">Cảnh báo tồn kho thấp</h1>
              </td>
            </tr>
            <tr>
              <td style="padding:20px; color:#333333;">
                <p>Xin chào,</p>
                <p>Dưới đây là danh sách các sản phẩm đang có mức tồn kho bằng hoặc dưới ngưỡng tối thiểu:</p>
                <table width="100%" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">
                  <thead>
                    <tr style="background:#f1f1f1;">
                      <th align="left">Mã</th>
                      <th align="left">Tên</th>
                      <th align="right">Tồn</th>
                      <th align="right">Tối thiểu</th>
                    </tr>
                  </thead>
                  <tbody>
                    {% for p in products %}
                    <tr>
                      <td>{{ p.product_code }}</td>
                      <td>{{ p.name }}</td>
                      <td align="right">{{ p.current_quantity }} {{ p.unit }}</td>
                      <td align="right">{{ p.minimum_quantity }} {{ p.unit }}</td>
                    </tr>
                    {% endfor %}
                  </tbody>
                </table>
                <p>Vui lòng kiểm tra và lên kế hoạch nhập hàng kịp thời.</p>
                <p>Trân trọng,<br/>Hệ thống quản lý kho OVNC</p>
              </td>
            </tr>
            <tr style="background:#f9f9f9;">
              <td style="padding:12px; font-size:12px; color:#666; text-align:center;">Generated at {{ date }}</td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
'''


class Command(BaseCommand):
    help = 'Tạo mẫu email low_stock_alert nếu chưa tồn tại'

    def handle(self, *args, **options):
        template_code = 'low_stock_alert'
        template, created = EmailTemplate.objects.update_or_create(
            code=template_code,
            defaults={
                'type': 'other',
                'name': 'Low Stock Alert',
                'subject': '[OVNC] Cảnh báo tồn kho thấp - {{ count }} sản phẩm',
                'content': DEFAULT_HTML,
                'is_html': True,
                'is_active': True,
                'variables': {'products': '', 'date': ''}
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Tạo mẫu low_stock_alert thành công.'))
        else:
            self.stdout.write(self.style.SUCCESS('Mẫu low_stock_alert đã được cập nhật.'))
