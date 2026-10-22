from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import DocumentosPublicos, TipoDocumentosPublicos
from .forms import DocumentosPublicosForm, TipoDocumentosPublicosForm
from django.http import HttpResponse
import mimetypes


# ---------- DocumentosPublicos ----------

def documentos_publicos_list(request):
    documentos = DocumentosPublicos.objects.all().order_by('-data_publicacao')
    return render(request, 'documentos_publicos_list.html', {
        'documentos': documentos
    })


def documentos_publicos_create(request):
    if request.method == 'POST':
        form = DocumentosPublicosForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.inserido_por = request.user.username if request.user.is_authenticated else 'sistema'
            documento.inserido_em = timezone.now().strftime('%d/%m/%Y %H:%M')
            documento.save() # Menyimpan form beserta file biner melalui method save() di forms.py
            messages.success(request, 'Documento criado com sucesso.')
            return redirect('documentos_publicos_list')
    else:
        form = DocumentosPublicosForm()

    return render(request, 'documentos_publicos_form.html', {
        'form': form,
        'is_edit': False,
    })


def documentos_publicos_update(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)
    if request.method == 'POST':
        form = DocumentosPublicosForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento atualizado com sucesso.')
            return redirect('documentos_publicos_list')
    else:
        form = DocumentosPublicosForm(instance=documento)

    return render(request, 'documentos_publicos_form.html', {
        'form': form,
        'is_edit': True,
    })

def documentos_publicos_detail(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)
    return render(request, 'documentos_publicos_detail.html', {
        'documento': documento
    })

def documentos_publicos_delete(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)

    if request.method == 'POST':
        documento.delete()
        messages.success(request, 'Documento excluído com sucesso.')
        return redirect('documentos_publicos_list')

    return render(request, 'documentos_publicos_confirm_delete.html', {
        'documento': documento
    })


def documentos_publicos_review(request, pk):
    documento = get_object_or_404(DocumentosPublicos, pk=pk)
    
    content_type, _ = mimetypes.guess_type(documento.nome_ficheiro_original)
    if not content_type:
        content_type = 'application/pdf'  # Default fallback jika tidak terdeteksi
    response = HttpResponse(documento.documentos_publicos, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{documento.nome_ficheiro_original}"'
    
    return response

# ---------- TipoDocumentosPublicos ----------

def tipo_documentos_publicos_list(request):
    tipos = TipoDocumentosPublicos.objects.all().order_by('tipo_documentos_publicos')
    return render(request, 'tipo_documentos_publicos_list.html', {
        'tipos': tipos
    })


def tipo_documentos_publicos_create(request):
    if request.method == 'POST':
        form = TipoDocumentosPublicosForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            tipo.inserido_por = request.user.username if request.user.is_authenticated else 'sistema'
            tipo.inserido_em = timezone.now().strftime('%d/%m/%Y %H:%M')
            tipo.save()
            messages.success(request, 'Tipo de documento criado com sucesso.')
            return redirect('tipo_documentos_publicos_list')
    else:
        form = TipoDocumentosPublicosForm()

    return render(request, 'tipo_documentos_publicos_form.html', {
        'form': form,
        'is_edit': False,
    })


def tipo_documentos_publicos_detail(request, pk):
    tipo = get_object_or_404(TipoDocumentosPublicos, pk=pk)
    return render(request, 'tipo_documentos_publicos_detail.html', {
        'tipo': tipo
    })


def tipo_documentos_publicos_update(request, pk):
    tipo = get_object_or_404(TipoDocumentosPublicos, pk=pk)

    if request.method == 'POST':
        form = TipoDocumentosPublicosForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de documento atualizado com sucesso.')
            return redirect('tipo_documentos_publicos_list')
    else:
        form = TipoDocumentosPublicosForm(instance=tipo)

    return render(request, 'tipo_documentos_publicos_form.html', {
        'form': form,
        'is_edit': True,
    })


def tipo_documentos_publicos_delete(request, pk):
    tipo = get_object_or_404(TipoDocumentosPublicos, pk=pk)

    if request.method == 'POST':
        tipo.delete()
        messages.success(request, 'Tipo de documento excluído com sucesso.')
        return redirect('tipo_documentos_publicos_list')

    return render(request, 'tipo_documentos_publicos_confirm_delete.html', {
        'tipo': tipo
    })