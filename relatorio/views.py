from django.shortcuts import render
from django.db.models import Count
from main_front_end.models import NoticiasView
# Create your views here.

def relatorio_noticias(request):
    # 1. Total keseluruhan berita
    total_noticias = NoticiasView.objects.count()
    
    # 2. Total keseluruhan views dari semua berita
    from django.db.models import Sum
    total_views = NoticiasView.objects.aggregate(Sum('visualizacoes'))['visualizacoes__sum'] or 0
    
    # 3. Top 5 Berita Terpopuler (Most Viewed)
    most_viewed = NoticiasView.objects.all().order_by('-visualizacoes')[:5]
    
    context = {
        'total_noticias': total_noticias,
        'total_views': total_views,
        'most_viewed': most_viewed,
        'active_menu': 'relatorio_noticias',
    }
    return render(request, 'relatorio_noticia.html', context)