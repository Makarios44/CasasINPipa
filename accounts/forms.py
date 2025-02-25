from django import forms
from django.contrib.auth.models import User

class EditarPerfilForm(forms.ModelForm):
    password = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(),
        required=False,  # A senha é opcional
    )

    class Meta:
        model = User
        fields = ['email']  # Apenas e-mail será editável, mas senha é opcional

    def save(self, commit=True):
        user = super().save(commit=False)

        # Se o usuário digitou uma nova senha, atualiza
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=256)
