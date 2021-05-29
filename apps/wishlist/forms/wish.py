from django import forms
from django.forms import widgets
from ..models import Wish
import datetime

class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = ['name', 'due_date', 'completed']
        widgets = {
            'completed' : forms.CheckboxInput()
        }
        labels ={
            'name': 'Deseo',
            'due_date' : 'Fecha completado',
            'completed' : 'Completado',
        }
    
    def clean(self):
        date = self.cleaned_data['due_date']
        if date < datetime.date.today():
            raise forms.ValidationError('no puede ser menor a la fecha actual')