from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import UserCreateWithRoleForm, UserEditForm
from settings.decorators import role_required 

# Create your views here.
def settings(request):
    utilizadores = User.objects.all().order_by('username').prefetch_related('groups')
    return render(request, "setting.html", {
        "utilizadores": utilizadores,
    })

@role_required('superadmin')
def user_form(request, pk=None):
    is_edit = pk is not None

    if is_edit:
        user_obj = get_object_or_404(User, pk=pk)
        FormClass = UserEditForm
        form_kwargs = {"instance": user_obj}
    else:
        user_obj = None
        FormClass = UserCreateWithRoleForm
        form_kwargs = {}

    if request.method == "POST":
        form = FormClass(request.POST, **form_kwargs)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Utilizador atualizado com sucesso." if is_edit else "Utilizador criado com sucesso."
            )
            return redirect("settings")
        messages.error(request, "Existem erros no formulário.")
    else:
        form = FormClass(**form_kwargs)

    return render(request, "form_user.html", {
        "form": form,
        "is_edit": is_edit,
    })

@role_required('superadmin')
def delete_user(request, pk):
    utilizadores = get_object_or_404(User, id=pk)
    utilizadores.delete()
    messages.success(request, "Sucesso de remover esta conta")
    return redirect('settings')

def perfil(request):
    if request.method == "POST":
        novo_username = request.POST.get("username", "").strip()
        novo_email = request.POST.get("email", "").strip()
        nova_senha = request.POST.get("nova_senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        erro = False

        # Validasi username
        if not novo_username:
            messages.error(request, "O nome de utilizador não pode estar vazio.")
            erro = True
        elif User.objects.filter(username=novo_username).exclude(pk=request.user.pk).exists():
            messages.error(request, "Este nome de utilizador já está em uso.")
            erro = True

        # Validasi password (opsional, cuma divalidasi kalau diisi)
        if nova_senha or confirmar_senha:
            if nova_senha != confirmar_senha:
                messages.error(request, "As palavras-passe não coincidem.")
                erro = True
            elif len(nova_senha) < 8:
                messages.error(request, "A palavra-passe deve ter no mínimo 8 caracteres.")
                erro = True

        if not erro:
            request.user.username = novo_username
            request.user.email = novo_email

            if nova_senha:
                request.user.set_password(nova_senha)

            request.user.save()

            if nova_senha:
                update_session_auth_hash(request, request.user)  # supaya tidak ter-logout

            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('perfil')

    return render(request, "perfil.html", {
        "usuario": request.user,
    })