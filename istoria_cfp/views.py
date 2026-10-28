from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import IstoriaCFPForm
from istoria_cfp.models import IstoriaCFP

# Create your views here.
def istoria_cfp_form(request):
    """View backend untuk menginput / mengedit data Istória CFP"""
    # Ambil data yang ada atau buat instance baru jika belum pernah ada data
    istoria = IstoriaCFP.objects.first()
    
    if request.method == 'POST':
        form = IstoriaCFPForm(request.POST, request.FILES, instance=istoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Istória da CFP atualizada com sucesso!")
            return redirect('istoria_cfp_form')
    else:
        form = IstoriaCFPForm(instance=istoria)
        
    return render(request, 'istoria_cfp_form.html', {
        'form': form,
        'istoria': istoria,
        'active_menu': 'istoria_cfp'
    })