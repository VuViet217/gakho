import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from inventory_requests.models import InventoryRequest

reqs = InventoryRequest.objects.all()
print(f'Total requests: {reqs.count()}')
print('\nStatus distribution:')
for status in ['draft', 'pending', 'approved', 'rejected', 'scheduled', 'completed', 'canceled']:
    count = reqs.filter(status=status).count()
    print(f'{status}: {count}')

print('\n\nApproved requests details:')
for r in reqs.filter(status='approved'):
    print(f'{r.request_code} - status={r.status} - approver={r.approver} - approval_date={r.approval_date}')

print('\n\nAll requests with non-draft status:')
for r in reqs.exclude(status='draft').order_by('-created_at')[:10]:
    print(f'{r.request_code} - status={r.status} - approver={r.approver}')
