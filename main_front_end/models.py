import uuid
from django.db import models
from django.utils.translation import get_language


class MandatoView(models.Model):
    id_identificacao = models.UUIDField(primary_key=True)
    nome_pessoa = models.CharField(max_length=255)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    
    # Field asli/default
    descricao = models.TextField(blank=True, null=True)
    funcao_mandato = models.CharField(max_length=100, blank=True, null=True)
    tipo_mandato = models.CharField(max_length=100, blank=True, null=True)
    
    imagen = models.CharField(max_length=255, blank=True, null=True)

    # ---------------------------------------------------------
    # KOLOM MULTIBAHASA UNTUK MANDATO (Sesuai database view)
    # ---------------------------------------------------------
    descricao_pt = models.TextField(blank=True, null=True)
    descricao_tet = models.TextField(blank=True, null=True)
    descricao_en = models.TextField(blank=True, null=True)

    funcao_mandato_pt = models.CharField(max_length=100, blank=True, null=True)
    funcao_mandato_tet = models.CharField(max_length=100, blank=True, null=True)
    funcao_mandato_en = models.CharField(max_length=100, blank=True, null=True)

    tipo_mandato_pt = models.CharField(max_length=100, blank=True, null=True)
    tipo_mandato_tet = models.CharField(max_length=100, blank=True, null=True)
    tipo_mandato_en = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mandato_cfp'

    def __str__(self):
        return self.nome_pessoa

    # --- PROPERTY PINTAR UNTUK MANDATO ---
    @property
    def current_descricao(self):
        lang = get_language()
        if lang == 'tet' and self.descricao_tet:
            return self.descricao_tet
        elif lang == 'en' and self.descricao_en:
            return self.descricao_en
        return self.descricao_pt or self.descricao

    @property
    def current_funcao(self):
        lang = get_language()
        if lang == 'tet' and self.funcao_mandato_tet:
            return self.funcao_mandato_tet
        elif lang == 'en' and self.funcao_mandato_en:
            return self.funcao_mandato_en
        return self.funcao_mandato_pt or self.funcao_mandato

    @property
    def current_tipo(self):
        lang = get_language()
        if lang == 'tet' and self.tipo_mandato_tet:
            return self.tipo_mandato_tet
        elif lang == 'en' and self.tipo_mandato_en:
            return self.tipo_mandato_en
        return self.tipo_mandato_pt or self.tipo_mandato