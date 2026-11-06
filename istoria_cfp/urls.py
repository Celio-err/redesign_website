from django.urls import path
from . import views

urlpatterns = [
    path('istoria-cfp-view', views.istoria_cfp_view, name='istoria_cfp_view' ),
    path('istoria-cfp-form/', views.istoria_cfp_form, name='istoria_cfp_form'),
]