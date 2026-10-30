from django import forms
from .models import Noticias, TipoNoticias 
from django_ckeditor_5.widgets import CKEditor5Widget  

MAX_IMAGENS = 10          # jumlah maksimal gambar per notícia
MAX_MB = 5                # ukuran maksimal per gambar


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    """ImageField yang menerima banyak file sekaligus (pola resmi Django)."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"accept": "image/*", "class": "form-control"}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(d, initial) for d in data]
        return [single_clean(data, initial)] if data else []


class NoticiasForm(forms.ModelForm):
    imagens = MultipleImageField(required=False, label="Imagens")

    class Meta:
        model = Noticias
        exclude = ["id_noticia", "inserido_por", "inserido_em", "imagen"]
        widgets = {
            # Memaksa input menjadi type="date" agar kalender dan pemilih tahun muncul native
            'data_publicacao': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
            'id_tipo_noticia': forms.Select(attrs={'class': 'form-select'}),
            
            # Field judul dan teks lainnya
            'nome_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_noticia_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_noticia_en': forms.TextInput(attrs={'class': 'form-control'}),
            
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'descricao_tet': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'descricao_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            'noticia': CKEditor5Widget(config_name='default'),
            'noticia_tet': CKEditor5Widget(config_name='default'),
            'noticia_en': CKEditor5Widget(config_name='default'),
        }

    def clean_imagens(self):
        files = self.cleaned_data.get("imagens", [])
        ja_existem = self.instance.imagens.count() if self.instance.pk else 0

        if ja_existem + len(files) > MAX_IMAGENS:
            raise forms.ValidationError(
                f"No máximo {MAX_IMAGENS} imagens por notícia "
                f"(já tem {ja_existem})."
            )
        for f in files:
            if f.size > MAX_MB * 1024 * 1024:
                raise forms.ValidationError(
                    f"'{f.name}' excede {MAX_MB} MB."
                )
        return files


class TipoNoticiasForm(forms.ModelForm):
    class Meta:
        model = TipoNoticias
        fields = ['tipo_noticia', 'tipo_noticia_tet', 'tipo_noticia_en', 'is_cooperacao','descricao']
        widgets = {
            'tipo_noticia': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_noticia_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_noticia_en': forms.TextInput(attrs={'class': 'form-control'}),
            'is_cooperacao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }