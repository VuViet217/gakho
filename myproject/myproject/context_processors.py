from django.utils.translation import gettext_lazy as _

def menu_context(request):
    """
    Context processor that provides menu structure for all templates.
    This ensures consistent menu across all pages regardless of the app/template.
    Thứ tự menu: Nhà cung cấp → Kho → Nhân viên → Người dùng → Yêu cầu → Báo cáo → Cài đặt
    """
    # Define the full menu structure (Ordered from top to bottom)
    from collections import OrderedDict
    
    menu_items = OrderedDict([
        ('dashboard', {
            'name': _('Dashboard'),
            'url': 'main_dashboard',
            'icon': 'fas fa-tachometer-alt',
            'active': False
        }),
        ('suppliers', {
            'name': _('Quản lý nhà cung cấp'),
            'icon': 'fas fa-truck-loading',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': _('Danh sách nhà cung cấp'), 'url': 'supplier_list', 'icon': 'fas fa-list-ul', 'active': False},
                {'name': _('Thêm nhà cung cấp'), 'url': 'supplier_create', 'icon': 'fas fa-plus-circle', 'active': False},
                {'name': _('Danh sách đơn hàng'), 'url': 'po_list', 'icon': 'fas fa-file-invoice-dollar', 'active': False},
                {'name': _('Tạo đơn hàng mới'), 'url': 'po_create', 'icon': 'fas fa-cart-plus', 'active': False},
            ]
        }),
        ('inventory', {
            'name': _('Quản lý kho'),
            'icon': 'fas fa-warehouse',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': _('Danh sách sản phẩm'), 'url': 'product_list', 'icon': 'fas fa-boxes', 'active': False},
                {'name': _('Thêm sản phẩm'), 'url': 'product_create', 'icon': 'fas fa-plus-square', 'active': False},
                {'name': _('Sản phẩm sắp hết'), 'url': 'low_stock_products', 'icon': 'fas fa-exclamation-triangle text-warning', 'active': False},
                {'name': _('Phiếu nhập kho'), 'url': 'stock_receipt_list', 'icon': 'fas fa-clipboard-list', 'active': False},
                {'name': _('Tạo phiếu nhập kho'), 'url': 'stock_receipt_create', 'icon': 'fas fa-file-import', 'active': False},
                {'name': _('Quản lý kho'), 'url': 'warehouse_list', 'icon': 'fas fa-building', 'active': False},
                {'name': _('Vị trí dãy'), 'url': 'warehouse_row_list', 'icon': 'fas fa-stream', 'active': False},
                {'name': _('Vị trí cột'), 'url': 'warehouse_column_list', 'icon': 'fas fa-grip-vertical', 'active': False},
                {'name': _('Danh mục sản phẩm'), 'url': 'category_list', 'icon': 'fas fa-tags', 'active': False},
                {'name': _('Đơn vị tính'), 'url': 'unit_list', 'icon': 'fas fa-ruler-combined', 'active': False},
            ]
        }),
        ('employees', {
            'name': _('Quản lý nhân viên'),
            'icon': 'fas fa-user-tie',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': _('Danh sách nhân viên'), 'url': 'employee_list', 'icon': 'fas fa-users', 'active': False},
                {'name': _('Danh sách bộ phận'), 'url': 'department_list', 'icon': 'fas fa-sitemap', 'active': False},
                {'name': _('Nhập xuất dữ liệu'), 'url': 'import_employees', 'icon': 'fas fa-file-excel', 'active': False},
            ]
        }),
        ('user_management', {
            'name': _('Quản lý người dùng'),
            'icon': 'fas fa-users-cog',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': _('Danh sách người dùng'), 'url': 'user_list', 'icon': 'fas fa-users', 'active': False},
                {'name': _('Thêm người dùng'), 'url': 'user_create', 'icon': 'fas fa-user-plus', 'active': False},
                {'name': _('Hồ sơ cá nhân'), 'url': 'profile_view', 'icon': 'fas fa-id-card', 'active': False},
            ]
        }),
        ('inventory_requests', {
            'name': _('Yêu cầu cấp phát'),
            'icon': 'fas fa-hand-holding-medical',
            'active': False,
            'open': False,
            'items': [
                {'name': _('Tạo yêu cầu mới'), 'url': 'inventory_requests:inventory_request_create', 'icon': 'fas fa-plus-circle', 'active': False},
                {'name': _('Yêu cầu của tôi'), 'url': 'inventory_requests:my_requests', 'icon': 'fas fa-clipboard-list', 'active': False},
                {'name': _('Phê duyệt của tôi'), 'url': 'inventory_requests:my_approval_requests', 'icon': 'fas fa-check-double', 'active': False},
                {'name': _('Quản lý kho - Xử lý'), 'url': 'inventory_requests:warehouse_requests_list', 'icon': 'fas fa-dolly', 'active': False, 'roles': ['admin', 'sm', 'manager']},
                {'name': _('Tất cả yêu cầu'), 'url': 'inventory_requests:inventory_request_list', 'icon': 'fas fa-list-alt', 'active': False},
                {'name': _('Lịch sử giao nhận'), 'url': 'inventory_requests:employee_delivery_history', 'icon': 'fas fa-history', 'active': False},
            ]
        }),
        ('reports', {
            'name': _('Báo cáo'),
            'icon': 'fas fa-chart-line',
            'active': False,
             'roles': ['manager', 'sm', 'admin'],
            'open': False,
            'items': [
                {'name': _('Tổng quan'), 'url': 'reports:dashboard', 'icon': 'fas fa-chart-pie', 'active': False},
                {'name': _('Báo cáo tháng'), 'url': 'reports:monthly_report', 'icon': 'fas fa-calendar-check', 'active': False},
                {'name': _('Sản phẩm sắp hết'), 'url': 'reports:low_stock_report', 'icon': 'fas fa-bell', 'active': False},
                {'name': _('Kiểm kê kho'), 'url': 'reports:audit_list', 'icon': 'fas fa-tasks', 'active': False},
            ]
        }),
        ('system_settings', {
            'name': _('Cấu hình hệ thống'),
            'icon': 'fas fa-cog',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': _('Cấu hình Email'), 'url': 'email_settings', 'icon': 'fas fa-envelope-open-text', 'active': False},
                {'name': _('Quản lý mẫu email'), 'url': 'email_template_list', 'icon': 'fas fa-file-alt', 'active': False},
            ]
        }),
    ])
    
    # Set active state based on current URL path
    path = request.path
    
    # Dashboard
    if path == '/' or 'dashboard' in path:
        menu_items['dashboard']['active'] = True
    
    # Employees section
    if 'employee' in path or 'department' in path:
        menu_items['employees']['active'] = True
        menu_items['employees']['open'] = True
        
        if 'employee_list' in path:
            menu_items['employees']['items'][0]['active'] = True
        elif 'department_list' in path:
            menu_items['employees']['items'][1]['active'] = True
        elif 'import_employees' in path:
            menu_items['employees']['items'][2]['active'] = True
    
    # Suppliers section
    if 'procurement/supplier' in path or 'supplier' in path or 'purchase-order' in path or 'po_' in path:
        menu_items['suppliers']['active'] = True
        menu_items['suppliers']['open'] = True
        
        if 'supplier_list' in path or 'suppliers/' in path:
            menu_items['suppliers']['items'][0]['active'] = True
        elif 'supplier_create' in path or 'supplier/create' in path:
            menu_items['suppliers']['items'][1]['active'] = True
        elif 'po_list' in path or 'purchase-orders/' in path:
            menu_items['suppliers']['items'][2]['active'] = True
        elif 'po_create' in path or 'purchase-order/create' in path:
            menu_items['suppliers']['items'][3]['active'] = True
    
    # Inventory Requests section
    if 'inventory/requests/' in path:
        menu_items['inventory_requests']['active'] = True
        menu_items['inventory_requests']['open'] = True
        
        if 'inventory/requests/create' in path:
            menu_items['inventory_requests']['items'][0]['active'] = True
        elif 'inventory/requests/my-requests' in path:
            menu_items['inventory_requests']['items'][1]['active'] = True
        elif 'inventory/requests/my-approvals' in path:
            menu_items['inventory_requests']['items'][2]['active'] = True
        elif 'inventory/requests/warehouse-requests' in path:
            menu_items['inventory_requests']['items'][3]['active'] = True
        elif 'inventory/requests/employee-delivery-history' in path:
            menu_items['inventory_requests']['items'][5]['active'] = True
        elif path == '/inventory/requests/' or 'inventory/requests/' in path and not any(s in path for s in ['create', 'my-requests', 'my-approvals', 'warehouse-requests', 'employee-delivery-history']):
            menu_items['inventory_requests']['items'][4]['active'] = True
    
    # Inventory section
    if 'inventory/' in path and not 'inventory/requests/' in path:
        menu_items['inventory']['active'] = True
        menu_items['inventory']['open'] = True
        
        if 'product_list' in path or 'products/' in path and not any(s in path for s in ['create', 'low-stock']):
            menu_items['inventory']['items'][0]['active'] = True
        elif 'product_create' in path or 'products/add' in path:
            menu_items['inventory']['items'][1]['active'] = True
        elif 'low_stock_products' in path or 'low-stock' in path:
            menu_items['inventory']['items'][2]['active'] = True
        elif 'stock_receipt_list' in path or 'stock-receipts/' in path and 'create' not in path:
            menu_items['inventory']['items'][3]['active'] = True
        elif 'stock_receipt_create' in path or 'stock-receipts/create' in path:
            menu_items['inventory']['items'][4]['active'] = True
        elif 'category_list' in path or 'categories/' in path:
            menu_items['inventory']['items'][5]['active'] = True
        elif 'unit_list' in path or 'units/' in path:
            menu_items['inventory']['items'][6]['active'] = True
        elif 'warehouse_list' in path or 'warehouses/' in path:
            menu_items['inventory']['items'][7]['active'] = True
        elif 'warehouse_row_list' in path or 'warehouse-rows/' in path:
            menu_items['inventory']['items'][8]['active'] = True
        elif 'warehouse_column_list' in path or 'warehouse-columns/' in path:
            menu_items['inventory']['items'][9]['active'] = True
    
    # Reports section
    if '/reports/' in path:
        menu_items['reports']['active'] = True
        menu_items['reports']['open'] = True
        
        if path == '/reports/' or 'dashboard' in path:
            menu_items['reports']['items'][0]['active'] = True
        elif 'monthly' in path:
            menu_items['reports']['items'][1]['active'] = True
        elif 'low-stock' in path:
            menu_items['reports']['items'][2]['active'] = True
        elif 'audit' in path:
            menu_items['reports']['items'][3]['active'] = True
    
    # User management section
    if '/users/' in path or '/profile' in path:
        menu_items['user_management']['active'] = True
        menu_items['user_management']['open'] = True
        
        if 'user_list' in path or ('/users/' in path and 'create' not in path and 'edit' not in path and 'delete' not in path):
            menu_items['user_management']['items'][0]['active'] = True
        elif 'user_create' in path or '/users/create' in path:
            menu_items['user_management']['items'][1]['active'] = True
        elif '/profile' in path:
            menu_items['user_management']['items'][2]['active'] = True
            
    # System settings section
    if '/system/' in path:
        menu_items['system_settings']['active'] = True
        menu_items['system_settings']['open'] = True
        
        if 'email_settings' in path or ('email' in path and 'template' not in path):
            menu_items['system_settings']['items'][0]['active'] = True
        elif 'email_template' in path or 'templates' in path:
            menu_items['system_settings']['items'][1]['active'] = True
    
    return {
        'menu': menu_items,  # Giữ tên 'menu' cho compatibility với code cũ
        'menu_items': menu_items  # Thêm 'menu_items' cho code mới
    }