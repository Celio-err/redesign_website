from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Noticias, TipoNoticias
from .forms import NoticiasForm, TipoNoticiasForm


# ---------- Noticias ----------

def noticias_list(request):
    noticias = Noticias.objects.all().order_by('-data_publicacao')
    return render(request, 'noticias_list.html', {
        'noticias': noticias
    })


def noticias_create(request):
    if request.method == 'POST':
        form = NoticiasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notícia criada com sucesso.')
            return redirect('noticias_list')
    else:
        form = NoticiasForm()

    return render(request, 'noticias_forms.html', {
        'form': form
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