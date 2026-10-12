from django import forms
from .models import DDDO, TipoDDDO


class DDDOForm(forms.ModelForm):
    ficheiro_upload = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Ficheiro'
    )

    class Meta:
        model = DDDO
        fields = [
            'id_tipo_dddo', 'nome_dddo', 'descricao',
        ]
        labels = {
            'id_tipo_dddo': 'Tipo de DDDO',
            'nome_dddo': 'Nome do DDDO',
            'descricao': 'Descrição',
        }
        widgets = {
            'id_tipo_dddo': forms.Select(attrs={'class': 'form-control'}),
            'nome_dddo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TipoDDDOForm(forms.ModelForm):
    class Meta:
        model = TipoDDDO
        fields = ['tipo_dddo']
        labels = {
            'tipo_dddo': 'Tipo de DDDO',
        }
        widgets = {
            'tipo_dddo': forms.TextInput(attrs={'class': 'form-control'}),
        }