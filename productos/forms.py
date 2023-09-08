from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 10:
            raise forms.ValidationError(
                _('El nombre de usuario debe tener máximo 10 caracteres'))
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Las contraseñas no coinciden'))
        return password2


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Nombre de usuario'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username', 'placeholder': 'Username' })
    )
    password = forms.CharField(
        label=_('Contraseña'),
        widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'password', 'placeholder': 'Contraseña'})
    )
