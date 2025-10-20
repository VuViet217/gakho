from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate


class Command(BaseCommand):
    help = 'Tạo email template cho thông báo hoàn thành cấp phát'

    def handle(self, *args, **options):
        template_code = 'request_completed'
        template_name = 'Yêu cầu đã hoàn thành'
        template_type = 'request_completed'
        subject = 'Yêu cầu cấp phát #{{ request_code }} đã hoàn thành'
        
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yêu cầu cấp phát đã hoàn thành</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #28a745; padding: 30px 40px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: bold;">
                                ✓ Yêu cầu cấp phát đã hoàn thành
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 20px 0; font-size: 16px; color: #333333; line-height: 1.6;">
                                Kính gửi <strong>{{ requester_name }}</strong>,
                            </p>
                            
                            <p style="margin: 0 0 25px 0; font-size: 14px; color: #555555; line-height: 1.6;">
                                Yêu cầu cấp phát của bạn đã được hoàn thành và sẵn sàng để nhận.
                            </p>
                            
                            <!-- Info Box -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa; border-left: 4px solid #28a745; margin: 25px 0;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="padding: 8px 0; font-size: 14px; color: #666666; width: 40%;">
                                                    <strong>Mã yêu cầu:</strong>
                                                </td>
                                                <td style="padding: 8px 0; font-size: 14px; color: #333333;">
                                                    <strong style="color: #28a745;">{{ request_code }}</strong>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0; font-size: 14px; color: #666666;">
                                                    <strong>Tiêu đề:</strong>
                                                </td>
                                                <td style="padding: 8px 0; font-size: 14px; color: #333333;">
                                                    {{ title }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0; font-size: 14px; color: #666666;">
                                                    <strong>Ngày hoàn thành:</strong>
                                                </td>
                                                <td style="padding: 8px 0; font-size: 14px; color: #333333;">
                                                    {{ completed_date }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0; font-size: 14px; color: #666666;">
                                                    <strong>Người xử lý:</strong>
                                                </td>
                                                <td style="padding: 8px 0; font-size: 14px; color: #333333;">
                                                    {{ warehouse_manager }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0; font-size: 14px; color: #666666; vertical-align: top;">
                                                    <strong>Ghi chú:</strong>
                                                </td>
                                                <td style="padding: 8px 0; font-size: 14px; color: #333333;">
                                                    {{ note }}
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 25px 0 20px 0; font-size: 14px; color: #555555; line-height: 1.6;">
                                Vui lòng liên hệ với bộ phận kho để nhận hàng theo lịch đã được sắp xếp.
                            </p>
                            
                            <!-- Button -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{{ detail_url }}" style="display: inline-block; padding: 14px 40px; background-color: #28a745; color: #ffffff; text-decoration: none; border-radius: 5px; font-size: 14px; font-weight: bold; border: 2px solid #28a745;">
                                            Xem chi tiết yêu cầu
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 25px 0 0 0; font-size: 13px; color: #888888; line-height: 1.6;">
                                Cảm ơn bạn đã sử dụng hệ thống quản lý kho.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 20px 40px; border-top: 1px solid #e9ecef;">
                            <p style="margin: 0; font-size: 12px; color: #666666; text-align: center; line-height: 1.5;">
                                Email này được gửi tự động từ Hệ thống quản lý kho.<br>
                                Vui lòng không trả lời email này.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''

        # Tạo hoặc cập nhật template
        template, created = EmailTemplate.objects.update_or_create(
            code=template_code,
            defaults={
                'type': template_type,
                'name': template_name,
                'subject': subject,
                'content': html_content,
                'is_html': True,
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Email template "{template_code}" đã được tạo thành công!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Email template "{template_code}" đã được cập nhật!'))
