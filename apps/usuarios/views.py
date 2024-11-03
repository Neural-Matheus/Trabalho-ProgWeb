# main/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.models import User

from apps.usuarios.forms import CadastroForms, LoginForms

def login_view(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            email = form["email"].value()
            senha = form["senha"].value() 

            usuario = auth.authenticate(
                request = request, 
                email = email,
                password = senha
            )
            
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f"{email} logado com sucesso!")
                return redirect("index")
            else:
                messages.error(request, "Erro ao efetuar login!")
                return redirect("login")
            
    return render(request, 'login/pagina_login.html', {"form" : form})

def cadastro_view(request):
    # Verifica se o método é POST
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            email = form["email"].value()
            senha1 = form["senha1"].value()

            if User.objects.filter(email = email).exists():
                messages.error(request, "Usuário já existe!")
                return redirect("cadastro")
            
            usuario = User.objects.create_user(
               email = email, password = senha1
            )

            usuario.save()
            messages.success(request, f"{email} cadastrado com sucesso!")
            return redirect("login")
        
    return render(request, 'signup/pagina_cadastro.html', {"form" : form})
