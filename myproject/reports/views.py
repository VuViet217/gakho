from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q, F
from django.http import HttpResponse
from datetime import datetime, timedelta
from calendar import monthrange
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import os
from django.conf import settings

from myproject.decorators import role_required
from inventory.models import Product
from .models import MonthlyInventorySnapshot, InventoryAudit, InventoryAuditItem

# Đăng ký font Arial cho tiếng Việt
arial_font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial.ttf')
arial_bold_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial_Bold.ttf')

if os.path.exists(arial_font_path):
    pdfmetrics.registerFont(TTFont('Arial', arial_font_path))
if os.path.exists(arial_bold_path):
    pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bold_path))


@login_required
def reports_dashboard(request):
    """Dashboard báo cáo tổng quan với biểu đồ"""
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Thống kê tổng quan
    total_products = Product.objects.all().count()
    low_stock_count = Product.objects.filter(
        current_quantity__lte=F('minimum_quantity')
    ).count()
    
    # Snapshot tháng hiện tại
    current_snapshot = MonthlyInventorySnapshot.objects.filter(
        year=current_year,
        month=current_month
    ).first()
    
    # Tất cả snapshots của tháng hiện tại
    snapshots = MonthlyInventorySnapshot.objects.filter(
        year=current_year,
        month=current_month
    )
    
    # Sản phẩm sắp hết (top 10)
    low_stock_products = Product.objects.filter(
        current_quantity__lte=F('minimum_quantity')
    ).select_related('category', 'unit').order_by('current_quantity')[:10]
    
    context = {
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'current_snapshot': current_snapshot,
        'snapshots': snapshots,
        'low_stock_products': low_stock_products,
        'current_month': current_month,
        'current_year': current_year,
    }
    
    return render(request, 'reports/dashboard.html', context)


@login_required
def monthly_report(request):
    """Danh sách báo cáo tháng"""
    # Lấy tất cả các tháng đã có snapshot
    snapshots = MonthlyInventorySnapshot.objects.values('year', 'month').distinct().order_by('-year', '-month')
    
    # Nhóm theo tháng
    months_data = []
    for item in snapshots:
        month_snapshots = MonthlyInventorySnapshot.objects.filter(
            year=item['year'],
            month=item['month']
        )
        
        is_closed = month_snapshots.filter(is_closed=True).exists()
        total_products = month_snapshots.count()
        
        months_data.append({
            'year': item['year'],
            'month': item['month'],
            'is_closed': is_closed,
            'total_products': total_products,
        })
    
    # Get current month for creating new reports
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    context = {
        'months_data': months_data,
        'current_month': current_month,
        'current_year': current_year,
        'title': 'Báo cáo tháng'
    }
    
    return render(request, 'reports/monthly_report_list.html', context)


@login_required
def monthly_report_detail(request, year, month):
    """Chi tiết báo cáo tháng"""
    # Lấy tất cả snapshot của tháng này
    snapshots = MonthlyInventorySnapshot.objects.filter(
        year=year,
        month=month
    ).select_related('product__category', 'product__unit', 'product__column__row__warehouse')
    
    # Nếu chưa có snapshot, tạo mới
    if not snapshots.exists():
        create_monthly_snapshots(year, month)
        snapshots = MonthlyInventorySnapshot.objects.filter(year=year, month=month)
    
    # Thống kê
    total_opening = sum(s.opening_stock for s in snapshots)
    total_closing = sum(s.closing_stock for s in snapshots)
    total_received = sum(s.total_received for s in snapshots)
    total_issued = sum(s.total_issued for s in snapshots)
    
    is_closed = snapshots.filter(is_closed=True).exists()
    
    # Filter
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    if search:
        snapshots = snapshots.filter(
            Q(product__name__icontains=search) |
            Q(product__product_code__icontains=search)
        )
    
    if category:
        snapshots = snapshots.filter(product__category__id=category)
    
    # Categories cho filter
    from inventory.models import Category
    categories = Category.objects.all()
    
    context = {
        'year': year,
        'month': month,
        'snapshots': snapshots,
        'total_opening': total_opening,
        'total_closing': total_closing,
        'total_received': total_received,
        'total_issued': total_issued,
        'is_closed': is_closed,
        'categories': categories,
        'search': search,
        'selected_category': category,
    }
    
    return render(request, 'reports/monthly_report_detail.html', context)


def create_monthly_snapshots(year, month):
    """Tạo snapshot cho tất cả sản phẩm trong tháng"""
    products = Product.objects.all()
    
    for product in products:
        snapshot, created = MonthlyInventorySnapshot.objects.get_or_create(
            product=product,
            year=year,
            month=month,
            defaults={
                'opening_stock': product.current_quantity,
                'closing_stock': product.current_quantity,
            }
        )


@login_required
@role_required(['sm', 'admin'])
def close_month(request, year, month):
    """Chốt số liệu cuối tháng"""
    if request.method == 'POST':
        snapshots = MonthlyInventorySnapshot.objects.filter(year=year, month=month)
        
        for snapshot in snapshots:
            snapshot.close_month()
        
        messages.success(request, f'Đã chốt số liệu tháng {month}/{year}')
        return redirect('reports:monthly_report_detail', year=year, month=month)
    
    return redirect('reports:monthly_report_detail', year=year, month=month)


@login_required
def low_stock_report(request):
    """Báo cáo sản phẩm sắp hết"""
    # Sản phẩm có tồn kho <= mức tối thiểu
    products = Product.objects.filter(
        current_quantity__lte=F('minimum_quantity')
    ).select_related('category', 'column__row__warehouse', 'unit').order_by('current_quantity')
    
    # Filter
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')  # 'critical', 'warning'
    
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(product_code__icontains=search)
        )
    
    if category:
        products = products.filter(category__id=category)
    
    if status == 'critical':
        products = products.filter(current_quantity=0)
    elif status == 'warning':
        products = products.exclude(current_quantity=0)
    
    from inventory.models import Category
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search': search,
        'selected_category': category,
        'selected_status': status,
    }
    
    return render(request, 'reports/low_stock_report.html', context)


# Tiếp tục với PDF và audit views...
@login_required
def monthly_report_pdf(request, year, month):
    """Xuất PDF báo cáo tháng"""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from io import BytesIO
    import os
    from django.conf import settings
    
    # Đăng ký font Arial cho tiếng Việt
    arial_font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial.ttf')
    arial_bold_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial_Bold.ttf')
    
    if os.path.exists(arial_font_path):
        pdfmetrics.registerFont(TTFont('Arial', arial_font_path))
    if os.path.exists(arial_bold_path):
        pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bold_path))
    
    # Lấy dữ liệu báo cáo
    snapshots = MonthlyInventorySnapshot.objects.filter(
        year=year,
        month=month
    ).select_related('product__category', 'product__unit').order_by('product__product_code')
    
    if not snapshots.exists():
        return HttpResponse("Chưa có dữ liệu báo cáo cho tháng này", status=404)
    
    # Tính tổng
    total_opening = sum(s.opening_stock for s in snapshots)
    total_closing = sum(s.closing_stock for s in snapshots)
    total_received = sum(s.total_received for s in snapshots)
    total_issued = sum(s.total_issued for s in snapshots)
    
    # Tạo PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=15*mm, bottomMargin=15*mm)
    
    # Container cho các elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='Arial-Bold' if os.path.exists(arial_bold_path) else 'Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=5*mm,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName='Arial' if os.path.exists(arial_font_path) else 'Helvetica',
        fontSize=11,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=8*mm,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph(f"BÁO CÁO TỒN KHO THÁNG {month}/{year}", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"OVNC Inventory - Ngày xuất: {timezone.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style)
    elements.append(subtitle)
    
    # Thông tin tổng quan
    summary_data = [
        ['Tồn đầu tháng', 'Nhập trong tháng', 'Xuất trong tháng', 'Tồn cuối tháng'],
        [f'{total_opening:,}', f'{total_received:,}', f'{total_issued:,}', f'{total_closing:,}']
    ]
    
    summary_table = Table(summary_data, colWidths=[60*mm, 60*mm, 60*mm, 60*mm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6B8DD6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold' if os.path.exists(arial_bold_path) else 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Arial' if os.path.exists(arial_font_path) else 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8f9fa')),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 10*mm))
    
    # Chi tiết sản phẩm
    data = [['STT', 'Mã SP', 'Tên sản phẩm', 'Danh mục', 'ĐVT', 'Tồn đầu', 'Nhập', 'Xuất', 'Tồn cuối']]
    
    for idx, snapshot in enumerate(snapshots, 1):
        data.append([
            str(idx),
            snapshot.product.product_code[:15],
            snapshot.product.name[:30] + '...' if len(snapshot.product.name) > 30 else snapshot.product.name,
            snapshot.product.category.name[:15] if snapshot.product.category else '-',
            snapshot.product.unit.name[:10] if snapshot.product.unit else '-',
            f'{snapshot.opening_stock:,}',
            f'{snapshot.total_received:,}',
            f'{snapshot.total_issued:,}',
            f'{snapshot.closing_stock:,}',
        ])
    
    # Tạo bảng
    col_widths = [12*mm, 25*mm, 60*mm, 30*mm, 20*mm, 22*mm, 22*mm, 22*mm, 22*mm]
    table = Table(data, colWidths=col_widths)
    
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6B8DD6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold' if os.path.exists(arial_bold_path) else 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'Arial' if os.path.exists(arial_font_path) else 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # STT
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Mã SP
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # Tên SP
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),    # Danh mục
        ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # ĐVT
        ('ALIGN', (5, 1), (-1, -1), 'RIGHT'),  # Số lượng
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    
    # Trả về response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bao_cao_thang_{month}_{year}.pdf"'
    
    return response


@login_required
def low_stock_report_pdf(request):
    """Xuất PDF báo cáo sắp hết"""
    # Placeholder for now
    return HttpResponse("PDF export functionality coming soon")


@login_required
def audit_list(request):
    """Danh sách kiểm kê"""
    # Placeholder for now
    return render(request, 'reports/audit_list.html', {
        'title': 'Danh sách kiểm kê'
    })


@login_required
def audit_create(request):
    """Tạo phiếu kiểm kê"""
    # Placeholder for now
    return render(request, 'reports/audit_create.html', {
        'title': 'Tạo phiếu kiểm kê mới'
    })


@login_required
def audit_detail(request, audit_id):
    """Chi tiết kiểm kê"""
    # Placeholder for now
    return HttpResponse("Audit detail page coming soon")


@login_required
def audit_edit(request, audit_id):
    """Sửa kiểm kê"""
    # Placeholder for now
    return HttpResponse("Audit edit page coming soon")


@login_required
def audit_pdf(request, audit_id):
    """PDF kiểm kê"""
    # Placeholder for now
    return HttpResponse("PDF export functionality coming soon")


@login_required
@role_required(['sm', 'admin'])
def audit_complete(request, audit_id):
    """Hoàn thành kiểm kê"""
    # Placeholder for now
    return HttpResponse("Audit completion functionality coming soon")
