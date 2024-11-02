# Usando uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala pacotes do sistema operacional necessários
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências para o contêiner e instala pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o contêiner
COPY . .

# Expõe a porta em que o Streamlit vai rodar
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "src/streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
