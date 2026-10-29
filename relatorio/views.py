from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
from main_front_end.models import NoticiasView

def relatorio_noticias(request):
    filter_type = request.GET.get('filter', 'all')
    
    # Ambil parameter filter kustom
    year_val = request.GET.get('ano')
    month_val = request.GET.get('mes')
    day_val = request.GET.get('dia')
    
    now = timezone.now()
    current_year = now.year
    
    target_year = int(year_val) if year_val else current_year
    queryset = NoticiasView.objects.all()
    
    # 1. Filter cepat (preset)
    if filter_type == 'semana':
        queryset = queryset.filter(data_publicacao__gte=now - timedelta(days=7))
    elif filter_type == 'mes':
        queryset = queryset.filter(data_publicacao__year=current_year, data_publicacao__month=now.month)
    elif filter_type == 'ano':
        queryset = queryset.filter(data_publicacao__year=current_year)
        
    # 2. Filter kustom lengkap (Tahun, Bulan, Tanggal)
    if year_val:
        queryset = queryset.filter(data_publicacao__year=year_val)
    if month_val:
        queryset = queryset.filter(data_publicacao__month=month_val)
    if day_val:
        queryset = queryset.filter(data_publicacao__day=day_val)

    # Metrik Kartu Ringkasan (Global)
    total_noticias = NoticiasView.objects.count()
    views_semana = NoticiasView.objects.filter(data_publicacao__gte=now - timedelta(days=7)).aggregate(Sum('visualizacoes'))['visualizacoes__sum'] or 0
    views_mes = NoticiasView.objects.filter(data_publicacao__year=current_year, data_publicacao__month=now.month).aggregate(Sum('visualizacoes'))['visualizacoes__sum'] or 0
    views_ano = NoticiasView.objects.filter(data_publicacao__year=current_year).aggregate(Sum('visualizacoes'))['visualizacoes__sum'] or 0
    
    # Data Grafik Bulanan
    monthly_views_qs = (
        NoticiasView.objects.filter(data_publicacao__year=target_year)
        .annotate(month=ExtractMonth('data_publicacao'))
        .values('month')
        .annotate(total=Sum('visualizacoes'))
        .order_by('month')
    )
    
    monthly_data = [0] * 12
    for entry in monthly_views_qs:
        m = entry['month']
        if m and 1 <= m <= 12:
            monthly_data[m - 1] = entry['total'] or 0

    most_viewed = queryset.order_by('-visualizacoes')[:50]
    
    # Ambil daftar tahun dinamis dari database
    years_queryset = (
        NoticiasView.objects.exclude(data_publicacao__isnull=True)
        .annotate(year=ExtractYear('data_publicacao'))
        .values_list('year', flat=True)
        .distinct()
        .order_by('-year')
    )
    years_range = list(years_queryset) if years_queryset else [current_year]

    context = {
        'total_noticias': total_noticias,
        'views_semana': views_semana,
        'views_mes': views_mes,
        'views_ano': views_ano,
        'most_viewed': most_viewed,
        'current_filter': filter_type,
        'year_val': year_val,
        'month_val': month_val,
        'day_val': day_val,
        'years_range': years_range,
        'target_year': target_year,
        'monthly_data': monthly_data,
        'active_menu': 'relatorio_noticias',
    }
    return render(request, 'relatorio_noticia.html', context)