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
from inventory.models import Product, Category
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
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from io import BytesIO
    import os
    from django.conf import settings
    
    # Đăng ký font tiếng Việt
    arial_font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial.ttf')
    arial_bold_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial-Bold.ttf')
    
    try:
        if os.path.exists(arial_font_path):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_font_path))
        if os.path.exists(arial_bold_path):
            pdfmetrics.registerFont(TTFont('ArialUnicode-Bold', arial_bold_path))
    except:
        pass
    
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
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(A4), 
        topMargin=10*mm, 
        bottomMargin=15*mm,
        leftMargin=10*mm,
        rightMargin=10*mm
    )
    
    # Container cho các elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='ArialUnicode-Bold',
        fontSize=16,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=3*mm,
        alignment=TA_CENTER,
        leading=20
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName='ArialUnicode',
        fontSize=11,
        textColor=colors.HexColor('#424242'),
        spaceAfter=2*mm,
        alignment=TA_CENTER,
        leading=14
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontName='ArialUnicode',
        fontSize=10,
        textColor=colors.HexColor('#212121'),
        leading=14
    )
    
    signature_style = ParagraphStyle(
        'SignatureStyle',
        parent=styles['Normal'],
        fontName='ArialUnicode',
        fontSize=10,
        textColor=colors.HexColor('#212121'),
        alignment=TA_CENTER,
        leading=14,
        spaceAfter=2*mm
    )
    
    # Header
    company_header = Paragraph("CÔNG TY TNHH OLYMPUS VIỆT NAM", title_style)
    elements.append(company_header)
    elements.append(Spacer(1, 2*mm))
    
    # Title
    title = Paragraph(f"<b>BÁO CÁO TỒN KHO THÁNG {month}/{year}</b>", title_style)
    elements.append(title)
    
    # Thông tin
    report_info = Paragraph(
        f"Ngày xuất báo cáo: <b>{timezone.now().strftime('%d/%m/%Y %H:%M')}</b>",
        subtitle_style
    )
    elements.append(report_info)
    elements.append(Spacer(1, 5*mm))
    
    # Thông tin tổng quan
    summary_data = [
        ['<b>Tồn đầu tháng</b>', '<b>Nhập trong tháng</b>', '<b>Xuất trong tháng</b>', '<b>Tồn cuối tháng</b>'],
        [f'<b>{total_opening:,}</b>', f'<b>{total_received:,}</b>', f'<b>{total_issued:,}</b>', f'<b>{total_closing:,}</b>']
    ]
    
    summary_table_data = []
    for row in summary_data:
        summary_table_data.append([Paragraph(cell, info_style) for cell in row])
    
    summary_table = Table(summary_table_data, colWidths=[65*mm, 65*mm, 65*mm, 65*mm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'ArialUnicode-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'ArialUnicode-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1565c0')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e3f2fd')),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 7*mm))
    
    # Chi tiết sản phẩm
    data = [['STT', 'Mã SP', 'Tên sản phẩm', 'Danh mục', 'ĐVT', 'Tồn đầu', 'Nhập', 'Xuất', 'Tồn cuối']]
    
    for idx, snapshot in enumerate(snapshots, 1):
        product_name = snapshot.product.name
        if len(product_name) > 35:
            product_name = product_name[:32] + '...'
        
        data.append([
            str(idx),
            snapshot.product.product_code[:15],
            product_name,
            snapshot.product.category.name[:12] if snapshot.product.category else '-',
            snapshot.product.unit.name[:8] if snapshot.product.unit else '-',
            f'{snapshot.opening_stock:,}',
            f'{snapshot.total_received:,}',
            f'{snapshot.total_issued:,}',
            f'{snapshot.closing_stock:,}',
        ])
    
    # Tạo bảng
    col_widths = [12*mm, 25*mm, 62*mm, 28*mm, 18*mm, 23*mm, 23*mm, 23*mm, 26*mm]
    table = Table(data, colWidths=col_widths)
    
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'ArialUnicode-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        
        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'ArialUnicode'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # STT
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Mã SP
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # Tên SP
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),    # Danh mục
        ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # ĐVT
        ('ALIGN', (5, 1), (-1, -1), 'RIGHT'),  # Số lượng
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 8*mm))
    
    # Phần ký nhận
    signature_data = [
        ['', 'Người lập', '', 'Kế toán', '', 'Trưởng phòng'],
        ['', '(Ký, họ tên)', '', '(Ký, họ tên)', '', '(Ký, họ tên)'],
    ]
    
    signature_table = Table(signature_data, colWidths=[15*mm, 70*mm, 15*mm, 70*mm, 15*mm, 75*mm])
    signature_table.setStyle(TableStyle([
        ('FONTNAME', (1, 0), (1, 0), 'ArialUnicode-Bold'),
        ('FONTNAME', (3, 0), (3, 0), 'ArialUnicode-Bold'),
        ('FONTNAME', (5, 0), (5, 0), 'ArialUnicode-Bold'),
        ('FONTNAME', (1, 1), (1, 1), 'ArialUnicode'),
        ('FONTNAME', (3, 1), (3, 1), 'ArialUnicode'),
        ('FONTNAME', (5, 1), (5, 1), 'ArialUnicode'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (1, 1), 'CENTER'),
        ('ALIGN', (3, 0), (3, 1), 'CENTER'),
        ('ALIGN', (5, 0), (5, 1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 35),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
    ]))
    
    elements.append(signature_table)
    
    # Build PDF
    doc.build(elements)
    
    # Trả về response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Bao_cao_ton_kho_thang_{month}_{year}.pdf"'
    
    return response


@login_required
def low_stock_report_pdf(request):
    """Xuất PDF báo cáo sắp hết"""
    # Placeholder for now
    return HttpResponse("PDF export functionality coming soon")


@login_required
def audit_list(request):
    """Danh sách kiểm kê"""
    audits = InventoryAudit.objects.all().select_related('created_by').order_by('-audit_date', '-created_at')
    
    # Filter
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    if status:
        audits = audits.filter(status=status)
    
    if search:
        audits = audits.filter(
            Q(audit_code__icontains=search) |
            Q(title__icontains=search)
        )
    
    context = {
        'title': 'Danh sách kiểm kê',
        'audits': audits,
        'selected_status': status,
        'search': search,
    }
    return render(request, 'reports/audit_list.html', context)


@login_required
def audit_create(request):
    """Tạo phiếu kiểm kê"""
    if request.method == 'POST':
        title = request.POST.get('title')
        audit_date = request.POST.get('audit_date')
        notes = request.POST.get('notes', '')
        product_ids = request.POST.getlist('products')
        
        if not title or not audit_date:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin')
            return redirect('reports:audit_create')
        
        # Tạo audit
        audit = InventoryAudit.objects.create(
            title=title,
            audit_date=audit_date,
            notes=notes,
            created_by=request.user,
            status='draft'
        )
        
        # Thêm sản phẩm vào audit
        if product_ids:
            for product_id in product_ids:
                try:
                    product = Product.objects.get(id=product_id)
                    InventoryAuditItem.objects.create(
                        audit=audit,
                        product=product,
                        system_quantity=product.current_quantity
                    )
                except Product.DoesNotExist:
                    pass
        else:
            # Nếu không chọn sản phẩm cụ thể, thêm tất cả
            products = Product.objects.all()
            for product in products:
                InventoryAuditItem.objects.create(
                    audit=audit,
                    product=product,
                    system_quantity=product.current_quantity
                )
        
        messages.success(request, f'Đã tạo phiếu kiểm kê {audit.audit_code}')
        return redirect('reports:audit_detail', audit_id=audit.id)
    
    # GET request
    products = Product.objects.all().select_related('category', 'unit').order_by('product_code')
    categories = Category.objects.all()
    
    context = {
        'title': 'Tạo phiếu kiểm kê mới',
        'products': products,
        'categories': categories,
        'today': timezone.now(),
    }
    return render(request, 'reports/audit_create.html', context)


@login_required
def audit_detail(request, audit_id):
    """Chi tiết kiểm kê"""
    audit = get_object_or_404(InventoryAudit.objects.select_related('created_by'), id=audit_id)
    items = audit.items.select_related('product__category', 'product__unit').order_by('product__product_code')
    
    # Tính thống kê
    total_items = items.count()
    checked_items = items.filter(actual_quantity__isnull=False).count()
    
    differences = []
    for item in items:
        if item.actual_quantity is not None and item.difference != 0:
            differences.append(item)
    
    context = {
        'title': f'Chi tiết kiểm kê {audit.audit_code}',
        'audit': audit,
        'items': items,
        'total_items': total_items,
        'checked_items': checked_items,
        'differences': differences,
    }
    return render(request, 'reports/audit_detail.html', context)


@login_required
def audit_edit(request, audit_id):
    """Sửa kiểm kê - Cập nhật số lượng thực tế"""
    audit = get_object_or_404(InventoryAudit, id=audit_id)
    
    if audit.status == 'completed':
        messages.error(request, 'Không thể sửa phiếu kiểm kê đã hoàn thành')
        return redirect('reports:audit_detail', audit_id=audit_id)
    
    if request.method == 'POST':
        # Cập nhật trạng thái
        audit.status = 'in_progress'
        audit.save()
        
        # Cập nhật số lượng thực tế cho từng item
        for key, value in request.POST.items():
            if key.startswith('actual_'):
                item_id = key.replace('actual_', '')
                try:
                    item = InventoryAuditItem.objects.get(id=item_id, audit=audit)
                    if value.strip():
                        item.actual_quantity = int(value)
                        notes_key = f'notes_{item_id}'
                        if notes_key in request.POST:
                            item.notes = request.POST[notes_key]
                        item.save()
                except (InventoryAuditItem.DoesNotExist, ValueError):
                    pass
        
        messages.success(request, 'Đã cập nhật thông tin kiểm kê')
        return redirect('reports:audit_detail', audit_id=audit_id)
    
    items = audit.items.select_related('product__category', 'product__unit').order_by('product__product_code')
    
    context = {
        'title': f'Sửa kiểm kê {audit.audit_code}',
        'audit': audit,
        'items': items,
    }
    return render(request, 'reports/audit_edit.html', context)


@login_required
def audit_pdf(request, audit_id):
    """PDF kiểm kê"""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from io import BytesIO
    import os
    from django.conf import settings
    
    audit = get_object_or_404(InventoryAudit.objects.select_related('created_by'), id=audit_id)
    items = audit.items.select_related('product__category', 'product__unit').order_by('product__product_code')
    
    # Đăng ký font tiếng Việt
    arial_font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial.ttf')
    arial_bold_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arial-Bold.ttf')
    
    try:
        if os.path.exists(arial_font_path):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_font_path))
        if os.path.exists(arial_bold_path):
            pdfmetrics.registerFont(TTFont('ArialUnicode-Bold', arial_bold_path))
    except:
        pass
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(A4), 
        topMargin=10*mm, 
        bottomMargin=20*mm,
        leftMargin=10*mm,
        rightMargin=10*mm
    )
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Style cho tiêu đề
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='ArialUnicode-Bold',
        fontSize=16,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=3*mm,
        alignment=TA_CENTER,
        leading=20
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName='ArialUnicode',
        fontSize=12,
        textColor=colors.HexColor('#424242'),
        spaceAfter=2*mm,
        alignment=TA_CENTER,
        leading=16
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontName='ArialUnicode',
        fontSize=10,
        textColor=colors.HexColor('#212121'),
        leading=14
    )
    
    signature_style = ParagraphStyle(
        'SignatureStyle',
        parent=styles['Normal'],
        fontName='ArialUnicode',
        fontSize=10,
        textColor=colors.HexColor('#212121'),
        alignment=TA_CENTER,
        leading=14,
        spaceAfter=2*mm
    )
    
    # Header công ty
    company_header = Paragraph("CÔNG TY TNHH OLYMPUS VIỆT NAM", title_style)
    elements.append(company_header)
    
    elements.append(Spacer(1, 2*mm))
    
    # Title chính
    title = Paragraph(f"<b>BIÊN BẢN KIỂM KÊ KHO</b>", title_style)
    elements.append(title)
    
    # Thông tin audit
    audit_info = Paragraph(
        f"Mã số: <b>{audit.audit_code}</b> | Ngày kiểm kê: <b>{audit.audit_date.strftime('%d/%m/%Y')}</b>",
        subtitle_style
    )
    elements.append(audit_info)
    
    elements.append(Spacer(1, 3*mm))
    
    # Thông tin chi tiết
    info_table_data = [
        ['Tiêu đề:', audit.title, 'Người lập:', audit.created_by.get_full_name() or audit.created_by.username],
        ['Trạng thái:', 
         'Nháp' if audit.status == 'draft' else ('Đang kiểm' if audit.status == 'in_progress' else 'Hoàn thành'),
         'Ngày tạo:', 
         audit.created_at.strftime('%d/%m/%Y %H:%M')],
    ]
    
    info_table = Table(info_table_data, colWidths=[30*mm, 90*mm, 30*mm, 90*mm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ArialUnicode'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#424242')),
        ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#424242')),
        ('FONTNAME', (0, 0), (0, -1), 'ArialUnicode-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'ArialUnicode-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 5*mm))
    
    # Bảng dữ liệu
    data = [['STT', 'Mã SP', 'Tên sản phẩm', 'Danh mục', 'ĐVT', 'SL Hệ thống', 'SL Thực tế', 'Chênh lệch', 'Ghi chú']]
    
    total_system = 0
    total_actual = 0
    
    for idx, item in enumerate(items, 1):
        actual = item.actual_quantity if item.actual_quantity is not None else None
        diff = item.difference if item.actual_quantity is not None else None
        
        total_system += item.system_quantity
        if actual is not None:
            total_actual += actual
        
        data.append([
            str(idx),
            item.product.product_code[:15],
            item.product.name[:30] + ('...' if len(item.product.name) > 30 else ''),
            item.product.category.name[:12] if item.product.category else '-',
            item.product.unit.name[:8] if item.product.unit else '-',
            str(item.system_quantity),
            str(actual) if actual is not None else '',
            str(diff) if diff is not None else '',
            (item.notes[:15] + '...' if item.notes and len(item.notes) > 15 else (item.notes or '')),
        ])
    
    # Tổng cộng
    data.append([
        '', '', '', '', 'TỔNG:',
        str(total_system),
        str(total_actual),
        str(total_actual - total_system),
        ''
    ])
    
    col_widths = [12*mm, 22*mm, 55*mm, 25*mm, 15*mm, 25*mm, 25*mm, 25*mm, 36*mm]
    table = Table(data, colWidths=col_widths)
    
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'ArialUnicode-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        # Body
        ('FONTNAME', (0, 1), (-1, -2), 'ArialUnicode'),
        ('FONTSIZE', (0, 1), (-1, -2), 8),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (5, 1), (-2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f5f5f5')]),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 4),
        ('TOPPADDING', (0, 1), (-1, -2), 4),
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e3f2fd')),
        ('FONTNAME', (0, -1), (-1, -1), 'ArialUnicode-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 9),
        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
        ('GRID', (0, -1), (-1, -1), 1, colors.HexColor('#1565c0')),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 6),
        ('TOPPADDING', (0, -1), (-1, -1), 6),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 10*mm))
    
    # Phần ký nhận
    signature_data = [
        ['', 'Người kiểm kê', '', 'Thủ kho', '', 'Trưởng phòng'],
        ['', '(Ký, họ tên)', '', '(Ký, họ tên)', '', '(Ký, họ tên)'],
    ]
    
    signature_table = Table(signature_data, colWidths=[10*mm, 70*mm, 10*mm, 70*mm, 10*mm, 70*mm])
    signature_table.setStyle(TableStyle([
        ('FONTNAME', (1, 0), (1, 0), 'ArialUnicode-Bold'),
        ('FONTNAME', (3, 0), (3, 0), 'ArialUnicode-Bold'),
        ('FONTNAME', (5, 0), (5, 0), 'ArialUnicode-Bold'),
        ('FONTNAME', (1, 1), (1, 1), 'ArialUnicode'),
        ('FONTNAME', (3, 1), (3, 1), 'ArialUnicode'),
        ('FONTNAME', (5, 1), (5, 1), 'ArialUnicode'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (1, 1), 'CENTER'),
        ('ALIGN', (3, 0), (3, 1), 'CENTER'),
        ('ALIGN', (5, 0), (5, 1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
    ]))
    
    elements.append(signature_table)
    
    # Ghi chú cuối
    if audit.notes:
        elements.append(Spacer(1, 3*mm))
        note_text = Paragraph(f"<b>Ghi chú:</b> {audit.notes}", info_style)
        elements.append(note_text)
    
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Bien_ban_kiem_ke_{audit.audit_code}.pdf"'
    
    return response


@login_required
@role_required(['sm', 'admin'])
def audit_complete(request, audit_id):
    """Hoàn thành kiểm kê"""
    audit = get_object_or_404(InventoryAudit, id=audit_id)
    
    if audit.status == 'completed':
        messages.warning(request, 'Phiếu kiểm kê đã được hoàn thành trước đó')
        return redirect('reports:audit_detail', audit_id=audit_id)
    
    if request.method == 'POST':
        audit.status = 'completed'
        audit.completed_at = timezone.now()
        audit.save()
        
        messages.success(request, f'Đã hoàn thành phiếu kiểm kê {audit.audit_code}')
        return redirect('reports:audit_detail', audit_id=audit_id)
    
    return redirect('reports:audit_detail', audit_id=audit_id)
