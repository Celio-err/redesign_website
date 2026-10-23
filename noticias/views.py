import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Noticias, TipoNoticias
from .forms import NoticiasForm, TipoNoticiasForm
from django.db.models import Max
from noticias.models import ImagemNoticia

# ---------- Noticias ----------

def noticias_list(request):
    noticias = Noticias.objects.all().order_by('-data_publicacao')
    return render(request, 'noticias_list.html', {
        'noticias': noticias
    })

 
from .forms import NoticiasForm
from .models import ImagemNoticia, Noticias
 
 
def _uuids(values):
    """Buang nilai yang bukan UUID valid agar filter tidak error."""
    out = []
    for v in values:
        try:
            out.append(uuid.UUID(v))
        except (ValueError, AttributeError):
            pass
    return out
 

def noticias_create(request, pk=None):
    """Tambah (pk=None) atau ubah notícia, termasuk banyak gambar."""
    noticia = get_object_or_404(Noticias, pk=pk) if pk else None
 
    if request.method == "POST":
        form = NoticiasForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia = form.save(commit=False)
            if not noticia.inserido_por:
                noticia.inserido_por = request.user.get_username()
            noticia.save()
 
            # 1) apagar gambar yang dicentang
            ids = _uuids(request.POST.getlist("apagar_imagens"))
            if ids:
                noticia.imagens.filter(pk__in=ids).delete()
 
            # 2) simpan gambar baru, lanjut dari urutan terakhir
            ordem = noticia.imagens.aggregate(m=Max("ordem"))["m"] or 0
            for i, f in enumerate(form.cleaned_data["imagens"], start=1):
                ImagemNoticia.objects.create(
                    id_noticia=noticia, imagem=f, ordem=ordem + i
                )
 
            return redirect("noticias_list")
    else:
        form = NoticiasForm(instance=noticia)
 
    return render(request, "noticias_forms.html", {
        "form": form,
        "noticia": noticia,
        "imagens": noticia.imagens.all() if noticia else [],
    })

def noticias_detail(request, pk):
    noticia = get_object_or_404(Noticias, pk=pk)
    return render(request, 'noticias_detail.html', {
        'noticia': noticia
    })


def noticias_update(request, pk):
    noticia = get_object_or_404(Noticias, pk=pk)

    if request.method == 'POST':
        form = NoticiasForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notícia atualizada com sucesso.')
            return redirect('noticias_list')
    else:
        form = NoticiasForm(instance=noticia)

    return render(request, 'noticias_forms.html', {
        'form': form
    })


def noticias_delete(request, pk):
    noticia = get_object_or_404(Noticias, pk=pk)

    if request.method == 'POST':
        noticia.delete()
        messages.success(request, 'Notícia excluída com sucesso.')
        return redirect('noticias_list')

    return render(request, 'noticias_confirm_delete.html', {
        'noticia': noticia
    })


# ---------- TipoNoticias ----------

def tipo_noticias_list(request):
    tipos = TipoNoticias.objects.all().order_by('tipo_noticia')
    return render(request, 'tipo_noticias_list.html', {
        'tipos': tipos
    })


def tipo_noticias_create(request):
    if request.method == 'POST':
        form = TipoNoticiasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de notícia criado com sucesso.')
            return redirect('tipo_noticias_list')
    else:
        form = TipoNoticiasForm()

    return render(request, 'tipo_noticias_forms.html', {
        'form': form
    })


def tipo_noticias_detail(request, pk):
    tipo = get_object_or_404(TipoNoticias, pk=pk)
    return render(request, 'tipo_noticias_detail.html', {
        'tipo': tipo
    })


def tipo_noticias_update(request, pk):
    tipo = get_object_or_404(TipoNoticias, pk=pk)

    if request.method == 'POST':
        form = TipoNoticiasForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de notícia atualizado com sucesso.')
            return redirect('tipo_noticias_list')
    else:
        form = TipoNoticiasForm(instance=tipo)

    return render(request, 'tipo_noticias_forms.html', {
        'form': form
    })


def tipo_noticias_delete(request, pk):
    tipo = get_object_or_404(TipoNoticias, pk=pk)

    if request.method == 'POST':
        tipo.delete()
        messages.success(request, 'Tipo de notícia excluído com sucesso.')
        return redirect('tipo_noticias_list')

    return render(request, 'tipo_noticias_confirm_delete.html', {
        'tipo': tipo
    })