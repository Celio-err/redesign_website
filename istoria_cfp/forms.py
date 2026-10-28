from django import forms
from ckeditor.widgets import CKEditorWidget  
from .models import IstoriaCFP

class IstoriaCFPForm(forms.ModelForm):
    class Meta:
        model = IstoriaCFP
        fields = [
            'titulo', 'subtitulo', 'conteudo', 
            'titulo_tet', 'subtitulo_tet', 'conteudo_tet', 
            'titulo_en', 'subtitulo_en', 'conteudo_en'
        ]
        widgets = {
            # Português
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título em Português'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtítulo em Português'}),
            'conteudo': CKEditorWidget(config_name='default'),
            
            # Tetun
            'titulo_tet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título em Tetun'}),
            'subtitulo_tet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtítulo em Tetun'}),
            'conteudo_tet': CKEditorWidget(config_name='default'),
            
            # English
            'titulo_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title in English'}),
            'subtitulo_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtitle in English'}),
            'conteudo_en': CKEditorWidget(config_name='default'),
        }