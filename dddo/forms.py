from django import forms
from django.utils.translation import gettext_lazy as _
from .models import DDDO, TipoDDDO


class TipoDDDOForm(forms.ModelForm):
    class Meta:
        model = TipoDDDO
        fields = ['tipo_dddo', 'tipo_dddo_tet', 'tipo_dddo_en']
        labels = {
            'tipo_dddo': _('Tipo de Legislação (Português)'),
            'tipo_dddo_tet': _('Tipo de Legislação (Tetun)'),
            'tipo_dddo_en': _('Tipo de Legislação (English)'),
        }
        widgets = {
            'tipo_dddo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: Leis')}),
            'tipo_dddo_tet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: Lei sira')}),
            'tipo_dddo_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: Laws')}),
        }

class DDDOForm(forms.ModelForm):
    # Buat field kustom untuk upload file karena documentos_dddo adalah BinaryField
    documentos_dddo_file = forms.FileField(
        required=False,
        label=_('Ficheiro do Documento'),
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = DDDO
        fields = [
            'id_tipo_dddo',
            'nome_dddo',
            'nome_dddo_tet',
            'nome_dddo_en',
            'descricao',
            'descricao_tet',
            'descricao_en',
            # 'documentos_dddo' DIHAPUS dari sini agar tidak error
        ]
        labels = {
            'id_tipo_dddo': _('Tipo de Legislação'),
            'nome_dddo': _('Título do Documento (Português)'),
            'nome_dddo_tet': _('Título do Documento (Tetun)'),
            'nome_dddo_en': _('Título do Documento (English)'),
            'descricao': _('Descrição (Português)'),
            'descricao_tet': _('Descrição (Tetun)'),
            'descricao_en': _('Descrição (English)'),
        }
        widgets = {
            'id_tipo_dddo': forms.Select(attrs={'class': 'form-control'}),
            'nome_dddo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_dddo_tet': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_dddo_en': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'descricao_tet': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'descricao_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('documentos_dddo_file')
        
        # Konversi file yang diupload menjadi biner
        if file:
            instance.documentos_dddo = file.read()
            instance.nome_dddo_original = file.name
            
        if commit:
            instance.save()
        return instance