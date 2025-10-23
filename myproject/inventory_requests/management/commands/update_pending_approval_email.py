from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Cập nhật template email pending_approval với bảng chi tiết sản phẩm (không emoji, phù hợp Outlook)'

    def handle(self, *args, **options):
        template_code = 'pending_approval'
        
        # Nội dung template mới - đơn giản, không chữ trắng, phù hợp Outlook
        new_content = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yêu cầu chờ phê duyệt</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border: 1px solid #dddddd; border-radius: 8px;">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #ff9800; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #333333; font-size: 22px; font-weight: bold;">
                                YÊU CẦU CHỜ PHÊ DUYỆT
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 30px;">
                            <p style="margin: 0 0 20px 0; font-size: 15px; color: #333333;">
                                Xin chào <strong>{{ approver_name }}</strong>,
                            </p>
                            
                            <p style="margin: 0 0 20px 0; font-size: 15px; color: #333333;">
                                Có một yêu cầu cấp phát đang chờ bạn phê duyệt. Vui lòng xem xét và xử lý yêu cầu này.
                            </p>
                            
                            <!-- Request Info Box -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f9f9f9; border: 1px solid #e0e0e0; border-radius: 5px; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h3 style="margin: 0 0 15px 0; color: #ff9800; font-size: 16px; font-weight: bold;">
                                            THÔNG TIN YÊU CẦU
                                        </h3>
                                        
                                        <table width="100%" cellpadding="8" cellspacing="0" border="0">
                                            <tr>
                                                <td width="150" style="font-weight: bold; color: #555555; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    Mã yêu cầu:
                                                </td>
                                                <td style="color: #333333; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    <strong>#{{ request_id }}</strong>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="150" style="font-weight: bold; color: #555555; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    Người yêu cầu:
                                                </td>
                                                <td style="color: #333333; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    {{ requester_name }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="150" style="font-weight: bold; color: #555555; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    Email:
                                                </td>
                                                <td style="color: #333333; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    {{ requester_email }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="150" style="font-weight: bold; color: #555555; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    Thời gian tạo:
                                                </td>
                                                <td style="color: #333333; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    {{ created_at }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="150" style="font-weight: bold; color: #555555; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    Ngày mong muốn:
                                                </td>
                                                <td style="color: #333333; font-size: 14px; border-bottom: 1px solid #e0e0e0;">
                                                    {{ requested_date }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="150" style="font-weight: bold; color: #555555; font-size: 14px;">
                                                    Trạng thái:
                                                </td>
                                                <td style="color: #ff9800; font-size: 14px; font-weight: bold;">
                                                    Chờ phê duyệt
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Action Buttons -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center" style="padding: 10px 0;">
                                        <table cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{ approve_url }}" style="display: inline-block; padding: 12px 25px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">
                                                        PHÊ DUYỆT YÊU CẦU
                                                    </a>
                                                </td>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{ reject_url }}" style="display: inline-block; padding: 12px 25px; background-color: #f44336; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">
                                                        TỪ CHỐI
                                                    </a>
                                                </td>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{ request_url }}" style="display: inline-block; padding: 12px 25px; background-color: #2196F3; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">
                                                        XEM CHI TIẾT
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Alternative Links -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f0f8ff; border: 1px solid #b3d9ff; border-radius: 5px; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 15px;">
                                        <p style="margin: 0 0 10px 0; font-size: 13px; color: #333333; font-weight: bold;">
                                            Nếu nút bấm không hoạt động, vui lòng copy link bên dưới:
                                        </p>
                                        <p style="margin: 5px 0; font-size: 12px; color: #555555;">
                                            <strong>Phê duyệt:</strong><br>
                                            <a href="{{ approve_url }}" style="color: #2196F3; word-break: break-all;">{{ approve_url }}</a>
                                        </p>
                                        <p style="margin: 5px 0; font-size: 12px; color: #555555;">
                                            <strong>Từ chối:</strong><br>
                                            <a href="{{ reject_url }}" style="color: #2196F3; word-break: break-all;">{{ reject_url }}</a>
                                        </p>
                                        <p style="margin: 5px 0; font-size: 12px; color: #555555;">
                                            <strong>Xem chi tiết:</strong><br>
                                            <a href="{{ request_url }}" style="color: #2196F3; word-break: break-all;">{{ request_url }}</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 20px 0 10px 0; font-size: 14px; color: #666666; font-style: italic;">
                                Vui lòng đăng nhập vào hệ thống để xem chi tiết và xử lý yêu cầu này.
                            </p>
                            
                            <p style="margin: 10px 0 0 0; font-size: 13px; color: #999999;">
                                Đây là email tự động, vui lòng không trả lời email này.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f5f5f5; padding: 20px; text-align: center; border-top: 1px solid #dddddd; border-radius: 0 0 8px 8px;">
                            <p style="margin: 0; font-size: 12px; color: #666666;">
                                <strong>Hệ thống Quản lý Kho</strong><br>
                                Email này được gửi từ động, vui lòng không trả lời.
                            </p>
                            <p style="margin: 10px 0 0 0; font-size: 11px; color: #999999;">
                                © 2025 GA Inventory Management System
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''

        new_subject = '[Cần phê duyệt] Yêu cầu cấp phát #{{ request_id }}'
        
        try:
            template = EmailTemplate.objects.get(code=template_code)
            template.subject = new_subject
            template.content = new_content
            template.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Đã cập nhật template "{template_code}" thành công!'
                )
            )
            self.stdout.write(f'   - Subject: {new_subject}')
            self.stdout.write(f'   - Giao diện: Đơn giản, phù hợp Outlook')
            self.stdout.write(f'   - Màu chữ: Đen (#333333)')
            self.stdout.write(f'   - Link: Có cả nút bấm và link text')
            
        except EmailTemplate.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Không tìm thấy template với mã "{template_code}"'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Lỗi khi cập nhật template: {str(e)}'
                )
            )
