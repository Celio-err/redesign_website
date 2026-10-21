# noticias/forms.py
from django import forms
from .models import NoticiasView

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = NoticiasView
        fields = [
            'imagen', 'data_publicacao',
            'nome_noticia_pt', 'nome_noticia_tet', 'nome_noticia_en',
            'descricao_pt', 'descricao_tet', 'descricao_en',
            'noticia_pt', 'noticia_tet', 'noticia_en',
        ]
        widgets = {
            'noticia_pt': forms.Textarea(attrs={'rows': 5}),
            'noticia_tet': forms.Textarea(attrs={'rows': 5}),
            'noticia_en': forms.Textarea(attrs={'rows': 5}),
        }