from django.urls import path
from . import views

urlpatterns = [
    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:pk>/update/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    
    # Purchase Order URLs
    path('purchase-orders/', views.po_list, name='po_list'),
    path('purchase-orders/create/', views.po_create, name='po_create'),
    path('purchase-orders/<int:pk>/', views.po_detail, name='po_detail'),
    path('purchase-orders/<int:pk>/update/', views.po_update, name='po_update'),
    path('purchase-orders/<int:pk>/delete/', views.po_delete, name='po_delete'),
    
    # Purchase Order Item URLs
    path('purchase-orders/items/<int:pk>/delete/', views.po_item_delete, name='po_item_delete'),
    path('purchase-orders/items/<int:pk>/update/', views.po_item_update, name='po_item_update'),
]