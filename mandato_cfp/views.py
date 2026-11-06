from django.shortcuts import render, redirect, get_object_or_404
from .models import Mandato, TipoMandato
from .forms import MandatoForm, TipoMandatoForm
from .models import FuncaoMandato
from .forms import FuncaoMandatoForm
from django.contrib.auth.decorators import login_required


# List
@login_required
def mandato_list(request):
    mandatos = Mandato.objects.select_related(
        "id_tipo_mandato",
        "id_funcao_mandato"
    )
    return render(request, "list.html", {
        "mandatos": mandatos
    })


# Create
@login_required
def mandato_create(request):
    if request.method == "POST":
        form = MandatoForm(request.POST, request.FILES)  # ← tambah request.FILES

        if form.is_valid():
            form.save()
            return redirect("mandato_list")
    else:
        form = MandatoForm()

    return render(request, "forms.html", {
        "form": form,
        "is_edit": False,  # ← tambah is_edit
    })


# Update
@login_required
def mandato_update(request, pk):
    mandato = get_object_or_404(Mandato, pk=pk)

    if request.method == "POST":
        form = MandatoForm(request.POST, request.FILES, instance=mandato)  # ← tambah request.FILES

        if form.is_valid():
            form.save()
            return redirect("mandato_list")
    else:
        form = MandatoForm(instance=mandato)

    return render(request, "forms.html", {
        "form": form,
        "is_edit": True,  # ← tambah is_edit
    })


# Delete
@login_required
def mandato_delete(request, pk):
    mandato = get_object_or_404(Mandato, pk=pk)

    if request.method == "POST":
        mandato.delete()
        return redirect("mandato_list")

    return render(request, "delete.html", {
        "mandato": mandato
    })


# Detail
@login_required
def mandato_detail(request, pk):
    mandato = get_object_or_404(
        Mandato.objects.select_related(
            "id_tipo_mandato",
            "id_funcao_mandato"
        ),
        pk=pk
    )
    return render(request, "detail.html", {
        "mandato": mandato
    })


# ---------- TipoMandato ----------
@login_required
def tipo_mandato_list(request):
    tipos = TipoMandato.objects.all().order_by('tipo_mandato')
    return render(request, "tipo_mandato_list.html", {
        "tipos": tipos
    })

@login_required
def tipo_mandato_create(request):
    if request.method == "POST":
        form = TipoMandatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tipo_mandato_list")
    else:
        form = TipoMandatoForm()

    return render(request, "tipo_mandato_form.html", {
        "form": form
    })

@login_required
def tipo_mandato_detail(request, pk):
    tipo = get_object_or_404(TipoMandato, pk=pk)
    return render(request, "tipo_mandato_detail.html", {
        "tipo": tipo
    })

@login_required
def tipo_mandato_update(request, pk):
    tipo = get_object_or_404(TipoMandato, pk=pk)

    if request.method == "POST":
        form = TipoMandatoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect("tipo_mandato_list")
    else:
        form = TipoMandatoForm(instance=tipo)

    return render(request, "tipo_mandato_form.html", {
        "form": form
    })

@login_required
def tipo_mandato_delete(request, pk):
    tipo = get_object_or_404(TipoMandato, pk=pk)

    if request.method == "POST":
        tipo.delete()
        return redirect("tipo_mandato_list")

    return render(request, "tipo_mandato_delete.html", {
        "tipo": tipo
    })


# ---------- FuncaoMandato ----------
@login_required
def funcao_mandato_list(request):
    funcoes = FuncaoMandato.objects.all().order_by('funcao_mandato')
    return render(request, "funcao_mandato_list.html", {
        "funcoes": funcoes
    })

@login_required
def funcao_mandato_create(request):
    if request.method == "POST":
        form = FuncaoMandatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("funcao_mandato_list")
    else:
        form = FuncaoMandatoForm()

    return render(request, "funcao_mandato_form.html", {
        "form": form,
        "is_edit": False,
    })

@login_required
def funcao_mandato_detail(request, pk):
    funcao = get_object_or_404(FuncaoMandato, pk=pk)
    return render(request, "funcao_mandato_detail.html", {
        "funcao": funcao
    })

@login_required
def funcao_mandato_update(request, pk):
    funcao = get_object_or_404(FuncaoMandato, pk=pk)

    if request.method == "POST":
        form = FuncaoMandatoForm(request.POST, instance=funcao)
        if form.is_valid():
            form.save()
            return redirect("funcao_mandato_list")
    else:
        form = FuncaoMandatoForm(instance=funcao)

    return render(request, "funcao_mandato_form.html", {
        "form": form,
        "is_edit": True,
    })

@login_required
def funcao_mandato_delete(request, pk):
    funcao = get_object_or_404(FuncaoMandato, pk=pk)

    if request.method == "POST":
        funcao.delete()
        return redirect("funcao_mandato_list")

    return render(request, "funcao_mandato_delete.html", {
        "funcao": funcao
    })