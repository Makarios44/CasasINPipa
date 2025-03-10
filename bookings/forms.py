from django import forms
from .models import Casa, ImagemAdicional

class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = [ 'descricao', 'endereco', 'contato', 'preco', 'imagem_principal']

    def clean_preco_diaria(self):
        preco = self.cleaned_data.get('preco_diaria')
        if preco <= 0:
            raise forms.ValidationError("O preço deve ser maior que zero.")
        return preco


class ImagemAdicionalForm(forms.ModelForm):
    class Meta:
        model = ImagemAdicional
        fields = ['imagem']