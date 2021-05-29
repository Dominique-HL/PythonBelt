from django import forms
from django.forms.widgets import ClearableFileInput

from ..models import User

my_default_errors = {
    'required': 'Requerido',
    'invalid': 'Fecha Invalida'
}

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label = 'Confirmar Contraseña'
    )

    class Meta:
        model = User
        fields = ['name','lastname','email', 'password']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder': 'Nombres Completos'}),
            'password' : forms.PasswordInput()
        }
        labels = {
           'name': "Nombres",
           'lastname': "Apellidos",
           'email': "Correo Electronico",
           'password': "Contraseña",
        }

    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if (password != confirm_password):
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )