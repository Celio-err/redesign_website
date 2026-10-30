# cooperation/models.py
import uuid
from django.db import models
from django.utils.text import slugify

class Cooperacao(models.Model):
    """Model utama untuk Partner/Kerjasama (Menyimpan Logo, Nama Institusi, dll)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_parceiro = models.CharField(max_length=255, verbose_name="Nome da Instituição / Parceiro (Ex: ASEAN, CSC, Local)")
    slug = models.SlugField(unique=True, blank=True, help_text="URL friendly, e.g. 'asean', 'csc', 'local'")
    
    # Logo Partner agar terlihat profesional
    logo_parceiro = models.ImageField(upload_to='cooperation/logos/', blank=True, null=True, verbose_name="Logo da Instituição")
    pais_parceiro = models.CharField(max_length=100, blank=True, null=True, verbose_name="País / Âmbito")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição da Parceria")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome_parceiro)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_parceiro

    class Meta:
        verbose_name_plural = "Cooperações e Parcerias"