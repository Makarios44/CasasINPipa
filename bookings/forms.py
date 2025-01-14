from django import forms
from .models import Casa

  
class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ['nome', 'descricao', 'endereco', 'preco_diaria', 'tipo', 'imagem_principal']

    def clean_preco_diaria(self):
        preco = self.cleaned_data.get('preco_diaria')
        if preco <= 0:
            raise forms.ValidationError("O preço diário deve ser maior que zero.")
        return preco
