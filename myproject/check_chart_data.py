import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from inventory.stock_models import StockReceipt, StockReceiptItem
from inventory_requests.models import InventoryRequest, EmployeeProductRequest
from datetime import datetime, timedelta

print("=== KIEM TRA DU LIEU CHO BIEU DO ===\n")

# Kiểm tra StockReceipt (nhập kho)
receipts = StockReceipt.objects.all()
receipt_items = StockReceiptItem.objects.all()
print(f"1. NHAP KHO (StockReceipt):")
print(f"   - Tong so phieu nhap: {receipts.count()}")
print(f"   - Tong so chi tiet nhap: {receipt_items.count()}")

if receipt_items.count() > 0:
    total_in = sum(item.quantity for item in receipt_items)
    print(f"   - Tong so luong nhap: {total_in}")
    print(f"\n   5 phieu nhap gan nhat:")
    for receipt in receipts[:5]:
        items_count = receipt.items.count()
        total = sum(item.quantity for item in receipt.items.all())
        print(f"   - {receipt.receipt_number}: {receipt.receipt_date.strftime('%d/%m/%Y')} - {items_count} san pham - Tong SL: {total}")

print(f"\n2. XUAT KHO (InventoryRequest completed):")
completed_requests = InventoryRequest.objects.filter(status='completed')
print(f"   - Tong yeu cau hoan thanh: {completed_requests.count()}")

if completed_requests.count() > 0:
    print(f"\n   5 yeu cau hoan thanh gan nhat:")
    for req in completed_requests[:5]:
        issued_items = req.employee_products.filter(issued_quantity__gt=0)
        total = sum(item.issued_quantity for item in issued_items)
        print(f"   - {req.request_code}: {req.completed_date.strftime('%d/%m/%Y') if req.completed_date else 'N/A'} - Tong SL xuat: {total}")

print("\n=== KET QUA ===")
if receipt_items.count() == 0 and completed_requests.count() == 0:
    print("CHUA CO DU LIEU!")
    print("\nHuong dan:")
    print("1. Tao phieu nhap kho: http://127.0.0.1:8000/inventory/stock-receipts/create/")
    print("2. Hoan thanh yeu cau cap phat: http://127.0.0.1:8000/inventory_requests/")
elif receipt_items.count() == 0:
    print("Chi co du lieu XUAT, chua co NHAP!")
    print("Tao phieu nhap kho: http://127.0.0.1:8000/inventory/stock-receipts/create/")
elif completed_requests.count() == 0:
    print("Chi co du lieu NHAP, chua co XUAT!")
    print("Hoan thanh yeu cau cap phat: http://127.0.0.1:8000/inventory_requests/")
else:
    print("CO DU LIEU! Bieu do se hien thi.")
