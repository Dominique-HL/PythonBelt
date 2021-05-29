from collections import deque
import re
from .models import Wish, User
from django.shortcuts import render, redirect, resolve_url
from .forms.user import UserForm
from .forms.wish import WishForm
from .forms.customForms import LoginForm

def index(request):
    formRegister = UserForm()
    formLogin = LoginForm()
    return render(request, 'index.html', {'formRegister': formRegister, 'formLogin': formLogin})

def register(request):
    if request.method == 'GET':
        formRegister = UserForm()
    else:
        formRegister = UserForm(request.POST)
        if formRegister.is_valid():
            user = formRegister.save()
            request.session['logged_user'] = user.name
            return redirect("/home")
    formLogin = LoginForm()         
    return render(request, 'index.html',{'formLogin':formLogin, 'formRegister': formRegister}) 


def login(request):
    if request.method == "GET":
        formLogin = LoginForm()
    else:
        formLogin = LoginForm(request.POST)
        if formLogin.is_valid():
            user = formLogin.login(request.POST)
            if user:
                print ("login --->")
                request.session['logged_user'] = user.name
                request.session['logged_user_id'] = user.id
                return redirect("/home")
    formRegister = UserForm()
    return render(request, 'index.html',{'formLogin':formLogin, 'formRegister': formRegister}) 

def logout(request):  
    try:
        del request.session['logged_user']
        del request.session['logged_user_id']
    except:
        print('Error')
    return redirect("/")                    

def home(request):
    try:
        user = User.objects.get(id = int(request.session['logged_user_id']))
        if user:
            #deseos pendientes , completed = False 
            wishes_pending = user.wishes.all().filter(completed = False)
            #deseos completadas
            wishes_completed = user.wishes.all().filter(completed = True)
            print("=====completed> ", wishes_completed)
            return render(request, 'home.html', {'user': user, 'wishes_pending': wishes_pending, 'wishes_completed': wishes_completed})
        else:
            return redirect("/")
    except:
        return redirect("/")


def wish(request):
    if request.method == "POST":
        #guardar el deseo
        user = User.objects.get(id = int(request.session['logged_user_id']))
        wish = Wish.objects.create(name = request.POST['name'], 
                            due_date = request.POST['due_date'],
                            user = user)
        return redirect("/home")   


def wish_detail(request, wish_id):
    wish = Wish.objects.get(id = int(wish_id))
    formWish = WishForm(instance=wish)
    if request.method == "POST": #actualizar task
        formWish = WishForm(request.POST, instance=wish)
        if formWish.is_valid():
            completed = request.POST.get('completed', '') == 'on'
            wish.name = request.POST['name']
            wish.completed = completed
            wish.save() #actualizar task
            return redirect('/home')
    return render(request, 'wish_detail.html' , {'formWish': formWish})     