from django import forms
from .models import Noticias, TipoNoticias


class NoticiasForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = [
            'id_tipo_noticia', 'nome_noticia', 'noticia',
            'data_publicacao', 'imagen', 'descricao',
        ]
        labels = {
            'id_tipo_noticia': 'Tipo Notícia',
            'nome_noticia': 'Título',
            'noticia': 'Notícia',
            'data_publicacao': 'Data de Publicação',
            'imagen': 'Imagem',
            'descricao': 'Descrição',
        }
        widgets = {
            'noticia': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_publicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_tipo_noticia': forms.Select(attrs={'class': 'form-control'}),
            'nome_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class TipoNoticiasForm(forms.ModelForm):
    class Meta:
        model = TipoNoticias
        fields = ['tipo_noticia', 'descricao']
        widgets = {
            'tipo_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }