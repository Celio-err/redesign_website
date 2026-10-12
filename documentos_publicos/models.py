# Create your models here.
from django.db import models
import uuid


class TipoDocumentosPublicos(models.Model):
    id_tipo_documentos_publicos = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    tipo_documentos_publicos = models.CharField(max_length=255)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
                db_table = 'publico_tipo_documentos' 
    def __str__(self):
        return self.tipo_documentos_publicos

class DocumentosPublicos(models.Model):
    id_documentos_publicos = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    id_tipo_documentos_publicos = models.ForeignKey(
        TipoDocumentosPublicos,
        on_delete=models.CASCADE
    )
    nome_documentos_publicos = models.CharField(max_length=255)
    documentos_publicos = models.BinaryField(blank=True, null=True)
    nome_ficheiro_original = models.CharField(max_length=255, blank=True, null=True)
    data_publicacao = models.DateField(blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    
    class Meta:
                db_table = 'publico_documentos' 

    def __str__(self):
        return self.nome_documentos_publicos