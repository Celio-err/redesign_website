from django.urls import path
from . import views

urlpatterns = [
    path("comentarios/", views.contacto, name='contacto'),
    path("comentarios/<int:pk>/lido/", views.comment_toggle_read, name="backend_comment_toggle_read"),
    path("comentarios/<int:pk>/apagar/", views.comment_delete, name="backend_comment_delete"),
]