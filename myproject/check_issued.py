import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from inventory_requests.models import InventoryRequest, EmployeeProductRequest

# Kiem tra yeu cau hoan thanh
completed_requests = InventoryRequest.objects.filter(status='completed').order_by('-completed_date')
print(f"Total completed requests: {completed_requests.count()}\n")

for req in completed_requests[:3]:
    print(f"Request: {req.request_code} - Status: {req.status}")
    print(f"Completed: {req.completed_date}")
    print(f"Employee Products: {req.employee_products.count()}")
    
    total_issued = 0
    for ep in req.employee_products.all():
        print(f"  - Product: {ep.product.name}")
        print(f"    Quantity: {ep.quantity}, Issued: {ep.issued_quantity}")
        total_issued += ep.issued_quantity
    
    print(f"  TOTAL ISSUED: {total_issued}\n")

# Kiem tra tong
from django.db.models import Sum
total = EmployeeProductRequest.objects.filter(
    request__status='completed'
).aggregate(total=Sum('issued_quantity'))
print(f"\nTOTAL ISSUED from all completed requests: {total['total']}")
