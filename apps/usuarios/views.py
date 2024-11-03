# main/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

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
