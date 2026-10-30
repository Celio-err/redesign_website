from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/cooperacao/', views.backend_cooperacao_list, name='cooperacao_list'),
    path('admin-panel/cooperacao/novo/', views.backend_cooperacao_create, name='cooperacao_create'),
    path('admin-panel/cooperacao/editar/<uuid:pk>/', views.backend_cooperacao_update, name='cooperacao_update'),
    path('admin-panel/cooperacao/eliminar/<uuid:pk>/', views.backend_cooperacao_delete, name='cooperacao_delete'),
]