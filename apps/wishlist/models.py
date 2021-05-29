from django.db import models
import re

from django.core import validators
from django.core.exceptions import ValidationError

from django.contrib.auth.hashers import check_password, make_password


MIN_FIELD_LENGHT = 4

def ValidarLongitudMinima(cadena):
    if len(cadena) < MIN_FIELD_LENGHT:
        raise ValidationError(
            f"{cadena} tiene deberia tener mas de {MIN_FIELD_LENGHT} caracteres"
        )

def ValidarEmail(cadena):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(cadena):  
        raise ValidationError(
            f'{cadena} no es un e-mail valido'
        )        


class User(models.Model):
    name = models.CharField(max_length=45, blank = False, null =False, validators=[ValidarLongitudMinima])
    lastname = models.CharField(max_length=45, blank = False, null = False , validators=[ValidarLongitudMinima])
    email = models.CharField(max_length=50, validators=[ValidarEmail])
    password = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    
    @staticmethod # User.authenticate('s', 'p')
    #sin decorador, userObj = User()  userObj.authenticate(s,s)
    def authenticate(email, password): 
        results = User.objects.filter(email = email) 
        if len(results) == 1:
            user = results[0]
            bd_password = user.password
            if check_password(password, bd_password):
                  return user
        return None           


class Wish(models.Model):
    name = models.CharField(max_length=45, blank = False, null =False, validators=[ValidarLongitudMinima])
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="wishes", on_delete=models.CASCADE)