import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from coperation.models import Cooperacao


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

    # LAMA: dibiarkan sementara agar data lama tidak hilang.
    # Hapus setelah data disalin ke ImagemNoticia (lihat migrasi data).
    imagen = models.ImageField(upload_to='img', blank=True, null=True)

    def __str__(self):
        return self.nome_noticia

    @property
    def capa(self):
        """Gambar pertama sebagai sampul. Memakai cache prefetch_related."""
        imgs = list(self.imagens.all())
        return imgs[0] if imgs else None


class ImagemNoticia(models.Model):
    id_imagem = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    id_noticia = models.ForeignKey(
        Noticias,
        on_delete=models.CASCADE,
        related_name='imagens'
    )
    imagem = models.ImageField(upload_to='noticias/%Y/%m/')
    legenda = models.CharField(max_length=255, blank=True, null=True)
    ordem = models.PositiveSmallIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem', 'criado_em']

    def __str__(self):
        return f"{self.id_noticia} - {self.imagem.name}"


@receiver(post_delete, sender=ImagemNoticia)
def apagar_ficheiro_imagem(sender, instance, **kwargs):
    """Django tidak menghapus file di disk saat baris dihapus; kita lakukan di sini."""
    if instance.imagem:
        instance.imagem.delete(save=False)