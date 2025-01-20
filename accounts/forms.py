from django import forms
from .models import User

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nome', 
                  'sobrenome', 
                  'email',
               
                    'telefone',
                      'data_nascimento']
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Nova Senha")