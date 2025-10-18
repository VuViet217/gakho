from django.core.management.base import BaseCommand
from system_settings.models import EmailTemplate

class Command(BaseCommand):
    help = 'Tạo các mẫu email mặc định cho chức năng yêu cầu cấp phát'

    def handle(self, *args, **kwargs):
        templates = [
            # Mẫu thông báo tạo yêu cầu mới
            {
                'code': 'request_created',
                'type': 'notification',
                'name': 'Thông báo tạo yêu cầu mới',
                'subject': 'Yêu cầu cấp phát mới #{{ request.request_code }} đã được tạo',
                'content': '''<p>Kính gửi {{ user.get_full_name }},</p>
<p>Yêu cầu cấp phát của bạn đã được tạo thành công và đã được gửi đến người phê duyệt.</p>
<p><strong>Thông tin yêu cầu:</strong></p>
<ul>
    <li>Mã yêu cầu: {{ request.request_code }}</li>
    <li>Tiêu đề: {{ request.title }}</li>
    <li>Trạng thái: Chờ phê duyệt</li>
    <li>Ngày mong muốn nhận: {{ request.expected_date|date:"d/m/Y" }}</li>
</ul>
<p>Bạn có thể theo dõi trạng thái yêu cầu trong phần "Yêu cầu của tôi".</p>
<p>Trân trọng,<br>Hệ thống Quản lý Kho</p>''',
                'is_active': True
            },
            
            # Mẫu thông báo chờ phê duyệt gửi đến quản lý
            {
                'code': 'pending_approval',
                'type': 'notification',
                'name': 'Thông báo yêu cầu chờ phê duyệt',
                'subject': 'Yêu cầu cấp phát #{{ request.request_code }} cần bạn phê duyệt',
                'content': '''<p>Kính gửi {{ manager.get_full_name }},</p>
<p>Có một yêu cầu cấp phát mới từ {{ user.get_full_name }} đang chờ bạn phê duyệt.</p>
<p><strong>Thông tin yêu cầu:</strong></p>
<ul>
    <li>Mã yêu cầu: {{ request.request_code }}</li>
    <li>Tiêu đề: {{ request.title }}</li>
    <li>Người tạo: {{ user.get_full_name }}</li>
    <li>Ngày tạo: {{ request.created_at|date:"d/m/Y H:i" }}</li>
    <li>Ngày mong muốn nhận: {{ request.expected_date|date:"d/m/Y" }}</li>
</ul>
<p>Vui lòng đăng nhập vào hệ thống và truy cập phần "Phê duyệt của tôi" để xem chi tiết và phê duyệt yêu cầu này.</p>
<p>Trân trọng,<br>Hệ thống Quản lý Kho</p>''',
                'is_active': True
            },
            
            # Mẫu thông báo yêu cầu được phê duyệt
            {
                'code': 'request_approved',
                'type': 'notification',
                'name': 'Thông báo yêu cầu được phê duyệt',
                'subject': 'Yêu cầu cấp phát #{{ request.request_code }} đã được phê duyệt',
                'content': '''<p>Kính gửi {{ user.get_full_name }},</p>
<p>Yêu cầu cấp phát của bạn đã được phê duyệt bởi {{ approver.get_full_name }}.</p>
<p><strong>Thông tin yêu cầu:</strong></p>
<ul>
    <li>Mã yêu cầu: {{ request.request_code }}</li>
    <li>Tiêu đề: {{ request.title }}</li>
    <li>Trạng thái: Đã phê duyệt</li>
    <li>Người phê duyệt: {{ approver.get_full_name }}</li>
    <li>Ngày phê duyệt: {{ request.approval_date|date:"d/m/Y H:i" }}</li>
</ul>
<p>Yêu cầu của bạn đã được chuyển đến bộ phận kho để lên lịch cấp phát. Bạn sẽ nhận được thông báo khi có lịch cấp phát.</p>
<p>Trân trọng,<br>Hệ thống Quản lý Kho</p>''',
                'is_active': True
            },
            
            # Mẫu thông báo yêu cầu bị từ chối
            {
                'code': 'request_rejected',
                'type': 'notification',
                'name': 'Thông báo yêu cầu bị từ chối',
                'subject': 'Yêu cầu cấp phát #{{ request.request_code }} đã bị từ chối',
                'content': '''<p>Kính gửi {{ user.get_full_name }},</p>
<p>Rất tiếc, yêu cầu cấp phát của bạn đã bị từ chối bởi {{ approver.get_full_name }}.</p>
<p><strong>Thông tin yêu cầu:</strong></p>
<ul>
    <li>Mã yêu cầu: {{ request.request_code }}</li>
    <li>Tiêu đề: {{ request.title }}</li>
    <li>Trạng thái: Bị từ chối</li>
    <li>Người từ chối: {{ approver.get_full_name }}</li>
    <li>Ngày từ chối: {{ request.approval_date|date:"d/m/Y H:i" }}</li>
    <li>Lý do từ chối: {{ rejection_reason }}</li>
</ul>
<p>Nếu bạn có thắc mắc, vui lòng liên hệ trực tiếp với người quản lý của bạn.</p>
<p>Trân trọng,<br>Hệ thống Quản lý Kho</p>''',
                'is_active': True
            },
            
            # Mẫu thông báo yêu cầu đã được lên lịch
            {
                'code': 'warehouse_scheduled',
                'type': 'notification',
                'name': 'Thông báo yêu cầu đã được lên lịch cấp phát',
                'subject': 'Yêu cầu cấp phát #{{ request.request_code }} đã được lên lịch',
                'content': '''<p>Kính gửi {{ user.get_full_name }},</p>
<p>Yêu cầu cấp phát của bạn đã được lên lịch cấp phát.</p>
<p><strong>Thông tin yêu cầu:</strong></p>
<ul>
    <li>Mã yêu cầu: {{ request.request_code }}</li>
    <li>Tiêu đề: {{ request.title }}</li>
    <li>Trạng thái: Đã lên lịch</li>
    <li>Ngày dự kiến cấp phát: {{ scheduled_date|date:"d/m/Y" }}</li>
    <li>Người phụ trách: {{ warehouse_manager.get_full_name }}</li>
</ul>
<p>Vui lòng sắp xếp thời gian để nhận vật tư theo lịch trên. Nếu có thay đổi, bạn sẽ được thông báo.</p>
<p>Trân trọng,<br>Hệ thống Quản lý Kho</p>''',
                'is_active': True
            },
            
            # Mẫu thông báo yêu cầu đã hoàn thành
            {
                'code': 'request_completed',
                'type': 'notification',
                'name': 'Thông báo yêu cầu đã hoàn thành',
                'subject': 'Yêu cầu cấp phát #{{ request.request_code }} đã hoàn thành',
                'content': '''<p>Kính gửi {{ user.get_full_name }},</p>
<p>Yêu cầu cấp phát của bạn đã được hoàn thành.</p>
<p><strong>Thông tin yêu cầu:</strong></p>
<ul>
    <li>Mã yêu cầu: {{ request.request_code }}</li>
    <li>Tiêu đề: {{ request.title }}</li>
    <li>Trạng thái: Đã hoàn thành</li>
    <li>Ngày hoàn thành: {{ request.completed_date|date:"d/m/Y H:i" }}</li>
</ul>
<p>Vui lòng kiểm tra lại các vật tư đã cấp phát. Nếu có bất kỳ vấn đề gì, vui lòng liên hệ với bộ phận kho.</p>
<p>Trân trọng,<br>Hệ thống Quản lý Kho</p>''',
                'is_active': True
            },
        ]
        
        for template_data in templates:
            template, created = EmailTemplate.objects.update_or_create(
                code=template_data['code'],
                defaults=template_data
            )
            status = 'Tạo mới' if created else 'Cập nhật'
            self.stdout.write(self.style.SUCCESS(f"{status} mẫu email '{template.name}' thành công"))