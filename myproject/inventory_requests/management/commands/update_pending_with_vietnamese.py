# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Cập nhật template email pending_approval với tiếng Việt có dấu và bảng sản phẩm'

    def handle(self, *args, **options):
        try:
            template = EmailTemplate.objects.get(code='pending_approval')
            
            template.subject = 'GA Inventory - Yêu cầu cấp phát #{{request.id}} chờ phê duyệt'
            
            template.content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thông báo yêu cầu chờ phê duyệt</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 20px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">YÊU CẦU CHỜ PHÊ DUYỆT</h1>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding: 30px 20px;">
                            <div style="background-color: #fff9e6; border-left: 4px solid #ffc107; padding: 15px; margin-bottom: 20px;">
                                <p style="margin: 0; color: #856404; font-weight: bold;">Bạn có một yêu cầu cấp phát mới cần phê duyệt!</p>
                                <p style="margin: 5px 0 0 0; color: #856404;">Yêu cầu từ <strong>{{requester_name}}</strong> ({{requester_email}}) đang chờ bạn xem xét và phê duyệt.</p>
                            </div>
                            
                            <h2 style="color: #667eea; font-size: 18px; margin-top: 20px; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Thông tin yêu cầu</h2>
                            
                            <table width="100%" cellpadding="8" cellspacing="0" style="border-collapse: collapse; margin-bottom: 20px;">
                                <tr style="background-color: #f8f9fa;">
                                    <td style="border: 1px solid #dee2e6; padding: 10px; font-weight: bold; width: 40%;">Mã yêu cầu:</td>
                                    <td style="border: 1px solid #dee2e6; padding: 10px;">#{{request.id}}</td>
                                </tr>
                                <tr>
                                    <td style="border: 1px solid #dee2e6; padding: 10px; font-weight: bold;">Người yêu cầu:</td>
                                    <td style="border: 1px solid #dee2e6; padding: 10px;">{{requester_name}} ({{requester_email}})</td>
                                </tr>
                                <tr style="background-color: #f8f9fa;">
                                    <td style="border: 1px solid #dee2e6; padding: 10px; font-weight: bold;">Thời gian tạo:</td>
                                    <td style="border: 1px solid #dee2e6; padding: 10px;">{{created_at}}</td>
                                </tr>
                                <tr>
                                    <td style="border: 1px solid #dee2e6; padding: 10px; font-weight: bold;">Ngày mong muốn:</td>
                                    <td style="border: 1px solid #dee2e6; padding: 10px;">{{requested_date}}</td>
                                </tr>
                                <tr style="background-color: #f8f9fa;">
                                    <td style="border: 1px solid #dee2e6; padding: 10px; font-weight: bold;">Trạng thái:</td>
                                    <td style="border: 1px solid #dee2e6; padding: 10px;"><span style="background-color: #ffc107; color: #000; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold;">CHỜ PHÊ DUYỆT</span></td>
                                </tr>
                            </table>
                            
                            {% if employee_products_with_history %}
                            <h2 style="color: #667eea; font-size: 18px; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Chi tiết phân bổ sản phẩm cho nhân viên</h2>
                            
                            <table width="100%" cellpadding="8" cellspacing="0" style="border-collapse: collapse; margin-bottom: 20px; font-size: 13px;">
                                <thead>
                                    <tr style="background-color: #667eea; color: #ffffff;">
                                        <th style="border: 1px solid #5568d3; padding: 10px; text-align: center;">#</th>
                                        <th style="border: 1px solid #5568d3; padding: 10px; text-align: left;">Nhân viên</th>
                                        <th style="border: 1px solid #5568d3; padding: 10px; text-align: left;">Sản phẩm</th>
                                        <th style="border: 1px solid #5568d3; padding: 10px; text-align: center;">SL</th>
                                        <th style="border: 1px solid #5568d3; padding: 10px; text-align: center;">Lần lấy gần nhất</th>
                                        <th style="border: 1px solid #5568d3; padding: 10px; text-align: left;">Ghi chú</th>
                                    </tr>
                                </thead>
                                <tbody>
                                {% for item in employee_products_with_history %}
                                    <tr style="{% if forloop.counter|divisibleby:2 %}background-color: #f8f9fa;{% endif %}">
                                        <td style="border: 1px solid #dee2e6; padding: 8px; text-align: center;">{{forloop.counter}}</td>
                                        <td style="border: 1px solid #dee2e6; padding: 8px;">
                                            <strong>{{item.employee_name}}</strong><br>
                                            <span style="color: #6c757d; font-size: 11px;">{{item.employee_code}}</span>
                                        </td>
                                        <td style="border: 1px solid #dee2e6; padding: 8px;">
                                            {{item.product_name}}<br>
                                            <span style="color: #6c757d; font-size: 11px;">Mã: {{item.product_code}}</span>
                                        </td>
                                        <td style="border: 1px solid #dee2e6; padding: 8px; text-align: center;">
                                            <strong style="color: #667eea;">{{item.quantity}}</strong>
                                        </td>
                                        <td style="border: 1px solid #dee2e6; padding: 8px; text-align: center; font-size: 11px;">
                                            {% if item.last_received_date %}
                                                {{item.last_received_date}}<br>
                                                <span style="color: #28a745; font-weight: bold;">SL: {{item.last_received_quantity}}</span><br>
                                                <span style="color: #6c757d;">{{item.last_request_code}}</span>
                                            {% else %}
                                                <span style="color: #dc3545; font-style: italic;">Chưa có lịch sử</span>
                                            {% endif %}
                                        </td>
                                        <td style="border: 1px solid #dee2e6; padding: 8px; font-size: 11px; color: #6c757d;">
                                            {{item.note|default:"&mdash;"}}
                                        </td>
                                    </tr>
                                {% endfor %}
                                </tbody>
                            </table>
                            {% endif %}
                            
                            <!-- Action Buttons -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 30px;">
                                <tr>
                                    <td align="center">
                                        <table cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{approve_url}}" style="display: inline-block; background-color: #28a745; color: #ffffff; text-decoration: none; padding: 12px 30px; border-radius: 5px; font-weight: bold; font-size: 14px;">PHÊ DUYỆT YÊU CẦU</a>
                                                </td>
                                                <td style="padding: 0 5px;">
                                                    <a href="{{request_url}}" style="display: inline-block; background-color: #007bff; color: #ffffff; text-decoration: none; padding: 12px 30px; border-radius: 5px; font-weight: bold; font-size: 14px;">XEM CHI TIẾT</a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin-top: 25px; padding: 15px; background-color: #e9ecef; border-radius: 5px; font-size: 13px; color: #495057;">
                                <strong>Lưu ý:</strong> Hoặc đăng nhập vào hệ thống và truy cập phần "Phê duyệt của tôi" để xử lý yêu cầu này.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 20px; text-align: center; border-top: 3px solid #667eea;">
                            <p style="margin: 0; font-size: 12px; color: #6c757d;">Hệ thống Quản lý Kho</p>
                            <p style="margin: 5px 0 0 0; font-size: 11px; color: #adb5bd;">Email này được gửi tự động, vui lòng không trả lời.</p>
                            <p style="margin: 10px 0 0 0; font-size: 11px; color: #adb5bd;">&copy; 2025 GA Inventory Management System</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''
            
            template.save()
            
            self.stdout.write(
                self.style.SUCCESS('✓ Đã cập nhật template email "pending_approval" với tiếng Việt có dấu và bảng sản phẩm!')
            )
            
        except EmailTemplate.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('✗ Không tìm thấy template "pending_approval"')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Lỗi: {str(e)}')
            )
