from django.urls import path
from . import views

urlpatterns = [
    path("", views.settings, name='settings'),
    path("novo/utilizador", views.user_form, name='user_form'),
    path('user/<int:pk>/editar/', views.user_form, name='form_user_edit'),
    path('user/<int:pk>/remover/', views.delete_user, name='delete_user'),
    path("perfil/", views.perfil, name='perfil'),
]