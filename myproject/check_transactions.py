import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from inventory.models import StockTransaction, Product
from datetime import datetime

# Kiểm tra có transaction nào không
transactions = StockTransaction.objects.all()
print(f"Total transactions: {transactions.count()}")

# Kiểm tra theo loại
in_count = StockTransaction.objects.filter(transaction_type='IN').count()
out_count = StockTransaction.objects.filter(transaction_type='OUT').count()
print(f"IN transactions: {in_count}")
print(f"OUT transactions: {out_count}")

if transactions.count() == 0:
    print("\n=== CHUA CO DU LIEU ===")
    print("Ban can:")
    print("1. Tao phieu nhap kho (Stock Receipt) de co giao dich NHAP")
    print("2. Hoan thanh yeu cau cap phat de co giao dich XUAT")
    print("\nTao du lieu mau? (y/n)")
else:
    print(f"\n=== 5 GIAO DICH GAN NHAT ===")
    for t in transactions[:5]:
        print(f"- {t.transaction_code}: {t.get_transaction_type_display()} {t.quantity} {t.product.name} - {t.transaction_date}")
