from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cooperacao
from .forms import CooperacaoForm
from main_front_end.models import NoticiasView
from django.db.models import Q


# --- List Admin ---
def backend_cooperacao_list(request):
    parceiros = Cooperacao.objects.all().order_by('-data_criacao')
    for p in parceiros:
        p.noticias_count = NoticiasView.objects.filter(
            Q(tipo_noticia__icontains=p.nome_parceiro) |
            Q(tipo_noticia_tet__icontains=p.nome_parceiro) |
            Q(tipo_noticia_en__icontains=p.nome_parceiro)
        ).count()

    return render(request, 'coperation_list.html', {
        'parceiros': parceiros,
        'active_menu': 'backend_cooperacao'
    })

# --- Inserir / Tambah ---
def backend_cooperacao_create(request):
    if request.method == 'POST':
        form = CooperacaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova instituição/parceria registada com sucesso!')
            return redirect('cooperacao_list')
    else:
        form = CooperacaoForm()
    
    return render(request, 'coperation_form.html', {
        'form': form,
        'active_menu': 'backend_cooperacao',
        'is_edit': False
    })

# --- Editar / Update ---
def backend_cooperacao_update(request, pk):
    parceiro = get_object_or_404(Cooperacao, pk=pk)
    if request.method == 'POST':
        form = CooperacaoForm(request.POST, request.FILES, instance=parceiro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da parceria atualizados com sucesso!')
            return redirect('backend_cooperacao_list')
    else:
        form = CooperacaoForm(instance=parceiro)
        
    return render(request, 'coperation_form.html', {
        'form': form,
        'parceiro': parceiro,
        'active_menu': 'backend_cooperacao',
        'is_edit': True
    })

# --- Eliminar / Delete ---
def backend_cooperacao_delete(request, pk):
    parceiro = get_object_or_404(Cooperacao, pk=pk)
    if request.method == 'POST':
        parceiro.delete()
        messages.success(request, 'Parceria eliminada com sucesso!')
        return redirect('backend_cooperacao_list')
        
    return render(request, 'coperation_delete.html', {
        'object': parceiro,
        'active_menu': 'backend_cooperacao'
    })

