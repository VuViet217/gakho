import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from inventory_requests.models import InventoryRequest, EmployeeProductRequest

print("=== CAP NHAT ISSUED_QUANTITY CHO CAC YEU CAU DA HOAN THANH ===\n")

# Lấy tất cả yêu cầu đã hoàn thành
completed_requests = InventoryRequest.objects.filter(status='completed')
print(f"Tong so yeu cau da hoan thanh: {completed_requests.count()}\n")

updated_count = 0
for req in completed_requests:
    print(f"Dang xu ly: {req.request_code}")
    
    for ep in req.employee_products.all():
        # Nếu issued_quantity = 0 hoặc None, cập nhật = approved_quantity (hoặc quantity)
        if ep.issued_quantity == 0 or ep.issued_quantity is None:
            # Ưu tiên approved_quantity, nếu không có thì dùng quantity
            ep.issued_quantity = ep.approved_quantity if ep.approved_quantity else ep.quantity
            ep.save()
            print(f"  - Cap nhat {ep.product.name}: issued = {ep.issued_quantity}")
            updated_count += 1
        else:
            print(f"  - {ep.product.name}: da co issued = {ep.issued_quantity} (bo qua)")

print(f"\n=== HOAN THANH ===")
print(f"Da cap nhat {updated_count} employee_product")
print(f"\nVui long refresh dashboard de xem bieu do!")
