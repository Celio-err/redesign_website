from django import forms
from .models import Noticias, TipoNoticias


class NoticiasForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = [
            'id_tipo_noticia', 'data_publicacao', 'imagen',
            
            # --- Português (Default / Utama) ---
            'nome_noticia', 'descricao', 'noticia',
            
            # --- Tetun ---
            'nome_noticia_tet', 'descricao_tet', 'noticia_tet',
            
            # --- English ---
            'nome_noticia_en', 'descricao_en', 'noticia_en',
        ]
        labels = {
            'id_tipo_noticia': 'Tipo Notícia',
            
            # Labels PT
            'nome_noticia': 'Título (PT)',
            'descricao': 'Descrição (PT)',
            'noticia': 'Notícia (PT)',
            
            # Labels Tetun
            'nome_noticia_tet': 'Título (Tetun)',
            'descricao_tet': 'Descrição (Tetun)',
            'noticia_tet': 'Notícia (Tetun)',
            
            # Labels English
            'nome_noticia_en': 'Título (English)',
            'descricao_en': 'Descrição (English)',
            'noticia_en': 'Notícia (English)',
            
            'data_publicacao': 'Data de Publicação',
            'imagen': 'Imagem',
        }
        widgets = {
            'id_tipo_noticia': forms.Select(attrs={'class': 'form-control'}),
            'data_publicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            # Inputs PT
            'nome_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'noticia': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            
            # Inputs Tetun
            'nome_noticia_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_tet': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'noticia_tet': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            
            # Inputs English
            'nome_noticia_en': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'noticia_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class TipoNoticiasForm(forms.ModelForm):
    class Meta:
        model = TipoNoticias
        fields = ['tipo_noticia', 'descricao']
        widgets = {
            'tipo_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }