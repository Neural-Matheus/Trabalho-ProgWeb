# Usando uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Configura o PYTHONPATH para o diretório de trabalho
ENV PYTHONPATH=/app

# Instala pacotes do sistema operacional necessários
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências para o contêiner e instala pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o contêiner
COPY . .

# Exponha as portas 8501 e 5000
EXPOSE 8501 5000

# Comando para rodar o aplicativo Django na porta 5000
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:5000"]
