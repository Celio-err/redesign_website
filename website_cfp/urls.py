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
from django.conf.urls.i18n import i18n_patterns
from noticias.views import custom_upload_file

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('mandato_cfp/', include('mandato_cfp.urls')),
    path('dddo/', include('dddo.urls')),
    path('documentos_publicos/', include('documentos_publicos.urls')),
    path('configuracao/', include('settings.urls')),
    path('noticias/', include('noticias.urls')),
    path('contacto/', include('contacto.urls')),
    path('istoria-cfp/', include('istoria_cfp.urls')),
    path('relatorio/', include('relatorio.urls')),
    path('cooperacao/', include('coperation.urls')),

    # === URUTAN PENTING DI SINI ===
    # Daftarkan endpoint custom upload PERSIS seperti yang dipanggil oleh CKEditor 5
    path("ckeditor5/image_upload/", custom_upload_file, name="custom_ckeditor_upload"),
    
    # Baru kemudian include urls bawaan ckeditor5 untuk komponen lainnya
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

# 2. i18n_patterns
urlpatterns += i18n_patterns(
    path('', include('main_front_end.urls')),
    prefix_default_language=True,
)

# 3. Media & Static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)