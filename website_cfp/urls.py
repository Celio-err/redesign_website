"""
URL configuration for website_cfp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Front End
    path('', include('main_front_end.urls')),

    # Back End
    path('', include('main.urls')),

    path('mandato_cfp/', include('mandato_cfp.urls')),
    path('dddo/', include('dddo.urls')),
    path('noticias/', include('noticias.urls')),
    path('documentos_publicos/', include('documentos_publicos.urls')),
    path('configuracao/', include('settings.urls')),
    path('contacto/', include('contacto.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)