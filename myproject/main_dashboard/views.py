from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Q, F
from inventory.models import Product
from suppliers.models import PurchaseOrder, Supplier

@method_decorator(login_required, name='dispatch')
class MainDashboardView(TemplateView):
    template_name = 'main_dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'OVNC - Trang chủ'
        
        # Add dashboard stats
        context['products_count'] = Product.objects.count()
        context['purchase_orders_count'] = PurchaseOrder.objects.count()
        context['suppliers_count'] = Supplier.objects.count()
        
        # Sản phẩm sắp hết: current_quantity <= minimum_quantity
        context['low_stock_count'] = Product.objects.filter(
            current_quantity__lte=F('minimum_quantity')
        ).count()
        
        return context
        
@method_decorator(login_required, name='dispatch')
class TestDashboardView(TemplateView):
    template_name = 'main_dashboard/test_dashboard.html'
