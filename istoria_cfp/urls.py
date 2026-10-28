from django.urls import path
from . import views

urlpatterns = [
    path('istoria-cfp/', views.istoria_cfp_form, name='istoria_cfp_form'),
]