import uuid
from django.db import models
from django.utils.translation import get_language


class TipoDDDO(models.Model):
    id_tipo_dddo = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Field Bahasa (pt = default)
    tipo_dddo = models.CharField(max_length=255)           # Português
    tipo_dddo_tet = models.CharField(max_length=255, blank=True, null=True)  # Tetun
    tipo_dddo_en = models.CharField(max_length=255, blank=True, null=True)   # English

    class Meta:
        db_table = 'documentos_tipo_dddo' 

    @property
    def current_tipo(self):
        """Mengambil nama jenis dokumen sesuai bahasa aktif pengguna (fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.tipo_dddo_tet:
            return self.tipo_dddo_tet
        elif lang == 'en' and self.tipo_dddo_en:
            return self.tipo_dddo_en
        return self.tipo_dddo

    def __str__(self):
        return self.current_tipo


class DDDO(models.Model):
    id_dddo = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    id_tipo_dddo = models.ForeignKey(
        TipoDDDO,
        on_delete=models.CASCADE
    )
    
    # Field Bahasa (pt = default)
    nome_dddo = models.CharField(max_length=255)            # Português
    nome_dddo_tet = models.CharField(max_length=255, blank=True, null=True)   # Tetun
    nome_dddo_en = models.CharField(max_length=255, blank=True, null=True)    # English

    documentos_dddo = models.BinaryField(blank=True, null=True)
    nome_dddo_original = models.CharField(max_length=255, blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    
    # Field Deskripsi Bahasa (pt = default)
    descricao = models.TextField(blank=True, null=True)          # Português
    descricao_tet = models.TextField(blank=True, null=True)      # Tetun
    descricao_en = models.TextField(blank=True, null=True)       # English

    class Meta:
        db_table = 'documentos_dddo' 

    @property
    def current_nome(self):
        """Mengambil judul/nama dokumen sesuai bahasa aktif (fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.nome_dddo_tet:
            return self.nome_dddo_tet
        elif lang == 'en' and self.nome_dddo_en:
            return self.nome_dddo_en
        return self.nome_dddo

    @property
    def current_descricao(self):
        """Mengambil deskripsi dokumen sesuai bahasa aktif (fallback PT)."""
        lang = get_language()
        if lang == 'tet' and self.descricao_tet:
            return self.descricao_tet
        elif lang == 'en' and self.descricao_en:
            return self.descricao_en
        return self.descricao or ""

    def __str__(self):
        return self.current_nome