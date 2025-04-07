from django import forms
from .models import Casa, ImagemAdicional, Videos

class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = [
            'titulo', 'descricao', 'endereco', 'contato', 'preco_mes', 'imagem_principal',
            'numero_quartos', 'numero_banheiros', 'numero_suites', 'numero_vagas_garagem',
            'mobiliado', 'aceita_pets', 'ar_condicionado', 'piscina', 'area_de_lazer',
            'churrasqueira', 'wifi_incluido', 'energia_inclusa', 'agua_inclusa', 'capacidade_máxima'
        ]

    def clean_preco_mes(self):
        preco = self.cleaned_data.get('preco_mes')
        if preco <= 0:
            raise forms.ValidationError("O preço deve ser maior que zero.")
        return preco



class ImagemAdicionalForm(forms.ModelForm):
    class Meta:
        model = ImagemAdicional
        fields = ['imagem']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ['video']
