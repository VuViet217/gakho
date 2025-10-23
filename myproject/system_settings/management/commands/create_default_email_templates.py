from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Tạo các mẫu email mặc định cho hệ thống'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Đang tạo các mẫu email mặc định...')
        created_count = 0
        updated_count = 0
        
        # Danh sách các mẫu email mặc định
        default_templates = [
            {
                'code': 'request_created',
                'type': 'request_created',
                'name': 'Thông báo yêu cầu mới',
                'subject': 'GA Inventory - Yêu cầu cấp phát mới #{{request_id}}',
                'content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Thông báo yêu cầu cấp phát</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        .header {
                            background-color: #007bff;
                            padding: 10px 20px;
                            color: white;
                            border-radius: 5px 5px 0 0;
                        }
                        .content {
                            padding: 20px;
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                        }
                        .footer {
                            font-size: 12px;
                            text-align: center;
                            padding: 10px;
                            color: #666;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 15px;
                        }
                        table, th, td {
                            border: 1px solid #ddd;
                        }
                        th, td {
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        .button {
                            background-color: #007bff;
                            color: white;
                            padding: 10px 15px;
                            text-decoration: none;
                            border-radius: 4px;
                            display: inline-block;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Thông báo yêu cầu cấp phát mới</h2>
                        </div>
                        <div class="content">
                            <p>Xin chào {{recipient_name}},</p>
                            
                            <p>Hệ thống GA Inventory đã nhận được yêu cầu cấp phát vật tư mới với các thông tin như sau:</p>
                            
                            <table>
                                <tr>
                                    <th>Mã yêu cầu</th>
                                    <td>#{{request_id}}</td>
                                </tr>
                                <tr>
                                    <th>Người yêu cầu</th>
                                    <td>{{requester_name}} ({{requester_email}})</td>
                                </tr>
                                <tr>
                                    <th>Thời gian tạo</th>
                                    <td>{{created_at}}</td>
                                </tr>
                                <tr>
                                    <th>Ngày mong muốn</th>
                                    <td>{{requested_date}}</td>
                                </tr>
                                <tr>
                                    <th>Trạng thái</th>
                                    <td>{{status}}</td>
                                </tr>
                            </table>
                            
                            <p>Vui lòng đăng nhập vào hệ thống để xem chi tiết và xử lý yêu cầu:</p>
                            
                            <p style="text-align: center;">
                                <a href="{{request_url}}" class="button">Xem chi tiết yêu cầu</a>
                            </p>
                            
                            <p>Đây là email tự động, vui lòng không trả lời.</p>
                        </div>
                        <div class="footer">
                            <p>© 2024 GA Inventory System</p>
                        </div>
                    </div>
                </body>
                </html>
                ''',
                'description': 'Mẫu email gửi thông báo khi có yêu cầu cấp phát mới được tạo trong hệ thống.',
                'is_active': True,
                'is_html': True,
            },
            {
                'code': 'pending_approval',
                'type': 'pending_approval',
                'name': 'Thông báo yêu cầu chờ phê duyệt',
                'subject': 'GA Inventory - Yêu cầu cấp phát #{{request_id}} chờ phê duyệt',
                'content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Thông báo yêu cầu chờ phê duyệt</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        .header {
                            background-color: #ff9800;
                            padding: 10px 20px;
                            color: white;
                            border-radius: 5px 5px 0 0;
                        }
                        .content {
                            padding: 20px;
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                        }
                        .footer {
                            font-size: 12px;
                            text-align: center;
                            padding: 10px;
                            color: #666;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 15px;
                        }
                        table, th, td {
                            border: 1px solid #ddd;
                        }
                        th, td {
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        .buttons {
                            text-align: center;
                            margin: 20px 0;
                        }
                        .button {
                            padding: 10px 15px;
                            text-decoration: none;
                            border-radius: 4px;
                            display: inline-block;
                            margin: 0 5px;
                        }
                        .approve {
                            background-color: #4CAF50;
                            color: white;
                        }
                        .reject {
                            background-color: #f44336;
                            color: white;
                        }
                        .view {
                            background-color: #2196F3;
                            color: white;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Thông báo yêu cầu chờ phê duyệt</h2>
                        </div>
                        <div class="content">
                            <p>Xin chào {{approver_name}},</p>
                            
                            <p>Có một yêu cầu cấp phát đang chờ bạn phê duyệt:</p>
                            
                            <table>
                                <tr>
                                    <th>Mã yêu cầu</th>
                                    <td>#{{request_id}}</td>
                                </tr>
                                <tr>
                                    <th>Người yêu cầu</th>
                                    <td>{{requester_name}} ({{requester_email}})</td>
                                </tr>
                                <tr>
                                    <th>Thời gian tạo</th>
                                    <td>{{created_at}}</td>
                                </tr>
                                <tr>
                                    <th>Ngày mong muốn</th>
                                    <td>{{requested_date}}</td>
                                </tr>
                                <tr>
                                    <th>Trạng thái</th>
                                    <td>Chờ phê duyệt</td>
                                </tr>
                            </table>
                            
                            <div class="buttons">
                                <a href="{{approve_url}}" class="button approve">Phê duyệt</a>
                                <a href="{{reject_url}}" class="button reject">Từ chối</a>
                                <a href="{{request_url}}" class="button view">Xem chi tiết</a>
                            </div>
                            
                            <p>Vui lòng đăng nhập vào hệ thống để xem chi tiết và xử lý yêu cầu này.</p>
                            
                            <p>Đây là email tự động, vui lòng không trả lời.</p>
                        </div>
                        <div class="footer">
                            <p>© 2024 GA Inventory System</p>
                        </div>
                    </div>
                </body>
                </html>
                ''',
                'description': 'Mẫu email gửi cho người phê duyệt khi có yêu cầu mới cần xem xét.',
                'is_active': True,
                'is_html': True,
            },
            {
                'code': 'request_approved',
                'type': 'request_approved',
                'name': 'Thông báo yêu cầu được phê duyệt',
                'subject': 'GA Inventory - Yêu cầu cấp phát #{{request_id}} đã được phê duyệt',
                'content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Yêu cầu cấp phát được phê duyệt</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        .header {
                            background-color: #4CAF50;
                            padding: 10px 20px;
                            color: white;
                            border-radius: 5px 5px 0 0;
                        }
                        .content {
                            padding: 20px;
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                        }
                        .footer {
                            font-size: 12px;
                            text-align: center;
                            padding: 10px;
                            color: #666;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 15px;
                        }
                        table, th, td {
                            border: 1px solid #ddd;
                        }
                        th, td {
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        .button {
                            background-color: #2196F3;
                            color: white;
                            padding: 10px 15px;
                            text-decoration: none;
                            border-radius: 4px;
                            display: inline-block;
                        }
                        .success {
                            color: #4CAF50;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Yêu cầu cấp phát đã được phê duyệt</h2>
                        </div>
                        <div class="content">
                            <p>Xin chào {{requester_name}},</p>
                            
                            <p>Chúng tôi vui mừng thông báo rằng yêu cầu cấp phát của bạn đã được <span class="success">phê duyệt</span>.</p>
                            
                            <table>
                                <tr>
                                    <th>Mã yêu cầu</th>
                                    <td>#{{request_id}}</td>
                                </tr>
                                <tr>
                                    <th>Người phê duyệt</th>
                                    <td>{{approver_name}}</td>
                                </tr>
                                <tr>
                                    <th>Thời gian phê duyệt</th>
                                    <td>{{approved_at}}</td>
                                </tr>
                                <tr>
                                    <th>Ngày mong muốn</th>
                                    <td>{{requested_date}}</td>
                                </tr>
                                <tr>
                                    <th>Ghi chú</th>
                                    <td>{{approval_note}}</td>
                                </tr>
                            </table>
                            
                            <p>Yêu cầu của bạn sẽ được chuyển tới bộ phận kho để xử lý. Bạn sẽ nhận được thông báo khi có lịch cấp phát cụ thể.</p>
                            
                            <p style="text-align: center;">
                                <a href="{{request_url}}" class="button">Xem chi tiết yêu cầu</a>
                            </p>
                            
                            <p>Đây là email tự động, vui lòng không trả lời.</p>
                        </div>
                        <div class="footer">
                            <p>© 2024 GA Inventory System</p>
                        </div>
                    </div>
                </body>
                </html>
                ''',
                'description': 'Mẫu email gửi cho người yêu cầu khi yêu cầu đã được phê duyệt.',
                'is_active': True,
                'is_html': True,
            },
            {
                'code': 'request_rejected',
                'type': 'request_rejected',
                'name': 'Thông báo yêu cầu bị từ chối',
                'subject': 'GA Inventory - Yêu cầu cấp phát #{{request_id}} đã bị từ chối',
                'content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Yêu cầu cấp phát bị từ chối</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        .header {
                            background-color: #f44336;
                            padding: 10px 20px;
                            color: white;
                            border-radius: 5px 5px 0 0;
                        }
                        .content {
                            padding: 20px;
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                        }
                        .footer {
                            font-size: 12px;
                            text-align: center;
                            padding: 10px;
                            color: #666;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 15px;
                        }
                        table, th, td {
                            border: 1px solid #ddd;
                        }
                        th, td {
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        .button {
                            background-color: #2196F3;
                            color: white;
                            padding: 10px 15px;
                            text-decoration: none;
                            border-radius: 4px;
                            display: inline-block;
                        }
                        .rejected {
                            color: #f44336;
                            font-weight: bold;
                        }
                        .reason {
                            background-color: #fff3f3;
                            border-left: 4px solid #f44336;
                            padding: 10px;
                            margin-bottom: 15px;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Yêu cầu cấp phát đã bị từ chối</h2>
                        </div>
                        <div class="content">
                            <p>Xin chào {{requester_name}},</p>
                            
                            <p>Chúng tôi rất tiếc phải thông báo rằng yêu cầu cấp phát của bạn đã bị <span class="rejected">từ chối</span>.</p>
                            
                            <table>
                                <tr>
                                    <th>Mã yêu cầu</th>
                                    <td>#{{request_id}}</td>
                                </tr>
                                <tr>
                                    <th>Người từ chối</th>
                                    <td>{{approver_name}}</td>
                                </tr>
                                <tr>
                                    <th>Thời gian từ chối</th>
                                    <td>{{rejected_at}}</td>
                                </tr>
                            </table>
                            
                            <p><strong>Lý do từ chối:</strong></p>
                            <div class="reason">
                                {{rejection_reason}}
                            </div>
                            
                            <p>Nếu bạn có thắc mắc hoặc cần giải thích thêm, vui lòng liên hệ trực tiếp với người quản lý của bạn hoặc phòng quản lý thiết bị.</p>
                            
                            <p>Bạn có thể tạo yêu cầu mới với những điều chỉnh phù hợp.</p>
                            
                            <p style="text-align: center;">
                                <a href="{{request_url}}" class="button">Xem chi tiết yêu cầu</a>
                            </p>
                            
                            <p>Đây là email tự động, vui lòng không trả lời.</p>
                        </div>
                        <div class="footer">
                            <p>© 2024 GA Inventory System</p>
                        </div>
                    </div>
                </body>
                </html>
                ''',
                'description': 'Mẫu email gửi cho người yêu cầu khi yêu cầu bị từ chối.',
                'is_active': True,
                'is_html': True,
            },
            {
                'code': 'warehouse_scheduled',
                'type': 'warehouse_scheduled',
                'name': 'Thông báo kho đã lên lịch cấp phát',
                'subject': 'GA Inventory - Lịch cấp phát cho yêu cầu #{{request_id}} đã được xác nhận',
                'content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Lịch cấp phát đã được xác nhận</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        .header {
                            background-color: #9C27B0;
                            padding: 10px 20px;
                            color: white;
                            border-radius: 5px 5px 0 0;
                        }
                        .content {
                            padding: 20px;
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                        }
                        .footer {
                            font-size: 12px;
                            text-align: center;
                            padding: 10px;
                            color: #666;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 15px;
                        }
                        table, th, td {
                            border: 1px solid #ddd;
                        }
                        th, td {
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        .button {
                            background-color: #2196F3;
                            color: white;
                            padding: 10px 15px;
                            text-decoration: none;
                            border-radius: 4px;
                            display: inline-block;
                        }
                        .schedule {
                            background-color: #e8f5e9;
                            border-left: 4px solid #4CAF50;
                            padding: 15px;
                            margin-bottom: 15px;
                            font-size: 16px;
                        }
                        .highlight {
                            color: #9C27B0;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Lịch cấp phát đã được xác nhận</h2>
                        </div>
                        <div class="content">
                            <p>Xin chào {{requester_name}},</p>
                            
                            <p>Chúng tôi vui mừng thông báo rằng yêu cầu cấp phát của bạn đã được lên lịch cụ thể.</p>
                            
                            <div class="schedule">
                                <p><strong>Ngày cấp phát:</strong> <span class="highlight">{{distribution_date}}</span></p>
                                <p><strong>Giờ cấp phát:</strong> <span class="highlight">{{distribution_time}}</span></p>
                                <p><strong>Địa điểm:</strong> <span class="highlight">{{distribution_location}}</span></p>
                            </div>
                            
                            <table>
                                <tr>
                                    <th>Mã yêu cầu</th>
                                    <td>#{{request_id}}</td>
                                </tr>
                                <tr>
                                    <th>Người phụ trách kho</th>
                                    <td>{{warehouse_manager}}</td>
                                </tr>
                                <tr>
                                    <th>Liên hệ</th>
                                    <td>{{warehouse_contact}}</td>
                                </tr>
                                <tr>
                                    <th>Ghi chú</th>
                                    <td>{{warehouse_note}}</td>
                                </tr>
                            </table>
                            
                            <p>Vui lòng đến đúng giờ và mang theo thẻ nhân viên để nhận vật tư. Nếu bạn không thể đến vào thời gian đã định, vui lòng liên hệ với người phụ trách kho càng sớm càng tốt.</p>
                            
                            <p style="text-align: center;">
                                <a href="{{request_url}}" class="button">Xem chi tiết yêu cầu</a>
                            </p>
                            
                            <p>Đây là email tự động, vui lòng không trả lời.</p>
                        </div>
                        <div class="footer">
                            <p>© 2024 GA Inventory System</p>
                        </div>
                    </div>
                </body>
                </html>
                ''',
                'description': 'Mẫu email gửi cho người yêu cầu khi kho đã lên lịch cấp phát.',
                'is_active': True,
                'is_html': True,
            },
            {
                'code': 'request_completed',
                'type': 'request_completed',
                'name': 'Thông báo yêu cầu đã hoàn thành',
                'subject': 'GA Inventory - Yêu cầu cấp phát #{{request_id}} đã hoàn thành',
                'content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Yêu cầu cấp phát đã hoàn thành</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        .header {
                            background-color: #009688;
                            padding: 10px 20px;
                            color: white;
                            border-radius: 5px 5px 0 0;
                        }
                        .content {
                            padding: 20px;
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                        }
                        .footer {
                            font-size: 12px;
                            text-align: center;
                            padding: 10px;
                            color: #666;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 15px;
                        }
                        table, th, td {
                            border: 1px solid #ddd;
                        }
                        th, td {
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                        .button {
                            background-color: #2196F3;
                            color: white;
                            padding: 10px 15px;
                            text-decoration: none;
                            border-radius: 4px;
                            display: inline-block;
                        }
                        .complete {
                            color: #009688;
                            font-weight: bold;
                        }
                        .items {
                            margin-top: 20px;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Yêu cầu cấp phát đã hoàn thành</h2>
                        </div>
                        <div class="content">
                            <p>Xin chào {{requester_name}},</p>
                            
                            <p>Chúng tôi vui mừng thông báo rằng yêu cầu cấp phát của bạn đã được <span class="complete">hoàn thành</span>.</p>
                            
                            <table>
                                <tr>
                                    <th>Mã yêu cầu</th>
                                    <td>#{{request_id}}</td>
                                </tr>
                                <tr>
                                    <th>Ngày hoàn thành</th>
                                    <td>{{completed_at}}</td>
                                </tr>
                                <tr>
                                    <th>Người thực hiện</th>
                                    <td>{{fulfilled_by}}</td>
                                </tr>
                            </table>
                            
                            <div class="items">
                                <p><strong>Danh sách vật tư đã được cấp phát:</strong></p>
                                <table>
                                    <tr>
                                        <th>Tên vật tư</th>
                                        <th>Số lượng</th>
                                        <th>Đơn vị</th>
                                        <th>Ghi chú</th>
                                    </tr>
                                    {{items_list}}
                                </table>
                            </div>
                            
                            <p>Cảm ơn bạn đã sử dụng hệ thống GA Inventory. Nếu bạn có bất kỳ thắc mắc nào về vật tư đã nhận, vui lòng liên hệ với phòng quản lý thiết bị.</p>
                            
                            <p style="text-align: center;">
                                <a href="{{request_url}}" class="button">Xem chi tiết yêu cầu</a>
                            </p>
                            
                            <p>Đây là email tự động, vui lòng không trả lời.</p>
                        </div>
                        <div class="footer">
                            <p>© 2024 GA Inventory System</p>
                        </div>
                    </div>
                </body>
                </html>
                ''',
                'description': 'Mẫu email gửi cho người yêu cầu khi yêu cầu đã hoàn thành.',
                'is_active': True,
                'is_html': True,
            },
        ]
        
        # Tạo hoặc cập nhật các mẫu email
        for template_data in default_templates:
            # Trích xuất biến từ nội dung
            from system_settings.utils.email_template_utils import extract_variables_from_template
            variables = extract_variables_from_template(template_data['content'])
            variable_dict = {var: '' for var in variables}
            template_data['variables'] = variable_dict
            
            # Kiểm tra xem mẫu đã tồn tại chưa
            try:
                template = EmailTemplate.objects.get(code=template_data['code'])
                # Cập nhật mẫu nếu đã tồn tại
                for key, value in template_data.items():
                    setattr(template, key, value)
                template.save()
                updated_count += 1
                self.stdout.write(f'Đã cập nhật mẫu: {template.name}')
            except EmailTemplate.DoesNotExist:
                # Tạo mẫu mới nếu chưa tồn tại
                EmailTemplate.objects.create(**template_data)
                created_count += 1
                self.stdout.write(f'Đã tạo mẫu mới: {template_data["name"]}')
        
        self.stdout.write(self.style.SUCCESS(f'Hoàn thành! Đã tạo {created_count} mẫu mới và cập nhật {updated_count} mẫu.'))