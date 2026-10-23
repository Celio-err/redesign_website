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


class NoticiasView(models.Model):
    id_noticia = models.UUIDField(primary_key=True)
    data_publicacao = models.DateField(blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    id_tipo_noticia_id = models.UUIDField(blank=True, null=True)
    
    # Field asli/default
    nome_noticia = models.CharField(max_length=255)
    noticia = models.TextField(blank=True, null=True)  # Isi berita utama
    descricao = models.TextField(blank=True, null=True)
    tipo_noticia = models.CharField(max_length=255, blank=True, null=True)

    # ---------------------------------------------------------
    # KOLOM MULTIBAHASA UNTUK NOTICIAS (Sesuai database view)
    # ---------------------------------------------------------
    nome_noticia_pt = models.CharField(max_length=255, blank=True, null=True)
    nome_noticia_tet = models.CharField(max_length=255, blank=True, null=True)
    nome_noticia_en = models.CharField(max_length=255, blank=True, null=True)

    noticia_pt = models.TextField(blank=True, null=True)
    noticia_tet = models.TextField(blank=True, null=True)
    noticia_en = models.TextField(blank=True, null=True)

    descricao_pt = models.TextField(blank=True, null=True)
    descricao_tet = models.TextField(blank=True, null=True)
    descricao_en = models.TextField(blank=True, null=True)

    tipo_noticia_pt = models.CharField(max_length=255, blank=True, null=True)
    tipo_noticia_tet = models.CharField(max_length=255, blank=True, null=True)
    tipo_noticia_en = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"website_foun"."noticias_pulico"'

    def __str__(self):
        return self.nome_noticia

    # --- PROPERTY PINTAR UNTUK NOTICIAS ---
    @property
    def current_title(self):
        lang = get_language()
        if lang == 'tet' and self.nome_noticia_tet:
            return self.nome_noticia_tet
        elif lang == 'en' and self.nome_noticia_en:
            return self.nome_noticia_en
        return self.nome_noticia_pt or self.nome_noticia

    @property
    def current_noticia(self):
        lang = get_language()
        if lang == 'tet' and self.noticia_tet:
            return self.noticia_tet
        elif lang == 'en' and self.noticia_en:
            return self.noticia_en
        return self.noticia_pt or self.noticia

    @property
    def current_descricao(self):
        lang = get_language()
        if lang == 'tet' and self.descricao_tet:
            return self.descricao_tet
        elif lang == 'en' and self.descricao_en:
            return self.descricao_en
        return self.descricao_pt or self.descricao

    @property
    def current_tipo(self):
        lang = get_language()
        if lang == 'tet' and self.tipo_noticia_tet:
            return self.tipo_noticia_tet
        elif lang == 'en' and self.tipo_noticia_en:
            return self.tipo_noticia_en
        return self.tipo_noticia_pt or self.tipo_noticia

    