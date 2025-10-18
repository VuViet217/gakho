from django.core.management.base import BaseCommand
from django.urls import reverse
from accounts.models import User

class Command(BaseCommand):
    help = 'Kiểm tra và in ra các URL cho chức năng yêu cầu cấp phát'

    def handle(self, *args, **kwargs):
        urls = [
            'inventory_requests:inventory_request_create',
            'inventory_requests:my_requests',
            'inventory_requests:my_approval_requests',
            'inventory_requests:warehouse_requests_list',
            'inventory_requests:inventory_request_list'
        ]
        
        for url_name in urls:
            try:
                url = reverse(url_name)
                self.stdout.write(self.style.SUCCESS(f"URL {url_name}: {url}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Lỗi khi lấy URL {url_name}: {str(e)}"))