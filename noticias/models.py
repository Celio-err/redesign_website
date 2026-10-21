from django.db import models
import uuid


class TipoNoticias(models.Model):
    id_tipo_noticia = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    tipo_noticia = models.CharField(max_length=100) # Default / Português
    tipo_noticia_tet = models.CharField(max_length=100, blank=True, null=True)
    tipo_noticia_en = models.CharField(max_length=100, blank=True, null=True)
    
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tipo_noticia


class Noticias(models.Model):
    id_noticia = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    id_tipo_noticia = models.ForeignKey(
        TipoNoticias,
        on_delete=models.CASCADE
    )
    
    # ---------------------------------------------------------
    # 1. PORTUGUÊS (Default / Utama)
    # ---------------------------------------------------------
    nome_noticia = models.CharField(max_length=255)
    noticia = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    # ---------------------------------------------------------
    # 2. TETUN (Kolom Terjemahan)
    # ---------------------------------------------------------
    nome_noticia_tet = models.CharField(max_length=255, blank=True, null=True)
    noticia_tet = models.TextField(blank=True, null=True)
    descricao_tet = models.TextField(blank=True, null=True)

    # ---------------------------------------------------------
    # 3. ENGLISH (Kolom Terjemahan)
    # ---------------------------------------------------------
    nome_noticia_en = models.CharField(max_length=255, blank=True, null=True)
    noticia_en = models.TextField(blank=True, null=True)
    descricao_en = models.TextField(blank=True, null=True)

    # ---------------------------------------------------------
    # Metadata Umum
    # ---------------------------------------------------------
    data_publicacao = models.DateField(blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    imagen = models.ImageField(upload_to='img', blank=True, null=True)

    def __str__(self):
        return self.nome_noticia