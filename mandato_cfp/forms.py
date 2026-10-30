from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget 
from .models import Mandato, TipoMandato, FuncaoMandato


class MandatoForm(forms.ModelForm):
    class Meta:
        model = Mandato
        fields = [
            'nome_pessoa',
            'id_tipo_mandato',
            'id_funcao_mandato',
            'data_inicio',
            'data_fim',
            # Kolom Deskripsi Multilingual
            'descricao',       # Português (Default)
            'descricao_tet',   # Tetun
            'descricao_en',    # English
            'imagen',
        ]
        labels = {
            'nome_pessoa': _('Nome da Pessoa'),
            'id_tipo_mandato': _('Tipo de Mandato'),
            'id_funcao_mandato': _('Função'),
            'data_inicio': _('Data de Início'),
            'data_fim': _('Data de Fim'),
            'descricao': _('Descrição (Português)'),
            'descricao_tet': _('Descrição (Tetun)'),
            'descricao_en': _('Descrição (English)'),
            'imagen': _('Fotografia / Imagem'),
        }
        widgets = {
            'nome_pessoa': forms.TextInput(attrs={'class': 'form-control'}),
            'id_tipo_mandato': forms.Select(attrs={'class': 'form-control'}),
            'id_funcao_mandato': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            # Menerapkan CKEditor pada field deskripsi multibahasa
            'descricao': CKEditor5Widget(config_name='default'),
            'descricao_tet': CKEditor5Widget(config_name='default'),
            'descricao_en': CKEditor5Widget(config_name='default'),
            
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class TipoMandatoForm(forms.ModelForm):
    class Meta:
        model = TipoMandato
        fields = [
            'tipo_mandato',      # Português (Default)
            'tipo_mandato_tet',  # Tetun
            'tipo_mandato_en',   # English
        ]
        labels = {
            'tipo_mandato': _('Tipo de Mandato (Português)'),
            'tipo_mandato_tet': _('Tipo de Mandato (Tetun)'),
            'tipo_mandato_en': _('Tipo de Mandato (English)'),
        }
        widgets = {
            'tipo_mandato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: I Mandato')}),
            'tipo_mandato_tet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: Mandatu Dahuluk')}),
            'tipo_mandato_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: First Mandate')}),
        }


class FuncaoMandatoForm(forms.ModelForm):
    class Meta:
        model = FuncaoMandato
        fields = [
            'funcao_mandato',      # Português (Default)
            'funcao_mandato_tet',  # Tetun
            'funcao_mandato_en',   # English
        ]
        labels = {
            'funcao_mandato': _('Função (Português)'),
            'funcao_mandato_tet': _('Função (Tetun)'),
            'funcao_mandato_en': _('Função (English)'),
        }
        widgets = {
            'funcao_mandato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: Presidente')}),
            'funcao_mandato_tet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: Prezidente')}),
            'funcao_mandato_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: President')}),
        }