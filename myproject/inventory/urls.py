from django.urls import path
from . import views
from . import stock_views

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Unit URLs
    path('units/', views.UnitListView.as_view(), name='unit_list'),
    path('units/<int:pk>/', views.UnitDetailView.as_view(), name='unit_detail'),
    path('units/add/', views.UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/edit/', views.UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit_delete'),
    
    # Warehouse URLs
    path('warehouses/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouses/add/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouses/<int:pk>/edit/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouses/<int:pk>/delete/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),
    
    # Warehouse Row URLs
    path('warehouse-rows/', views.WarehouseRowListView.as_view(), name='warehouse_row_list'),
    path('warehouse-rows/<int:pk>/', views.WarehouseRowDetailView.as_view(), name='warehouse_row_detail'),
    path('warehouse-rows/add/', views.WarehouseRowCreateView.as_view(), name='warehouse_row_create'),
    path('warehouse-rows/<int:pk>/edit/', views.WarehouseRowUpdateView.as_view(), name='warehouse_row_update'),
    path('warehouse-rows/<int:pk>/delete/', views.WarehouseRowDeleteView.as_view(), name='warehouse_row_delete'),
    
    # Warehouse Column URLs
    path('warehouse-columns/', views.WarehouseColumnListView.as_view(), name='warehouse_column_list'),
    path('warehouse-columns/<int:pk>/', views.WarehouseColumnDetailView.as_view(), name='warehouse_column_detail'),
    path('warehouse-columns/add/', views.WarehouseColumnCreateView.as_view(), name='warehouse_column_create'),
    path('warehouse-columns/<int:pk>/edit/', views.WarehouseColumnUpdateView.as_view(), name='warehouse_column_update'),
    path('warehouse-columns/<int:pk>/delete/', views.WarehouseColumnDeleteView.as_view(), name='warehouse_column_delete'),
    
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Other URLs
    path('products/low-stock/', views.LowStockProductsView.as_view(), name='low_stock_products'),
    
    # Stock Receipt URLs
    path('stock-receipts/', stock_views.stock_receipt_list, name='stock_receipt_list'),
    path('stock-receipts/create/', stock_views.stock_receipt_create, name='stock_receipt_create'),
    path('stock-receipts/<int:pk>/', stock_views.stock_receipt_detail, name='stock_receipt_detail'),
    path('api/purchase-order-items/', stock_views.get_purchase_order_items, name='get_purchase_order_items'),
]