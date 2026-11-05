from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from coperation.models import Cooperacao
from istoria_cfp.models import IstoriaCFP
from mandato_cfp.models import Mandato, TipoMandato
from noticias.models import Noticias, TipoNoticias
from dddo.models import DDDO, TipoDDDO
from documentos_publicos.models import DocumentosPublicos
from django.http import HttpResponse, Http404
from .decorators import logout_required
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Case, When, Value, BooleanField
import mimetypes
from urllib.parse import quote
from django.db.models import Q
from django.urls import reverse
from django_ratelimit.decorators import ratelimit
from .forms import CommentForm
from django.db.models import F
from django.utils.html import strip_tags
import time


# ==========================================
# HOME PAGE
# ==========================================
@logout_required(redirect_to='index')
def index(request):
    mandatos = Mandato.objects.all().select_related(
        "id_tipo_mandato",
        "id_funcao_mandato"  
    )

    all_parceiros = Cooperacao.objects.all().order_by('nome_parceiro')
    
    # Ambil data berita terbaru dari model fisik Noticias
    noticias_recentes = Noticias.objects.all().order_by('-data_publicacao')[:9]
    
    for n in noticias_recentes:
        capa_url = None
        if hasattr(n, 'imagem_capa') and n.imagem_capa:
            try:
                capa_url = n.imagem_capa.url
            except Exception:
                capa_url = f"/media/{n.imagem_capa}"
        n.capa_url = capa_url
        
    return render(request, 'home.html', {
        'mandatos': mandatos,
        'noticias_recentes': noticias_recentes,
        'all_parceiros': all_parceiros,
        "active_menu": "home"
    })


# ==========================================
# ABOUT / ISTORIA & MANDATOS
# ==========================================
@logout_required(redirect_to='index')
def istoria_cfp(request):
    istoria = IstoriaCFP.objects.first()

    return render(request, 'istoria_cfp.html', {
        'istoria': istoria,
        'active_menu': 'about'
    })

def lista_mandatos(request):
    return render(request, "lista_mandato.html", {
        "active_menu": "about",
    })

@logout_required(redirect_to='index')
def mandato_list_by_tipo(request, pk):
    tipo_selecionado = get_object_or_404(TipoMandato, pk=pk)
    mandatos = (
        Mandato.objects
        .filter(id_tipo_mandato_id=pk)
        .select_related("id_tipo_mandato", "id_funcao_mandato")
        .order_by("id_funcao_mandato", "nome_pessoa")
    )
    return render(request, "mandato_list.html", {
        "mandatos": mandatos,
        "tipo_selecionado": tipo_selecionado,
    })

@logout_required(redirect_to='index')
def detallu_mandatu(request, pk):
    mandato = get_object_or_404(
        Mandato.objects.select_related("id_tipo_mandato", "id_funcao_mandato"),
        pk=pk,
    )
    mandato.funcao_mandato = str(mandato.id_funcao_mandato) if mandato.id_funcao_mandato_id else ""
    mandato.tipo_mandato = str(mandato.id_tipo_mandato) if mandato.id_tipo_mandato_id else ""

    return render(request, "detail_mandatu.html", {
        "m": mandato,
        "active_menu": "about",
    })


# ==========================================
# NOTICIAS (BERITA) - MENGGUNAKAN MODEL FISIK
# ==========================================
TAGS_CSC_ASEAN = ['CSC', 'ASEAN']
NOTICIAS_POR_PAGINA = 10

def _processar_capa_noticia(n):
    """Helper untuk memproses URL gambar sampul berita baru."""
    capa_url = None
    if hasattr(n, 'imagem_capa') and n.imagem_capa:
        try:
            capa_url = n.imagem_capa.url
        except Exception:
            capa_url = f"/media/{n.imagem_capa}"
    n.capa_url = capa_url


@logout_required(redirect_to='index')
def noticias_publico_lista(request, pk=None):
    q = request.GET.get('q', '').strip()
    
    base = Noticias.objects.all().order_by('-data_publicacao')
    if q:
        base = base.filter(
            Q(nome_noticia__icontains=q) | 
            Q(nome_noticia_tet__icontains=q) | 
            Q(nome_noticia_en__icontains=q)
        )
    
    grupos = []
    for tag in TAGS_CSC_ASEAN:
        # Filter berdasarkan relasi tipe berita atau teks
        qs = base.filter(
            Q(id_tipo_noticia__tipo_noticia__icontains=tag) |
            Q(id_tipo_noticia__tipo_noticia_tet__icontains=tag) |
            Q(id_tipo_noticia__tipo_noticia_en__icontains=tag)
        )
        
        key = f'p_{tag.lower()}'
        page_obj = Paginator(qs, NOTICIAS_POR_PAGINA).get_page(request.GET.get(key))
        
        params = request.GET.copy()
        params.pop(key, None)
        
        grupos.append({
            'tag': tag,
            'slug': tag.lower(),
            'key': key,
            'page_obj': page_obj,
            'qs': params.urlencode(),
        })

    for g in grupos:
        for item in g['page_obj'].object_list:
            _processar_capa_noticia(item)

    return render(request, "noticias_publico_lista.html", {
        "grupos": grupos,
        "q": q,
        "active_menu": "csc",
    })
 
@logout_required(redirect_to='index')
def noticia_detalho(request, pk):
    Noticias.objects.filter(pk=pk).update(visualizacoes=F('visualizacoes') + 1)
    noticia = get_object_or_404(Noticias, pk=pk)
    
    outras_noticias = list(
        Noticias.objects
        .exclude(pk=pk)
        .order_by('-data_publicacao')[:6]
    )
    for o in outras_noticias:
        _processar_capa_noticia(o)
 
    return render(request, "noticia_detalho.html", {
        "noticia": noticia,
        "outras_noticias": outras_noticias,
        "active_menu": "noticias",
    })

@logout_required(redirect_to='index')
def todas_noticias(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    
    t_noticias = Noticias.objects.all().order_by('-data_publicacao')
    
    if q:
        t_noticias = t_noticias.filter(
            Q(nome_noticia__icontains=q) | 
            Q(nome_noticia_tet__icontains=q) | 
            Q(nome_noticia_en__icontains=q) |
            Q(descricao__icontains=q) |
            Q(descricao_tet__icontains=q)
        )
        
    if tipo:
        t_noticias = t_noticias.filter(
            Q(id_tipo_noticia__tipo_noticia=tipo) |
            Q(id_tipo_noticia__tipo_noticia_tet=tipo) |
            Q(id_tipo_noticia__tipo_noticia_en=tipo)
        )

    for n in t_noticias:
        _processar_capa_noticia(n)

    # Ambil daftar jenis berita untuk dropdown filter
    tipos = TipoNoticias.objects.values_list('tipo_noticia', flat=True).distinct().order_by('tipo_noticia')
    
    paginator = Paginator(t_noticias, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'todas_noticias.html', {
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
        'tipos': tipos,
        'qs': params.urlencode(),
        "active_menu": "noticias",
    })


# ==========================================
# DDDO & LEGISLATION
# ==========================================
DDDO_POR_PAGINA = 10
def _dddo_context(request, qs):
    q = request.GET.get('q', '').strip()
    qs = (
        qs.defer('documentos_dddo')
          .annotate(
              tem_ficheiro=Case(
                  When(documentos_dddo__isnull=False, then=Value(True)),
                  default=Value(False),
                  output_field=BooleanField(),
              )
          )
          .order_by('nome_dddo')
    )
    if q:
        qs = qs.filter(nome_dddo__icontains=q)

    page_obj = Paginator(qs, DDDO_POR_PAGINA).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)
    return {
        'page_obj': page_obj,
        'q': q,
        'qs': params.urlencode(),
        'active_menu': 'legislation',
    }

@logout_required(redirect_to='index')
def dddo_publico_list(request):
    qs = DDDO.objects.select_related('id_tipo_dddo')
    return render(request, "dddo_publico_list.html", _dddo_context(request, qs))

@logout_required(redirect_to='index')
def dddo_list_by_tipo(request, pk):
    tipo_selecionado = get_object_or_404(TipoDDDO, pk=pk)
    qs = DDDO.objects.filter(id_tipo_dddo_id=pk).select_related('id_tipo_dddo')

    ctx = _dddo_context(request, qs)
    ctx['tipo_selecionado'] = tipo_selecionado
    return render(request, "dddo_publico_list.html", ctx)


# ==========================================
# FILE SERVING / DOWNLOADS
# ==========================================
def _servir_ficheiro(conteudo, nome, forcar_download=False):
    if isinstance(conteudo, memoryview):
        conteudo = bytes(conteudo)

    content_type = mimetypes.guess_type(nome)[0]
    if not content_type and conteudo[:4] == b'%PDF':
        content_type = 'application/pdf'
    content_type = content_type or 'application/octet-stream'

    bele_haree = content_type == 'application/pdf' or content_type.startswith('image/')
    disposicao = 'inline' if bele_haree and not forcar_download else 'attachment'
    response = HttpResponse(conteudo, content_type=content_type)
    response['Content-Disposition'] = f"{disposicao}; filename*=UTF-8''{quote(nome)}"
    response['X-Content-Type-Options'] = 'nosniff'
    return response

@logout_required(redirect_to='index')
def documentos_dddo_review(request, pk):
    documento = get_object_or_404(DDDO, pk=pk)
    if not documento.documentos_dddo:
        raise Http404
    nome = getattr(documento, 'nome_ficheiro_original', None) or f'{documento.nome_dddo}.pdf'
    return _servir_ficheiro(documento.documentos_dddo, nome)


# ==========================================
# DOCUMENTOS PÚBLICOS
# ==========================================
ORDEM_TIPOS = [2, 1]
POR_PAGINA = 1
CAMPO_TIPO = 'id_tipo_documentos_publicos'

@logout_required(redirect_to='index')
def documentos_publicos_publico_list(request):
    q = request.GET.get('q', '').strip()
    tids = set(
        DocumentosPublicos.objects.order_by()
        .values_list(f'{CAMPO_TIPO}_id', flat=True).distinct()
    )
    TipoModel = DocumentosPublicos._meta.get_field(CAMPO_TIPO).related_model
    destinos = [(t.pk, str(t)) for t in TipoModel.objects.filter(pk__in=tids - {None})]
    if None in tids:
        destinos.append((None, _('Outros'))) 
    
    def pozisaun(item):
        tid = item[0]
        if tid in ORDEM_TIPOS:
            return (0, ORDEM_TIPOS.index(tid))
        return (1, tid if tid is not None else 10**9)
        
    base = (
        DocumentosPublicos.objects
        .defer('documentos_publicos')
        .annotate(
            tem_ficheiro=Case(
                When(documentos_publicos__isnull=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        .order_by('nome_documentos_publicos')
    )
    if q:
        base = base.filter(nome_documentos_publicos__icontains=q)
        
    grupos = []
    for tid, nome in sorted(destinos, key=pozisaun):
        if tid is None:
            qs = base.filter(**{f'{CAMPO_TIPO}__isnull': True})
        else:
            qs = base.filter(**{f'{CAMPO_TIPO}_id': tid})
            
        key = f'p{tid}'
        page_obj = Paginator(qs, POR_PAGINA).get_page(request.GET.get(key))
        params = request.GET.copy()
        params.pop(key, None)
        grupos.append({
            'id': tid,
            'nome': nome,
            'key': key,
            'page_obj': page_obj,
            'qs': params.urlencode(),
        })
        
    return render(request, "documentos_publicos_publico_list.html", {
        "grupos": grupos,
        "q": q,
        "active_menu": "documents",
    })

@logout_required(redirect_to='index')
def documentos_publicos_review(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)
    response = HttpResponse(documento.documentos_publicos, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{documento.nome_ficheiro_original}"'
    return response


# ==========================================
# COOPERAÇÃO / PARTNER
# ==========================================
def public_cooperacao_directory(request):
    parceiros = Cooperacao.objects.all().order_by('nome_parceiro')
    return render(request, 'coperation_public_list.html', {
        'parceiros': parceiros,
        'active_menu': 'public_cooperacao_directory',
    })

def public_cooperacao_detail(request, slug):
    parceiro = get_object_or_404(Cooperacao, slug=slug)
    
    # Ambil berita yang berelasi dengan partner (melalui ForeignKey atau pencarian nama)
    noticias_parceiro = list(
        Noticias.objects.filter(
            Q(cooperacao=parceiro) |
            Q(id_tipo_noticia__tipo_noticia__icontains=parceiro.nome_parceiro) |
            Q(id_tipo_noticia__tipo_noticia_tet__icontains=parceiro.nome_parceiro)
        ).order_by('-data_publicacao')
    )
    
    for n in noticias_parceiro:
        _processar_capa_noticia(n)

    context = {
        'parceiro': parceiro,
        'noticias_parceiro': noticias_parceiro,
        'active_menu': 'public_cooperacao_directory',
    }
    return render(request, 'coperation_public_detail.html', context)


# ==========================================
# CONTACTO (COMMENT / INQUIRY)
# ==========================================
@logout_required(redirect_to='index')
@ratelimit(key="ip", rate="1/d", method="POST", block=True)
def contacto(request):
    done = f"{reverse('contacto')}?enviado=1#comentarios"

    if request.method == 'POST':
        if request.POST.get('website'):
            return redirect(done)

        form_time = request.session.get('form_timestamp')
        if not form_time or (time.time() - form_time < 3):
            return redirect(done)

        form = CommentForm(request.POST)
        if form.is_valid():
            if 'form_timestamp' in request.session:
                del request.session['form_timestamp']

            comment = form.save(commit=False)
            if hasattr(comment, 'mensagem'):
                comment.mensagem = strip_tags(comment.mensagem)
            if hasattr(comment, 'nome'):
                comment.nome = strip_tags(comment.nome)

            comment.save()
            return redirect(done)
    else:
        request.session['form_timestamp'] = time.time()
        form = CommentForm()

    return render(
        request,
        'contacto.html',
        {
            'form': form,
            'enviado': request.GET.get('enviado') == '1',
            'active_menu': 'contact',
        },
    )