from django.db import models
import uuid


class TipoMandato(models.Model):
    id_tipo_mandato = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    tipo_mandato = models.CharField(max_length=100)

    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.tipo_mandato
    
class FuncaoMandato(models.Model):
    id_funcao_mandato = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    ) 
    funcao_mandato = models.CharField(max_length=100)

    def __str__(self):
        return self.funcao_mandato

class Mandato(models.Model):
    id_identificacao = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nome_pessoa = models.CharField(max_length=255)
    id_tipo_mandato = models.ForeignKey(
        TipoMandato,
        on_delete=models.CASCADE
    )
    id_funcao_mandato = models.ForeignKey(
        FuncaoMandato,
        on_delete=models.CASCADE
    )
    data_inicio = models.DateField(blank=True, null=True)   # ← tambahan
    data_fim = models.DateField(blank=True, null=True)      # ← tambahan
    descricao = models.TextField()
    imagen = models.ImageField(                             # ← tambahan
        upload_to='mandato/fotos/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome_pessoa
    