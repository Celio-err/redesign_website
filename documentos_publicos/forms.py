from django import forms
from django.utils.translation import gettext_lazy as _
from .models import DocumentosPublicos, TipoDocumentosPublicos


class TipoDocumentosPublicosForm(forms.ModelForm):
    class Meta:
        model = TipoDocumentosPublicos
        fields = [
            'tipo_documentos_publicos',
            'tipo_documentos_publicos_tet',
            'tipo_documentos_publicos_en',
            'descricao',
            'descricao_tet',
            'descricao_en',
        ]
        labels = {
            'tipo_documentos_publicos': _('Tipo de Documento (Português)'),
            'tipo_documentos_publicos_tet': _('Tipo de Documento (Tetun)'),
            'tipo_documentos_publicos_en': _('Tipo de Documento (English)'),
            'descricao': _('Descrição (Português)'),
            'descricao_tet': _('Descrição (Tetun)'),
            'descricao_en': _('Descrição (English)'),
        }
        widgets = {
            'tipo_documentos_publicos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documentos_publicos_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documentos_publicos_en': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'descricao_tet': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'descricao_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class DocumentosPublicosForm(forms.ModelForm):
    # Field kustom untuk menangani upload file karena documentos_publicos adalah BinaryField
    documentos_publicos_file = forms.FileField(
        required=False,
        label=_('Ficheiro do Documento'),
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = DocumentosPublicos
        fields = [
            'id_tipo_documentos_publicos',
            'nome_documentos_publicos',
            'nome_documentos_publicos_tet',
            'nome_documentos_publicos_en',
            'data_publicacao',
            'descricao',
            'descricao_tet',
            'descricao_en',
        ]
        labels = {
            'id_tipo_documentos_publicos': _('Tipo de Documento'),
            'nome_documentos_publicos': _('Título do Documento (Português)'),
            'nome_documentos_publicos_tet': _('Título do Documento (Tetun)'),
            'nome_documentos_publicos_en': _('Título do Documento (English)'),
            'data_publicacao': _('Data de Publicação'),
            'descricao': _('Descrição (Português)'),
            'descricao_tet': _('Descrição (Tetun)'),
            'descricao_en': _('Descrição (English)'),
        }
        widgets = {
            'id_tipo_documentos_publicos': forms.Select(attrs={'class': 'form-control'}),
            'nome_documentos_publicos': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_documentos_publicos_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_documentos_publicos_en': forms.TextInput(attrs={'class': 'form-control'}),
            'data_publicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'descricao_tet': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'descricao_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('documentos_publicos_file')
        
        # Konversi file yang diupload menjadi biner untuk BinaryField
        if file:
            instance.documentos_publicos = file.read()
            instance.nome_ficheiro_original = file.name
            
        if commit:
            instance.save()
        return instance