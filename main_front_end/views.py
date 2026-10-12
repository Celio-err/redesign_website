from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from mandato_cfp.models import Mandato, TipoMandato
from noticias.models import TipoNoticias
from main_front_end.models import NoticiasView, MandatoView
from dddo.models import DDDO, TipoDDDO
from documentos_publicos.models import DocumentosPublicos
from django.http import HttpResponse
from .decorators import logout_required
from django.utils.translation import gettext as _



#HOME PAGE
@logout_required(redirect_to='index')
def index(request):
    mandatos = Mandato.objects.all().select_related(
        "id_tipo_mandato",
        "id_funcao_mandato"  
    )
    noticias_recentes = NoticiasView.objects.all().order_by('-data_publicacao')[:6]

    return render(request, 'home.html', {
        'mandatos': mandatos,
        'noticias_recentes': noticias_recentes,
    })

@logout_required(redirect_to='index')
def mandato_list_by_tipo(request, pk):
    tipo_selecionado = get_object_or_404(TipoMandato, pk=pk)
    mandatos = Mandato.objects.filter(id_tipo_mandato_id=pk).select_related(
        "id_tipo_mandato",
        "id_funcao_mandato"
    )
    return render(request, "mandato_list.html", {
        "mandatos": mandatos,
        "tipo_selecionado": tipo_selecionado,
    })

@logout_required(redirect_to='index')
def detallu_mandatu(request, pk):
    mandato = get_object_or_404(MandatoView, pk=pk)
    return render(request, "detail_mandatu.html" , {
        'm': mandato
    })

@logout_required(redirect_to='index')
def noticias_publico_lista(request, pk):
    tipo_selecionado = get_object_or_404(TipoNoticias, pk=pk)
    noticias = NoticiasView.objects.filter(id_tipo_noticia_id=pk)
    
    return render(request, "noticias_publico_lista.html", {
        "noticias": noticias,
        "tipo_selecionado": tipo_selecionado,
    })

@logout_required(redirect_to='index')
def noticia_detalho(request, pk):
    noticia = get_object_or_404(NoticiasView, pk=pk)
    
    return render(request, "noticia_detalho.html", {
        "noticia": noticia
    })

@logout_required(redirect_to='index')
def todas_noticias(request):
    t_noticias = NoticiasView.objects.all()

    return render(request, 'todas_noticias.html', {
            't_noticias': t_noticias,
        })

@logout_required(redirect_to='index')
def dddo_publico_list(request):
    documentos = DDDO.objects.all().select_related('id_tipo_dddo')

    return render(request, "dddo_publico_list.html", {
        "documentos": documentos
    })

@logout_required(redirect_to='index')
def documentos_publicos_publico_list(request):
    relatorios = DocumentosPublicos.objects.all().select_related('id_tipo_documentos_publicos')
    return render(request, "documentos_publicos_publico_list.html", {
        "relatorios": relatorios
    })

@logout_required(redirect_to='index')
def documentos_publicos_review(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)
    response = HttpResponse(documento.documentos_publicos, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{documento.nome_ficheiro_original}"'
    return response

@logout_required(redirect_to='index')
def dddo_list_by_tipo(request, pk):
    tipo_selecionado = get_object_or_404(TipoDDDO, pk=pk)
    documentos = DDDO.objects.filter(id_tipo_dddo_id=pk).select_related('id_tipo_dddo')
    return render(request, "dddo_publico_list.html", {
        "documentos": documentos,
        "tipo_selecionado": tipo_selecionado,
    })

@logout_required(redirect_to='index')
def documentos_publicos_download(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)
    response = HttpResponse(documento.documentos_publicos, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{documento.nome_ficheiro_original}"'
    return response

@logout_required(redirect_to='index')
def contacto(request):
    return render(request, "contacto.html")