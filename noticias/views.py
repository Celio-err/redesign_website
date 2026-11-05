import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Noticias, TipoNoticias
from .forms import NoticiasForm, TipoNoticiasForm
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.http import JsonResponse

# ---------- Noticias ----------

def noticias_list(request):
    noticias = Noticias.objects.all().order_by('-data_publicacao')
    return render(request, 'noticias_list.html', {
        'noticias': noticias
    })

def noticias_create(request, pk=None):
    """Tambah (pk=None) atau ubah notícia dengan 1 gambar capa tunggal."""
    noticia = get_object_or_404(Noticias, pk=pk) if pk else None

    if request.method == "POST":
        # Perhatikan parameter request.FILES di bawah ini:
        form = NoticiasForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia = form.save(commit=False)
            if not noticia.inserido_por:
                noticia.inserido_por = request.user.get_username() if request.user.is_authenticated else "admin"
            noticia.save() # <-- Method save() di model akan otomatis mengeksekusi penghapusan gambar lama di sini

            messages.success(request, 'Notícia guardada com sucesso.')
            return redirect("noticias_list")
    else:
        form = NoticiasForm(instance=noticia)

    return render(request, "noticias_forms.html", {
        "form": form,
        "noticia": noticia,
    })

@csrf_exempt
def custom_upload_file(request):
    if request.method == "POST" and request.FILES.get("upload"):
        upload = request.FILES["upload"]
        # Simpan file ke folder media/ckeditor5/
        file_path = default_storage.save(f"ckeditor5/{upload.name}", upload)
        file_url = default_storage.url(file_path)
        return JsonResponse({
            "url": file_url,
            "uploaded": True,
            "message": "Upload successful"
        })
    return JsonResponse({
        "uploaded": False, 
        "error": {"message": "Nenhum arquivo enviado ou método inválido."}
    }, status=400)

def noticias_detail(request, pk):
    noticia = get_object_or_404(Noticias, pk=pk)
    return render(request, 'noticias_detail.html', {
        'noticia': noticia
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