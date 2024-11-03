# main/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseServerError
import os
import subprocess
import psutil

def login_view(request):
    # Renderiza a página de login
    return render(request, 'login/pagina_login.html')

def cadastro_view(request):
    # Verifica se o método é POST
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
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