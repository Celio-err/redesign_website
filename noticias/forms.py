from django import forms
from .models import Noticias, TipoNoticias 
from django_ckeditor_5.widgets import CKEditor5Widget  

MAX_MB = 5  # ukuran maksimal untuk gambar sampul (5 MB)

class NoticiasForm(forms.ModelForm):
    class Meta:
        model = Noticias
        exclude = ["id_noticia", "inserido_por", "inserido_em", "imagen"]
        widgets = {
            # Memaksa input menjadi type="date" agar kalender muncul native
            'data_publicacao': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
            'id_tipo_noticia': forms.Select(attrs={'class': 'form-select'}),
            'cooperacao': forms.Select(attrs={'class': 'form-select'}),
            
            # Input Gambar Sampul Tunggal
            'imagem_capa': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            
            # Field judul dan teks lainnya (Português)
            'nome_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'noticia': CKEditor5Widget(config_name='default'),
            
            # Tetun
            'nome_noticia_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_tet': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'noticia_tet': CKEditor5Widget(config_name='default'),
            
            # English
            'nome_noticia_en': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'noticia_en': CKEditor5Widget(config_name='default'),
        }

    def clean_imagem_capa(self):
        f = self.cleaned_data.get("imagem_capa")
        if f and f.size > MAX_MB * 1024 * 1024:
            raise forms.ValidationError(f"O tamanho da imagem excede {MAX_MB} MB.")
        return f


class TipoNoticiasForm(forms.ModelForm):
    class Meta:
        model = TipoNoticias
        fields = ['tipo_noticia', 'tipo_noticia_tet', 'tipo_noticia_en', 'is_cooperacao', 'descricao']
        widgets = {
            'tipo_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_noticia_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_noticia_en': forms.TextInput(attrs={'class': 'form-control'}),
            'is_cooperacao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }