from django import forms
from .models import Cooperacao

class CooperacaoForm(forms.ModelForm):
    class Meta:
        model = Cooperacao
        fields = [
            'nome_parceiro',
            'slug',
            'logo_parceiro',
            'pais_parceiro',
            'descricao',
        ]
        widgets = {
            'nome_parceiro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: ASEAN, UNDP, CSC, Governo Local'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional (gerado automaticamente)'
            }),
            'logo_parceiro': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'pais_parceiro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Timor-Leste, Internacional'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição resumida sobre a parceria ou instituição...'
            }),
        }