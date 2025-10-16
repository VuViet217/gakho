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
        'employees': {
            'name': 'Quản lý nhân viên',
            'icon': 'fas fa-users',
            'active': False,
            'open': False,
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
            'items': [
                {'name': 'Danh sách nhà cung cấp', 'url': 'supplier_list', 'icon': 'fas fa-list', 'active': False},
                {'name': 'Thêm nhà cung cấp', 'url': 'supplier_create', 'icon': 'fas fa-plus-circle', 'active': False},
                {'name': 'Danh sách đơn hàng', 'url': 'po_list', 'icon': 'fas fa-file-invoice', 'active': False},
                {'name': 'Tạo đơn hàng mới', 'url': 'po_create', 'icon': 'fas fa-plus-square', 'active': False},
            ]
        },
        'products': {
            'name': 'Sản phẩm',
            'icon': 'fas fa-boxes',
            'active': False,
            'open': False,
            'items': [
                {'name': 'Danh sách sản phẩm', 'url': '#', 'icon': 'far fa-circle', 'active': False},
                {'name': 'Thêm sản phẩm', 'url': '#', 'icon': 'far fa-circle', 'active': False},
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
    
    return {
        'menu': menu
    }