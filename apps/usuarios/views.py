# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseServerError
import os
import subprocess
import psutil
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from apps.usuarios.forms import LoginForms, CadastroForms

from apps.usuarios.forms import CadastroForms, LoginForms

def login_view(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            username = form["username"].value()
            senha = form["senha"].value() 

            usuario = auth.authenticate(
                request = request, 
                username = username,
                password = senha
            )
            
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f"{username} logado com sucesso!")
                return redirect('http://localhost:8501')
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
            username = form["username"].value()
            senha1 = form["senha1"].value()

            if User.objects.filter(username = username).exists():
                messages.error(request, "Usuário já existe!")
                return redirect("cadastro")
            
            usuario = User.objects.create_user(
               username = username, password = senha1
            )

            usuario.save()
            messages.success(request, f"{username} cadastrado com sucesso!")
            return redirect("login")
        
        # Redireciona para a página de login
        return redirect(reverse('login'))
    
    # Renderiza a página de cadastro
    return render(request, "signup/pagina_cadastro.html", {"form" : form})

def iniciar_streamlit(request):
    caminho_script = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app/templates/streamlit/model.py'))

    # Verifica se algum processo Streamlit já está rodando
    streamlit_rodando = any(
        'streamlit' in (p.info['cmdline'][0] if p.info['cmdline'] else '') 
        for p in psutil.process_iter(attrs=['pid', 'name', 'cmdline'])
    )

    if not streamlit_rodando:
        try:
            # Inicia o processo Streamlit de forma assíncrona
            subprocess.Popen(['streamlit', 'run', caminho_script], start_new_session=True)
        except Exception as e:
            # Retorna um erro 500 caso o processo falhe ao iniciar
            return HttpResponseServerError(f"Erro ao iniciar o Streamlit: {e}")

    # Redireciona o usuário para a interface do Streamlit
    return redirect('http://localhost:8501')

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, "list/user_list.html", {"users": users})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        users = User.objects.all()
        return render(request, "list/user_list.html", {"users": users})
    return render(request, "list/confirm_delete.html", {"user": user})
