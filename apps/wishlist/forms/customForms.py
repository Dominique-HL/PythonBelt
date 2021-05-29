from django import forms
from django.db.models.fields import EmailField
from ..models import User


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), required=True)

    def login(self, request):
        email= self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.authenticate(email, password)
        return user