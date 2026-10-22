import uuid
from django.db import models
from django.utils.translation import get_language


class TipoDocumentosPublicos(models.Model):
    id_tipo_documentos_publicos = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Field Bahasa (pt = default)
    tipo_documentos_publicos = models.CharField(max_length=255)           # Português
    tipo_documentos_publicos_tet = models.CharField(max_length=255, blank=True, null=True)  # Tetun
    tipo_documentos_publicos_en = models.CharField(max_length=255, blank=True, null=True)   # English

    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    
    # Field Deskripsi Bahasa (pt = default)
    descricao = models.TextField(blank=True, null=True)          # Português
    descricao_tet = models.TextField(blank=True, null=True)      # Tetun
    descricao_en = models.TextField(blank=True, null=True)       # English

    class Meta:
        db_table = 'publico_tipo_documentos' 

    @property
    def current_tipo(self):
        """Mengambil nama jenis dokumen publik sesuai bahasa aktif pengguna (fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.tipo_documentos_publicos_tet:
            return self.tipo_documentos_publicos_tet
        elif lang == 'en' and self.tipo_documentos_publicos_en:
            return self.tipo_documentos_publicos_en
        return self.tipo_documentos_publicos

    @property
    def current_descricao(self):
        """Mengambil deskripsi tipe dokumen sesuai bahasa aktif (fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.descricao_tet:
            return self.descricao_tet
        elif lang == 'en' and self.descricao_en:
            return self.descricao_en
        return self.descricao or ""

    def __str__(self):
        return self.current_tipo


class DocumentosPublicos(models.Model):
    id_documentos_publicos = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    id_tipo_documentos_publicos = models.ForeignKey(
        TipoDocumentosPublicos,
        on_delete=models.CASCADE
    )
    
    # Field Bahasa Judul Dokumen (pt = default)
    nome_documentos_publicos = models.CharField(max_length=255)           # Português
    nome_documentos_publicos_tet = models.CharField(max_length=255, blank=True, null=True)  # Tetun
    nome_documentos_publicos_en = models.CharField(max_length=255, blank=True, null=True)   # English

    documentos_publicos = models.BinaryField(blank=True, null=True)
    nome_ficheiro_original = models.CharField(max_length=255, blank=True, null=True)
    data_publicacao = models.DateField(blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    
    # Field Deskripsi Dokumen (pt = default)
    descricao = models.TextField(blank=True, null=True)          # Português
    descricao_tet = models.TextField(blank=True, null=True)      # Tetun
    descricao_en = models.TextField(blank=True, null=True)       # English
    
    class Meta:
        db_table = 'publico_documentos' 

    @property
    def current_nome(self):
        """Mengambil judul dokumen publik sesuai bahasa aktif (fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.nome_documentos_publicos_tet:
            return self.nome_documentos_publicos_tet
        elif lang == 'en' and self.nome_documentos_publicos_en:
            return self.nome_documentos_publicos_en
        return self.nome_documentos_publicos

    @property
    def current_descricao(self):
        """Mengambil deskripsi dokumen publik sesuai bahasa aktif (fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.descricao_tet:
            return self.descricao_tet
        elif lang == 'en' and self.descricao_en:
            return self.descricao_en
        return self.descricao or ""

    def __str__(self):
        return self.current_nome