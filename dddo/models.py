from django.db import models
import uuid


class TipoDDDO(models.Model):
    id_tipo_dddo = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    tipo_dddo = models.CharField(max_length=255)
    class Meta:
        db_table = 'documentos_tipo_dddo' 

    def __str__(self):
        return self.tipo_dddo

class DDDO(models.Model):
    id_dddo = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    id_tipo_dddo = models.ForeignKey(
        TipoDDDO,
        on_delete=models.CASCADE
    )
    nome_dddo = models.CharField(max_length=255)
    documentos_dddo = models.BinaryField(blank=True, null=True)
    nome_dddo_original = models.CharField(max_length=255, blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    class Meta:
            db_table = 'documentos_dddo' 
    def __str__(self):
        return self.nome_dddo