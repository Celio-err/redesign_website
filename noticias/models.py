import uuid
import os
from django.db import models
from coperation.models import Cooperacao
from django.utils.translation import get_language


class TipoNoticias(models.Model):
    id_tipo_noticia = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    is_cooperacao = models.BooleanField(
        default=False, 
        verbose_name="É uma categoria de Cooperação? (Ex: ASEAN, CSC, Local)"
    )
    tipo_noticia = models.CharField(max_length=100)  # Default / Português
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
    cooperacao = models.ForeignKey(
        Cooperacao, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='noticias',
        verbose_name="Parceria / Cooperação Relacionada"
    )

    # 1. PORTUGUÊS (Default / Utama)
    nome_noticia = models.CharField(max_length=255)
    noticia = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    # 2. TETUN
    nome_noticia_tet = models.CharField(max_length=255, blank=True, null=True)
    noticia_tet = models.TextField(blank=True, null=True)
    descricao_tet = models.TextField(blank=True, null=True)

    # 3. ENGLISH
    nome_noticia_en = models.CharField(max_length=255, blank=True, null=True)
    noticia_en = models.TextField(blank=True, null=True)
    descricao_en = models.TextField(blank=True, null=True)

    # Metadata Umum
    data_publicacao = models.DateField(blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    visualizacoes = models.PositiveIntegerField(default=0, blank=True, null=True)

    imagem_capa = models.ImageField(upload_to='noticias/capas/%Y/%m/', blank=True, null=True, verbose_name="Imagem de Capa")
    def save(self, *args, **kwargs):
        # Jika instance sudah ada di database (artinya sedang proses update/edit)
        if self.pk:
            try:
                old_instance = Noticias.objects.get(pk=self.pk)
                # Cek apakah user mengunggah gambar baru dan gambar lama itu ada
                if old_instance.imagem_capa and old_instance.imagem_capa != self.imagem_capa:
                    # Hapus file gambar lama dari storage/disk
                    if os.path.isfile(old_instance.imagem_capa.path):
                        os.remove(old_instance.imagem_capa.path)
            except Noticias.DoesNotExist:
                pass
                
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nome_noticia

    @property
    def current_title(self):
        lang = get_language()
        if lang == 'tet' and self.nome_noticia_tet:
            return self.nome_noticia_tet
        elif lang == 'en' and self.nome_noticia_en:
            return self.nome_noticia_en
        return self.nome_noticia

    @property
    def current_content(self):
        lang = get_language()
        if lang == 'tet' and self.noticia_tet:
            return self.noticia_tet
        elif lang == 'en' and self.noticia_en:
            return self.noticia_en
        return self.noticia

    @property
    def current_descricao(self):
        lang = get_language()
        if lang == 'tet' and self.descricao_tet:
            return self.descricao_tet
        elif lang == 'en' and self.descricao_en:
            return self.descricao_en
        return self.descricao

    @property
    def current_tipo(self):
        if not self.id_tipo_noticia:
            return ""
        
        lang = get_language()
        if lang == 'tet' and self.id_tipo_noticia.tipo_noticia_tet:
            return self.id_tipo_noticia.tipo_noticia_tet
        elif lang == 'en' and self.id_tipo_noticia.tipo_noticia_en:
            return self.id_tipo_noticia.tipo_noticia_en
        return self.id_tipo_noticia.tipo_noticia