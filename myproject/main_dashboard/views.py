from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

@method_decorator(login_required, name='dispatch')
class MainDashboardView(TemplateView):
    template_name = 'main_dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'OVNC - Trang chủ'
        
        # Add dashboard stats
        context['products_count'] = 0
        context['purchase_orders_count'] = 0
        context['suppliers_count'] = 0
        context['low_stock_count'] = 0
        
        return context
        
@method_decorator(login_required, name='dispatch')
class TestDashboardView(TemplateView):
    template_name = 'main_dashboard/test_dashboard.html'
