from django.urls import path
from . import views

urlpatterns = [
    path('relatorio_noticias/', views.relatorio_noticias, name='relatorio_noticias'),
]