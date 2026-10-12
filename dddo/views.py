from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from .models import DDDO, TipoDDDO
from .forms import DDDOForm, TipoDDDOForm


# ---------- DDDO ----------

def documentos_dddo_list(request):
    documentos = DDDO.objects.all().select_related('id_tipo_dddo')
    return render(request, 'documentos_dddo_list.html', {
        'documentos': documentos
    })


def documentos_dddo_create(request):
    if request.method == 'POST':
        form = DDDOForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            ficheiro = form.cleaned_data.get('ficheiro_upload')
            if ficheiro:
                documento.documentos_dddo = ficheiro.read()
                documento.nome_dddo_original = ficheiro.name
            documento.inserido_por = request.user.username if request.user.is_authenticated else 'sistema'
            documento.inserido_em = timezone.now().strftime('%d/%m/%Y %H:%M')
            documento.save()
            messages.success(request, 'DDDO criado com sucesso.')
            return redirect('documentos_dddo_list')
    else:
        form = DDDOForm()

    return render(request, 'documentos_dddo_form.html', {
        'form': form,
        'is_edit': False,
    })


def documentos_dddo_detail(request, pk):
    documento = get_object_or_404(DDDO, pk=pk)
    return render(request, 'documentos_dddo_detail.html', {
        'documento': documento
    })


def documentos_dddo_update(request, pk):
    documento = get_object_or_404(DDDO, pk=pk)

    if request.method == 'POST':
        form = DDDOForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            documento_atualizado = form.save(commit=False)
            ficheiro = form.cleaned_data.get('ficheiro_upload')
            if ficheiro:
                documento_atualizado.documentos_dddo = ficheiro.read()
                documento_atualizado.nome_dddo_original = ficheiro.name
            documento_atualizado.save()
            messages.success(request, 'DDDO atualizado com sucesso.')
            return redirect('documentos_dddo_list')
    else:
        form = DDDOForm(instance=documento)

    return render(request, 'documentos_dddo_form.html', {
        'form': form,
        'is_edit': True,
    })


def documentos_dddo_delete(request, pk):
    documento = get_object_or_404(DDDO, pk=pk)

    if request.method == 'POST':
        documento.delete()
        messages.success(request, 'DDDO excluído com sucesso.')
        return redirect('documentos_dddo_list')

    return render(request, 'documentos_dddo_delete.html', {
        'documento': documento
    })


def documentos_dddo_download(request, pk):
    documento = get_object_or_404(DDDO, pk=pk)
    response = HttpResponse(documento.documentos_dddo, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{documento.nome_dddo_original}"'
    return response


# ---------- TipoDDDO ----------

def tipo_dddo_list(request):
    tipos = TipoDDDO.objects.all().order_by('tipo_dddo')
    return render(request, 'tipo_dddo_list.html', {
        'tipos': tipos
    })


def tipo_dddo_create(request):
    if request.method == 'POST':
        form = TipoDDDOForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de DDDO criado com sucesso.')
            return redirect('tipo_dddo_list')
    else:
        form = TipoDDDOForm()

    return render(request, 'tipo_dddo_form.html', {
        'form': form,
        'is_edit': False,
    })


def tipo_dddo_detail(request, pk):
    tipo = get_object_or_404(TipoDDDO, pk=pk)
    return render(request, 'tipo_dddo_detail.html', {
        'tipo': tipo
    })


def tipo_dddo_update(request, pk):
    tipo = get_object_or_404(TipoDDDO, pk=pk)

    if request.method == 'POST':
        form = TipoDDDOForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de DDDO atualizado com sucesso.')
            return redirect('tipo_dddo_list')
    else:
        form = TipoDDDOForm(instance=tipo)

    return render(request, 'tipo_dddo_form.html', {
        'form': form,
        'is_edit': True,
    })


def tipo_dddo_delete(request, pk):
    tipo = get_object_or_404(TipoDDDO, pk=pk)

    if request.method == 'POST':
        tipo.delete()
        messages.success(request, 'Tipo de DDDO excluído com sucesso.')
        return redirect('tipo_dddo_list')

    return render(request, 'tipo_dddo_delete.html', {
        'tipo': tipo
    })