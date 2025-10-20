from django.core.management.base import BaseCommand
from system_settings.models import Menu, SubMenu

class Command(BaseCommand):
    help = 'Tạo/cập nhật menu cho chức năng yêu cầu cấp phát'

    def handle(self, *args, **kwargs):
        # Tạo menu chính nếu chưa có
        inventory_menu, created = Menu.objects.update_or_create(
            code='inventory',
            defaults={
                'name': 'Quản lý kho',
                'icon': 'fas fa-warehouse',
                'order': 4,
                'is_active': True
            }
        )
        status = 'Tạo mới' if created else 'Cập nhật'
        self.stdout.write(self.style.SUCCESS(f"{status} menu '{inventory_menu.name}' thành công"))
        
        # Tạo các submenu
        submenus = [
            {
                'code': 'request_create',
                'name': 'Tạo yêu cầu mới',
                'url': 'inventory_requests:inventory_request_create',
                'icon': 'fas fa-plus',
                'order': 1,
                'parent': inventory_menu,
                'roles': 'all',
                'is_active': True
            },
            {
                'code': 'my_requests',
                'name': 'Yêu cầu của tôi',
                'url': 'inventory_requests:my_requests',
                'icon': 'fas fa-clipboard-list',
                'order': 2,
                'parent': inventory_menu,
                'roles': 'all',
                'is_active': True
            },
            {
                'code': 'my_approvals',
                'name': 'Phê duyệt của tôi',
                'url': 'inventory_requests:my_approval_requests',
                'icon': 'fas fa-check-double',
                'order': 3,
                'parent': inventory_menu,
                'roles': 'admin,manager',
                'is_active': True
            },
            {
                'code': 'warehouse_requests',
                'name': 'Quản lý kho',
                'url': 'inventory_requests:warehouse_requests_list',
                'icon': 'fas fa-dolly',
                'order': 4,
                'parent': inventory_menu,
                'roles': 'admin,sm,manager',
                'is_active': True
            },
            {
                'code': 'request_list',
                'name': 'Tất cả yêu cầu',
                'url': 'inventory_requests:inventory_request_list',
                'icon': 'fas fa-list',
                'order': 5,
                'parent': inventory_menu,
                'roles': 'admin,sm',
                'is_active': True
            }
        ]
        
        for submenu_data in submenus:
            submenu, created = SubMenu.objects.update_or_create(
                code=submenu_data['code'],
                defaults=submenu_data
            )
            status = 'Tạo mới' if created else 'Cập nhật'
            self.stdout.write(self.style.SUCCESS(f"{status} submenu '{submenu.name}' thành công"))