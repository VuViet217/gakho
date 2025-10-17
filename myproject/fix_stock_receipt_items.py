"""
Script để sửa chữa các StockReceiptItem bằng cách liên kết chúng với PurchaseOrderItem.
"""

import os
import sys
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import transaction
from inventory.stock_models import StockReceipt, StockReceiptItem
from suppliers.models import PurchaseOrder, PurchaseOrderItem


def fix_stock_receipt_items():
    """
    Tìm tất cả các StockReceiptItem không có liên kết với PurchaseOrderItem
    và tạo liên kết dựa trên sản phẩm và đơn đặt hàng.
    """
    unlinked_items = StockReceiptItem.objects.filter(purchase_order_item__isnull=True)
    print(f"Tìm thấy {unlinked_items.count()} mục nhập kho không có liên kết")

    fixed_count = 0
    created_count = 0
    error_count = 0

    with transaction.atomic():
        for item in unlinked_items:
            try:
                # Lấy đơn đặt hàng từ phiếu nhập kho
                purchase_order = item.receipt.purchase_order
                if not purchase_order:
                    print(f"Lỗi: Mục nhập kho {item.id} không có đơn đặt hàng")
                    error_count += 1
                    continue

                # Tìm hoặc tạo mục trong đơn đặt hàng
                po_item, created = PurchaseOrderItem.objects.get_or_create(
                    purchase_order=purchase_order,
                    product=item.product,
                    defaults={
                        'quantity': item.quantity,
                        'unit_price': item.product.latest_purchase_price or 0
                    }
                )

                if created:
                    print(f"Đã tạo mới PurchaseOrderItem cho sản phẩm {item.product.name} trong đơn hàng {purchase_order.po_number}")
                    created_count += 1
                else:
                    print(f"Đã tìm thấy PurchaseOrderItem cho sản phẩm {item.product.name} trong đơn hàng {purchase_order.po_number}")

                # Liên kết StockReceiptItem với PurchaseOrderItem
                item.purchase_order_item = po_item
                item.save(update_fields=['purchase_order_item'])
                print(f"Đã liên kết StockReceiptItem {item.id} với PurchaseOrderItem {po_item.id}")
                fixed_count += 1

            except Exception as e:
                print(f"Lỗi khi xử lý mục nhập kho {item.id}: {str(e)}")
                error_count += 1

    print("\nKết quả:")
    print(f"- Đã sửa: {fixed_count} mục nhập kho")
    print(f"- Đã tạo: {created_count} mục đơn hàng mới")
    print(f"- Lỗi: {error_count} mục")


if __name__ == "__main__":
    print("Bắt đầu sửa chữa các mục nhập kho...")
    fix_stock_receipt_items()
    print("Hoàn thành!")