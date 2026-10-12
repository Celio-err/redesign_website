from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


def login_view(request):
    if request.user.is_authenticated:
        return redirect('noticias_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, f'Bem-vindo, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'index')
        else:
            messages.error(request, 'Username ou password incorretos.')

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sessão terminada com sucesso.')
    return redirect('home')

@login_required
def index(request):
    return render(request, 'index.html')