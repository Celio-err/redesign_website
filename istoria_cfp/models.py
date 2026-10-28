from django.db import models
from django.utils.translation import get_language, gettext_lazy as _

class IstoriaCFP(models.Model):
    # Português (Default)
    titulo = models.CharField(max_length=255, verbose_name=_("Título"))
    subtitulo = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Subtítulo"))
    conteudo = models.TextField(verbose_name=_("Conteúdo"))

    # Tetun
    titulo_tet = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Título (Tetun)"))
    subtitulo_tet = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Subtítulo (Tetun)"))
    conteudo_tet = models.TextField(blank=True, null=True, verbose_name=_("Conteúdo (Tetun)"))

    # English
    titulo_en = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Título (English)"))
    subtitulo_en = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Subtítulo (English)"))
    conteudo_en = models.TextField(blank=True, null=True, verbose_name=_("Conteúdo (English)"))

    data_atualizacao = models.DateTimeField(auto_now=True)

    @property
    def current_titulo(self):
        lang = get_language() or 'pt'
        if lang.startswith('tet') and self.titulo_tet:
            return self.titulo_tet
        elif lang.startswith('en') and self.titulo_en:
            return self.titulo_en
        return self.titulo

    @property
    def current_subtitulo(self):
        lang = get_language() or 'pt'
        if lang.startswith('tet') and self.subtitulo_tet:
            return self.subtitulo_tet
        elif lang.startswith('en') and self.subtitulo_en:
            return self.subtitulo_en
        return self.subtitulo

    @property
    def current_conteudo(self):
        lang = get_language() or 'pt'
        if lang.startswith('tet') and self.conteudo_tet:
            return self.conteudo_tet
        elif lang.startswith('en') and self.conteudo_en:
            return self.conteudo_en
        return self.conteudo

    def __str__(self):
        return self.titulo