# main/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseServerError
import os
import subprocess
import psutil

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
        
        # Exibe mensagem flash
        messages.success(request, f'Recebido cadastro com email: {email}')
        
        # Redireciona para a página de login
        return redirect(reverse('login'))
    
    # Renderiza a página de cadastro
    return render(request, 'signup/pagina_cadastro.html')
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
