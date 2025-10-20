def menu_context(request):
    """
    Context processor that provides menu structure for all templates.
    This ensures consistent menu across all pages regardless of the app/template.
    """
    # Define the full menu structure
    menu = {
        'dashboard': {
            'name': 'Dashboard',
            'url': 'main_dashboard',
            'icon': 'fas fa-tachometer-alt',
            'active': False
        },
        'system_settings': {
            'name': 'Quản lý hệ thống',
            'icon': 'fas fa-cogs',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': 'Cấu hình Email', 'url': 'email_settings', 'icon': 'fas fa-envelope', 'active': False},
                {'name': 'Email mẫu', 'url': 'email_template_list', 'icon': 'fas fa-file-alt', 'active': False},
            ]
        },
        'employees': {
            'name': 'Quản lý nhân viên',
            'icon': 'fas fa-users',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': 'Danh sách nhân viên', 'url': 'employee_list', 'icon': 'fas fa-user-friends', 'active': False},
                {'name': 'Danh sách bộ phận', 'url': 'department_list', 'icon': 'fas fa-building', 'active': False},
                {'name': 'Nhập xuất dữ liệu', 'url': 'import_employees', 'icon': 'fas fa-file-import', 'active': False},
            ]
        },
        'suppliers': {
            'name': 'Quản lý nhà cung cấp',
            'icon': 'fas fa-truck',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': 'Danh sách nhà cung cấp', 'url': 'supplier_list', 'icon': 'fas fa-list', 'active': False},
                {'name': 'Thêm nhà cung cấp', 'url': 'supplier_create', 'icon': 'fas fa-plus-circle', 'active': False},
                {'name': 'Danh sách đơn hàng', 'url': 'po_list', 'icon': 'fas fa-file-invoice', 'active': False},
                {'name': 'Tạo đơn hàng mới', 'url': 'po_create', 'icon': 'fas fa-plus-square', 'active': False},
            ]
        },

        'inventory_requests': {
            'name': 'Yêu cầu cấp phát',
            'icon': 'fas fa-clipboard-list',
            'active': False,
            'open': False,
            'items': [
                {'name': 'Tạo yêu cầu mới', 'url': 'inventory_requests:inventory_request_create', 'icon': 'fas fa-plus', 'active': False},
                {'name': 'Yêu cầu của tôi', 'url': 'inventory_requests:my_requests', 'icon': 'fas fa-clipboard-check', 'active': False},
                {'name': 'Phê duyệt của tôi', 'url': 'inventory_requests:my_approval_requests', 'icon': 'fas fa-check-double', 'active': False, 'roles': ['admin', 'manager']},
                {'name': 'Quản lý kho', 'url': 'inventory_requests:warehouse_requests_list', 'icon': 'fas fa-dolly', 'active': False, 'roles': ['admin', 'sm', 'manager']},
                {'name': 'Tất cả yêu cầu', 'url': 'inventory_requests:inventory_request_list', 'icon': 'fas fa-list', 'active': False, 'roles': ['admin', 'sm', 'manager']},
            ]
        },
        'inventory': {
            'name': 'Quản lý kho',
            'icon': 'fas fa-warehouse',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': 'Sản phẩm', 'url': 'product_list', 'icon': 'fas fa-boxes', 'active': False},
                {'name': 'Thêm sản phẩm', 'url': 'product_create', 'icon': 'fas fa-plus-circle', 'active': False},
                {'name': 'Sản phẩm sắp hết', 'url': 'low_stock_products', 'icon': 'fas fa-exclamation-triangle', 'active': False},
                {'name': 'Phiếu nhập kho', 'url': 'stock_receipt_list', 'icon': 'fas fa-dolly-flatbed', 'active': False},
                {'name': 'Tạo phiếu nhập kho', 'url': 'stock_receipt_create', 'icon': 'fas fa-file-import', 'active': False},
                {'name': 'Danh mục', 'url': 'category_list', 'icon': 'fas fa-tags', 'active': False},
                {'name': 'Đơn vị tính', 'url': 'unit_list', 'icon': 'fas fa-balance-scale', 'active': False},
                {'name': 'Quản lý kho', 'url': 'warehouse_list', 'icon': 'fas fa-warehouse', 'active': False},
                {'name': 'Vị trí dãy', 'url': 'warehouse_row_list', 'icon': 'fas fa-th-list', 'active': False},
                {'name': 'Vị trí cột', 'url': 'warehouse_column_list', 'icon': 'fas fa-columns', 'active': False},
            ]
        },
        'user_management': {
            'name': 'Quản lý người dùng',
            'icon': 'fas fa-users-cog',
            'active': False,
            'open': False,
            'roles': ['manager', 'sm', 'admin'],
            'items': [
                {'name': 'Danh sách người dùng', 'url': 'user_list', 'icon': 'fas fa-users', 'active': False},
                {'name': 'Thêm người dùng', 'url': 'user_create', 'icon': 'fas fa-user-plus', 'active': False},
                {'name': 'Hồ sơ cá nhân', 'url': 'profile_view', 'icon': 'fas fa-user-circle', 'active': False},
            ]
        }
    }
    
    # Set active state based on current URL path
    path = request.path
    
    # Dashboard
    if path == '/' or 'dashboard' in path:
        menu['dashboard']['active'] = True
    
    # Employees section
    if 'employee' in path or 'department' in path:
        menu['employees']['active'] = True
        menu['employees']['open'] = True
        
        if 'employee_list' in path:
            menu['employees']['items'][0]['active'] = True
        elif 'department_list' in path:
            menu['employees']['items'][1]['active'] = True
        elif 'import_employees' in path:
            menu['employees']['items'][2]['active'] = True
    
    # Suppliers section
    if 'procurement/supplier' in path or 'supplier' in path or 'purchase-order' in path or 'po_' in path:
        menu['suppliers']['active'] = True
        menu['suppliers']['open'] = True
        
        if 'supplier_list' in path or 'suppliers/' in path:
            menu['suppliers']['items'][0]['active'] = True
        elif 'supplier_create' in path or 'supplier/create' in path:
            menu['suppliers']['items'][1]['active'] = True
        elif 'po_list' in path or 'purchase-orders/' in path:
            menu['suppliers']['items'][2]['active'] = True
        elif 'po_create' in path or 'purchase-order/create' in path:
            menu['suppliers']['items'][3]['active'] = True
    
    # Inventory Requests section
    if 'inventory/requests/' in path:
        menu['inventory_requests']['active'] = True
        menu['inventory_requests']['open'] = True
        
        if 'inventory/requests/create' in path:
            menu['inventory_requests']['items'][0]['active'] = True
        elif 'inventory/requests/my-requests' in path:
            menu['inventory_requests']['items'][1]['active'] = True
        elif 'inventory/requests/my-approvals' in path:
            menu['inventory_requests']['items'][2]['active'] = True
        elif 'inventory/requests/warehouse-requests' in path:
            menu['inventory_requests']['items'][3]['active'] = True
        elif path == '/inventory/requests/' or 'inventory/requests/' in path and not any(s in path for s in ['create', 'my-requests', 'my-approvals', 'warehouse-requests']):
            menu['inventory_requests']['items'][4]['active'] = True
    
    # Inventory section
    if 'inventory/' in path and not 'inventory/requests/' in path:
        menu['inventory']['active'] = True
        menu['inventory']['open'] = True
        
        if 'product_list' in path or 'products/' in path and not any(s in path for s in ['create', 'low-stock']):
            menu['inventory']['items'][0]['active'] = True
        elif 'product_create' in path or 'products/add' in path:
            menu['inventory']['items'][1]['active'] = True
        elif 'low_stock_products' in path or 'low-stock' in path:
            menu['inventory']['items'][2]['active'] = True
        elif 'stock_receipt_list' in path or 'stock-receipts/' in path and 'create' not in path:
            menu['inventory']['items'][3]['active'] = True
        elif 'stock_receipt_create' in path or 'stock-receipts/create' in path:
            menu['inventory']['items'][4]['active'] = True
        elif 'category_list' in path or 'categories/' in path:
            menu['inventory']['items'][5]['active'] = True
        elif 'unit_list' in path or 'units/' in path:
            menu['inventory']['items'][6]['active'] = True
        elif 'warehouse_list' in path or 'warehouses/' in path:
            menu['inventory']['items'][7]['active'] = True
        elif 'warehouse_row_list' in path or 'warehouse-rows/' in path:
            menu['inventory']['items'][8]['active'] = True
        elif 'warehouse_column_list' in path or 'warehouse-columns/' in path:
            menu['inventory']['items'][9]['active'] = True
    
    # User management section
    if '/users/' in path or '/profile' in path:
        menu['user_management']['active'] = True
        menu['user_management']['open'] = True
        
        if 'user_list' in path or ('/users/' in path and 'create' not in path and 'edit' not in path and 'delete' not in path):
            menu['user_management']['items'][0]['active'] = True
        elif 'user_create' in path or '/users/create' in path:
            menu['user_management']['items'][1]['active'] = True
        elif '/profile' in path:
            menu['user_management']['items'][2]['active'] = True
            
    # System settings section
    if '/system/' in path:
        menu['system_settings']['active'] = True
        menu['system_settings']['open'] = True
        
        if 'email_settings' in path or ('email' in path and 'template' not in path):
            menu['system_settings']['items'][0]['active'] = True
        elif 'email_template' in path or 'templates' in path:
            menu['system_settings']['items'][1]['active'] = True
    
    return {
        'menu': menu
    }