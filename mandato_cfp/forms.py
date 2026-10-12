from django import forms

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
            'descricao',
            'imagen',
        ]
        labels = {                              # ← labels iha fatin rasik, la iha laran fields
            'nome_pessoa': 'Nome Pessoa',
            'id_tipo_mandato': 'Tipo Mandato',
            'id_funcao_mandato': 'Função',
            'data_inicio': 'Data Início',
            'data_fim': 'Data Fim',
            'descricao': 'Descrição',
            'imagen': 'Foto',
        }
        widgets = {
            'nome_pessoa': forms.TextInput(attrs={'class': 'form-control'}),
            'id_tipo_mandato': forms.Select(attrs={'class': 'form-control'}),
            'id_funcao_mandato': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class TipoMandatoForm(forms.ModelForm):
    class Meta:
        model = TipoMandato
        fields = ["tipo_mandato"]
        labels = {
            "tipo_mandato": "Tipo de Mandato",
        }
        widgets = {
            "tipo_mandato": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }





class FuncaoMandatoForm(forms.ModelForm):
    class Meta:
        model = FuncaoMandato
        fields = ["funcao_mandato"]
        labels = {
            "funcao_mandato": "Função",
        }
        widgets = {
            "funcao_mandato": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }