from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from inventory.models import Product
from system_settings.template_email_service import send_template_email
from system_settings.utils import get_template_by_code


class Command(BaseCommand):
    help = 'Gửi email cảnh báo sản phẩm sắp hết (dựa trên minimum_quantity)'

    def add_arguments(self, parser):
        parser.add_argument('--template', type=str, default='low_stock_alert', help='Mã mẫu email sử dụng')
        parser.add_argument('--force', action='store_true', help='Bắt buộc gửi ngay cả khi không có recipients')

    def handle(self, *args, **options):
        template_code = options['template']
        force = options['force']

        template = get_template_by_code(template_code)
        if not template:
            self.stdout.write(self.style.ERROR(f'Mẫu email không tồn tại hoặc chưa kích hoạt: {template_code}'))
            return

        # Lấy danh sách sản phẩm dưới ngưỡng
        low_products = Product.objects.filter(current_quantity__lte=models.F('minimum_quantity')).select_related('unit')
        if not low_products.exists():
            self.stdout.write(self.style.SUCCESS('Không có sản phẩm dưới ngưỡng.'))
            return

        # Xây dựng danh sách recipients từ template.default_recipients
        recipients = []
        if template.default_recipients:
            recipients = [e.strip() for e in template.default_recipients.split(',') if e.strip()]

        cc_list = []
        if template.default_cc:
            cc_list = [e.strip() for e in template.default_cc.split(',') if e.strip()]

        if not recipients and not force:
            self.stdout.write(self.style.ERROR('Không có người nhận mặc định trong mẫu. Sử dụng --force để gửi test.'))
            return

        # Chuẩn bị nội dung
        products_info = []
        for p in low_products:
            products_info.append({
                'product_code': p.product_code,
                'name': p.name,
                'current_quantity': p.current_quantity,
                'minimum_quantity': p.minimum_quantity,
                'unit': p.unit.name if p.unit else ''
            })

        context = {
            'date': timezone.now(),
            'products': products_info,
            'count': low_products.count()
        }

        # Gửi email
        success, err = send_template_email(recipient_list=recipients, template_code=template_code, context_data=context, cc_list=cc_list)
        if success:
            self.stdout.write(self.style.SUCCESS(f'Đã gửi thông báo tới: {recipients}'))
        else:
            self.stdout.write(self.style.ERROR(f'Lỗi khi gửi: {err}'))
