from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Q, F, Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from inventory.models import Product
from suppliers.models import PurchaseOrder, Supplier
import json

@method_decorator(login_required, name='dispatch')
class MainDashboardView(TemplateView):
    template_name = 'main_dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'OVNC - Trang chủ'
        
        # Lấy thời gian hiện tại
        today = timezone.now()
        
        # Add dashboard stats
        context['products_count'] = Product.objects.count()
        context['purchase_orders_count'] = PurchaseOrder.objects.count()
        context['suppliers_count'] = Supplier.objects.count()
        
        # Sản phẩm sắp hết: current_quantity <= minimum_quantity
        context['low_stock_count'] = Product.objects.filter(
            current_quantity__lte=F('minimum_quantity')
        ).count()
        
        # KPI: Mục tiêu hoàn thành
        from inventory.stock_models import StockReceipt
        from inventory_requests.models import InventoryRequest
        
        # 1. Nhập kho từ PO (tháng này)
        current_month_start = datetime(today.year, today.month, 1)
        receipts_this_month = StockReceipt.objects.filter(
            receipt_date__gte=current_month_start
        ).count()
        context['receipts_this_month'] = receipts_this_month
        context['receipts_target'] = 20  # Mục tiêu 20 phiếu nhập/tháng
        context['receipts_percent'] = min(int((receipts_this_month / 20) * 100), 100)
        
        # 2. Yêu cầu cấp phát hoàn thành (tháng này)
        requests_completed_this_month = InventoryRequest.objects.filter(
            status='completed',
            completed_date__gte=current_month_start
        ).count()
        context['requests_completed'] = requests_completed_this_month
        context['requests_target'] = 30  # Mục tiêu 30 yêu cầu/tháng
        context['requests_percent'] = min(int((requests_completed_this_month / 30) * 100), 100)
        
        # 3. Sản phẩm có tồn kho đủ (không sắp hết)
        total_products = Product.objects.count()
        products_sufficient = total_products - context['low_stock_count']
        context['products_sufficient'] = products_sufficient
        context['products_sufficient_percent'] = int((products_sufficient / total_products * 100)) if total_products > 0 else 0
        
        # 4. Tỷ lệ yêu cầu được duyệt (tháng này)
        total_requests_this_month = InventoryRequest.objects.filter(
            created_at__gte=current_month_start
        ).count()
        approved_requests_this_month = InventoryRequest.objects.filter(
            created_at__gte=current_month_start,
            status__in=['approved', 'scheduled', 'completed']
        ).count()
        context['approval_rate'] = int((approved_requests_this_month / total_requests_this_month * 100)) if total_requests_this_month > 0 else 0
        context['approved_count'] = approved_requests_this_month
        context['total_requests_month'] = total_requests_this_month
        
        # Tổng số lượng nhập/xuất tháng này (cho bảng)
        from inventory.stock_models import StockReceiptItem
        from inventory_requests.models import EmployeeProductRequest
        
        total_import = StockReceiptItem.objects.filter(
            receipt__receipt_date__gte=current_month_start
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        total_export = EmployeeProductRequest.objects.filter(
            request__status='completed',
            request__completed_date__gte=current_month_start
        ).aggregate(total=Sum('issued_quantity'))['total'] or 0
        
        context['total_import_qty'] = total_import
        context['total_export_qty'] = total_export
        context['current_month'] = today.strftime('%m/%Y')
        
        # PO gần đây (5 PO mới nhất)
        recent_pos = PurchaseOrder.objects.select_related('supplier').order_by('-order_date')[:5]
        context['recent_pos'] = recent_pos
        
        # Sản phẩm sắp hết hàng (5 sản phẩm)
        low_stock_products = Product.objects.filter(
            current_quantity__lte=F('minimum_quantity')
        ).select_related('unit').order_by('current_quantity')[:5]
        context['low_stock_products'] = low_stock_products
        
        # Lấy dữ liệu 10 tháng gần nhất cho biểu đồ
        start_date = today - timedelta(days=300)  # ~10 tháng
        
        # Nhập kho (từ StockReceipt - phiếu nhập kho)
        from inventory.stock_models import StockReceipt, StockReceiptItem
        
        import_by_month = StockReceiptItem.objects.filter(
            receipt__receipt_date__gte=start_date
        ).annotate(
            month=TruncMonth('receipt__receipt_date')
        ).values('month').annotate(
            total_quantity=Sum('quantity')
        ).order_by('month')
        
        # Xuất kho (từ InventoryRequest đã hoàn thành)
        from inventory_requests.models import InventoryRequest, EmployeeProductRequest
        
        export_by_month = EmployeeProductRequest.objects.filter(
            request__completed_date__gte=start_date,
            request__status='completed'
        ).annotate(
            month=TruncMonth('request__completed_date')
        ).values('month').annotate(
            total_quantity=Sum('issued_quantity')
        ).order_by('month')
        
        # Tạo dict để map tháng -> số lượng
        import_data = {}
        for item in import_by_month:
            if item['month'] and item['total_quantity']:
                month_key = item['month'].strftime('%Y-%m')
                import_data[month_key] = item['total_quantity']
        
        export_data = {}
        for item in export_by_month:
            if item['month'] and item['total_quantity']:
                month_key = item['month'].strftime('%Y-%m')
                export_data[month_key] = item['total_quantity']
        
        # Tạo danh sách 10 tháng gần nhất
        months = []
        import_values = []
        export_values = []
        
        for i in range(9, -1, -1):
            month_date = today - timedelta(days=30*i)
            month_key = month_date.strftime('%Y-%m')
            month_label = f"Tháng {month_date.month}"
            
            months.append(month_label)
            import_values.append(import_data.get(month_key, 0))
            export_values.append(export_data.get(month_key, 0))
        
        context['chart_months'] = json.dumps(months)
        context['chart_import_data'] = json.dumps(import_values)
        context['chart_export_data'] = json.dumps(export_values)
        
        return context
        
@method_decorator(login_required, name='dispatch')
class TestDashboardView(TemplateView):
    template_name = 'main_dashboard/test_dashboard.html'
