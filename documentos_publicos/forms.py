from django import forms
from .models import DocumentosPublicos, TipoDocumentosPublicos


class DocumentosPublicosForm(forms.ModelForm):
    ficheiro_upload = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Ficheiro'
    )

    class Meta:
        model = DocumentosPublicos
        fields = [
            'id_tipo_documentos_publicos', 'nome_documentos_publicos',
            'data_publicacao', 'descricao',
        ]
        labels = {
            'id_tipo_documentos_publicos': 'Tipo de Documento',
            'nome_documentos_publicos': 'Nome do Documento',
            'data_publicacao': 'Data de Publicação',
            'descricao': 'Descrição',
        }
        widgets = {
            'id_tipo_documentos_publicos': forms.Select(attrs={'class': 'form-control'}),
            'nome_documentos_publicos': forms.TextInput(attrs={'class': 'form-control'}),
            'data_publicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TipoDocumentosPublicosForm(forms.ModelForm):
    class Meta:
        model = TipoDocumentosPublicos
        fields = ['tipo_documentos_publicos', 'descricao']
        labels = {
            'tipo_documentos_publicos': 'Tipo de Documento',
            'descricao': 'Descrição',
        }
        widgets = {
            'tipo_documentos_publicos': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }