from django.shortcuts import render, redirect, get_object_or_404
from istoria_cfp.models import IstoriaCFP
from mandato_cfp.models import Mandato, TipoMandato
from noticias.models import Noticias, TipoNoticias
from main_front_end.models import NoticiasView, MandatoView
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
from noticias.models import ImagemNoticia


#HOME PAGE
@logout_required(redirect_to='index')
def index(request):
    mandatos = Mandato.objects.all().select_related(
        "id_tipo_mandato",
        "id_funcao_mandato"  
    )
    noticias_recentes = Noticias.objects.prefetch_related('imagens').order_by('-data_publicacao')[:9]
    
    for n in noticias_recentes:
        n.current_title = getattr(n, 'nome_noticia', None) or getattr(n, 'titulo', '')
        tipo_raw = getattr(n, 'tipo_noticia', None) or getattr(n, 'id_tipo_noticia', None) or getattr(n, 'tipo', '')
        if hasattr(n, 'get_tipo_noticia_display'):
            n.current_tipo = n.get_tipo_noticia_display()
        else:
            n.current_tipo = str(tipo_raw) if tipo_raw else ''

        capa_url = None
        if hasattr(n, 'imagen') and n.imagen:
            try:
                capa_url = n.imagen.url
            except AttributeError:
                path = str(n.imagen)
                capa_url = path if path.startswith('/') or path.startswith('http') else f"/media/{path}"
        
        if not capa_url:
            galeria_fotos = getattr(n, 'imagens', None)
            if galeria_fotos and galeria_fotos.exists():
                foto_primeira = galeria_fotos.first()
                if hasattr(foto_primeira, 'imagem') and foto_primeira.imagem:
                    try:
                        capa_url = foto_primeira.imagem.url
                    except AttributeError:
                        path = str(foto_primeira.imagem)
                        capa_url = path if path.startswith('/') or path.startswith('http') else f"/media/{path}"
        n.capa_url = capa_url
    return render(request, 'home.html', {
        'mandatos': mandatos,
        'noticias_recentes': noticias_recentes,
        "active_menu": "home"
    })

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
def noticias(request):
    q = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    base_qs = NoticiasView.objects.order_by('-data_publicacao')
    if q:
        base_qs = base_qs.filter(nome_noticia__icontains=q)
    paginator = Paginator(base_qs, 15)
    page_obj = paginator.get_page(page_number)
    page_obj.object_list = list(page_obj.object_list)
    _anexar_capas(page_obj.object_list)

    return render(request, 'noticias_lista_publico.html', { 
        'page_obj': page_obj,
        'q': q,
        "active_menu": "noticias",  
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

TAGS_CSC_ASEAN = ['CSC', 'ASEAN']      # urutan tampil dari atas ke bawah
NOTICIAS_POR_PAGINA = 5               # 5 = satu blok bento penuh (1 besar + 4 kecil)

def _url_imagem_antiga(obj):
    """Cadangan: kolom 'imagen' lama. Di NoticiasView nilainya berupa teks path,
    jadi dibentuk seperti di template lama: '/' + path."""
    antiga = getattr(obj, 'imagen', None)
    return f'/{antiga}' if antiga else None
 
 
def _url_imagem(imagem_field):
    """URL gambar baru. Jika URL tampil salah, cukup ubah di SINI (satu tempat).
    Normalnya mengikuti MEDIA_URL di settings.py."""
    return imagem_field.url
 
 
def _anexar_capas(objetos):
    """Pasang atribut .capa_url pada setiap objek NoticiasView (1 query untuk semua)."""
    ids = {o.pk for o in objetos}
    capas = {}
    if ids:
        qs = ImagemNoticia.objects.filter(id_noticia_id__in=ids)  # sudah urut: ordem, criado_em
        for im in qs:
            capas.setdefault(im.id_noticia_id, im)                # simpan hanya yang pertama
    for o in objetos:
        capa = capas.get(o.pk)
        o.capa_url = _url_imagem(capa.imagem) if capa else _url_imagem_antiga(o)
    return objetos
 
 
def _montar_galeria(noticia):
    """Semua gambar notícia sebagai list [{'url':..., 'legenda':...}]."""
    galeria = [
        {'url': _url_imagem(im.imagem), 'legenda': im.legenda}
        for im in ImagemNoticia.objects.filter(id_noticia_id=noticia.pk)
    ]
    if not galeria:
        antiga = _url_imagem_antiga(noticia)
        if antiga:
            galeria = [{'url': antiga, 'legenda': None}]
    return galeria
 
 
# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------
@logout_required(redirect_to='index')
def noticias_publico_lista(request, pk=None):
    q = request.GET.get('q', '').strip()
    
    # Tanpa prefetch_related karena NoticiasView tidak memilikinya
    base = NoticiasView.objects.order_by('-data_publicacao')
    if q:
        base = base.filter(nome_noticia__icontains=q)
    
    grupos = []
    for tag in TAGS_CSC_ASEAN:
        qs = base.filter(tipo_noticia__icontains=tag)
        
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

    semua = []
    for g in grupos:
        g['page_obj'].object_list = list(g['page_obj'].object_list)
        semua.extend(g['page_obj'].object_list)
    _anexar_capas(semua)

    return render(request, "noticias_publico_lista.html", {
        "grupos": grupos,
        "q": q,
        "active_menu": "csc",
    })
 
@logout_required(redirect_to='index')
def noticia_detalho(request, pk):
    noticia = get_object_or_404(NoticiasView, pk=pk)
 
    outras_noticias = list(
        NoticiasView.objects
        .exclude(pk=pk)
        .order_by('-data_publicacao')[:6]
    )
    _anexar_capas(outras_noticias)
 
    return render(request, "noticia_detalho.html", {
        "noticia": noticia,
        "galeria": _montar_galeria(noticia),
        "outras_noticias": outras_noticias,
        "active_menu": "noticias",
    })
@logout_required(redirect_to='index')
def todas_noticias(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    t_noticias = NoticiasView.objects.all().order_by('-data_publicacao')
    if q:
        t_noticias = t_noticias.filter(nome_noticia__icontains=q)
    if tipo:
        t_noticias = t_noticias.filter(tipo_noticia=tipo)

    tipos = (
        NoticiasView.objects
        .exclude(tipo_noticia__isnull=True)
        .exclude(tipo_noticia='')
        .values_list('tipo_noticia', flat=True)
        .distinct()
        .order_by('tipo_noticia')
    )
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
        "active_menu": "home"
    })

DDDO_POR_PAGINA = 10
def _dddo_context(request, qs):
    """Pencarian + paginator + penanda file, dipakai kedua view DDDO."""
    q = request.GET.get('q', '').strip()
    qs = (
        qs.defer('documentos_dddo')          # jangan muat isi file ke memori
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

# ---------- Melihat file di browser (tombol "Ver") ----------
def _servir_ficheiro(conteudo, nome, forcar_download=False):
    """PDF dan gambar dibuka di browser; Word/Excel tetap diunduh."""
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

ORDEM_TIPOS = [2, 1]   # 2 = Relatórios (karuk), 1 = Publicações (los)
POR_PAGINA = 1        # dokumentu por pagina kada tipu
CAMPO_TIPO = 'id_tipo_documentos_publicos'

@logout_required(redirect_to='index')
def documentos_publicos_publico_list(request):
    q = request.GET.get('q', '').strip()
    # Tipe mana saja yang punya dokumen (tidak terpengaruh pencarian)
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
        .defer('documentos_publicos')          # jangan muat isi file (binary)
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
        key = f'p{tid}'                         # parameter halaman milik tipe ini
        page_obj = Paginator(qs, POR_PAGINA).get_page(request.GET.get(key))
        params = request.GET.copy()
        params.pop(key, None)                   # halaman tipe lain & pencarian tetap terbawa
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

@logout_required(redirect_to='index')
def documentos_publicos_download(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)
    response = HttpResponse(documento.documentos_publicos, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{documento.nome_ficheiro_original}"'
    return response

def contacto(request):
    return render(request, "contacto.html" ,{
        "active_menu": "contact",
    })

@logout_required(redirect_to='index')
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def contacto(request):
    done = f"{reverse('contact')}?enviado=1#comentarios"

    if request.method == "POST":
        # Honeypot terisi = bot: pura-pura sukses, jangan simpan
        if request.POST.get("website"):
            return redirect(done)

        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()          # disimpan ke tabel yang dibaca oleh backend
            return redirect(done)  # Post/Redirect/Get
    else:
        form = CommentForm()

    return render(request, "contacto.html", {
        "form": form,
        "enviado": request.GET.get("enviado") == "1",
        "active_menu": "contact",
    })