import uuid
from django.db import models
from django.utils.translation import get_language


class TipoMandato(models.Model):
    id_tipo_mandato = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Field Bahasa (pt = default)
    tipo_mandato = models.CharField(max_length=100)           # Português
    tipo_mandato_tet = models.CharField(max_length=100, blank=True, null=True)  # Tetun
    tipo_mandato_en = models.CharField(max_length=100, blank=True, null=True)   # English

    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['ordem']

    @property
    def current_tipo(self):
        """Mengambil nama tipo_mandato sesuai bahasa aktif pengguna (dengan fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.tipo_mandato_tet:
            return self.tipo_mandato_tet
        elif lang == 'en' and self.tipo_mandato_en:
            return self.tipo_mandato_en
        return self.tipo_mandato

    def __str__(self):
        return self.current_tipo


class FuncaoMandato(models.Model):
    id_funcao_mandato = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    ) 

    # Field Bahasa (pt = default)
    funcao_mandato = models.CharField(max_length=100)           # Português
    funcao_mandato_tet = models.CharField(max_length=100, blank=True, null=True)  # Tetun
    funcao_mandato_en = models.CharField(max_length=100, blank=True, null=True)   # English

    @property
    def current_funcao(self):
        """Mengambil nama funcao_mandato sesuai bahasa aktif pengguna (dengan fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.funcao_mandato_tet:
            return self.funcao_mandato_tet
        elif lang == 'en' and self.funcao_mandato_en:
            return self.funcao_mandato_en
        return self.funcao_mandato

    def __str__(self):
        return self.current_funcao


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
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)

    # Field Bahasa (pt = default)
    descricao = models.TextField(blank=True, null=True)          # Português
    descricao_tet = models.TextField(blank=True, null=True)      # Tetun
    descricao_en = models.TextField(blank=True, null=True)       # English

    imagen = models.ImageField(
        upload_to='mandato/fotos/',
        blank=True,
        null=True
    )

    @property
    def current_descricao(self):
        """Mengambil deskripsi sesuai bahasa aktif pengguna (dengan fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.descricao_tet:
            return self.descricao_tet
        elif lang == 'en' and self.descricao_en:
            return self.descricao_en
        return self.descricao or ""

    def __str__(self):
        return self.nome_pessoa