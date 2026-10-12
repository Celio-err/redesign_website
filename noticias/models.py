from django.db import models
import uuid


class TipoNoticias(models.Model):
    id_tipo_noticia = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    tipo_noticia = models.CharField(max_length=100)
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
    nome_noticia = models.CharField(max_length=255)
    noticia = models.TextField(blank=True, null=True)
    data_publicacao = models.DateField(blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    imagen = models.ImageField(upload_to='img', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_noticia