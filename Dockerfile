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

# Exponha a porta 8501 para Streamlit e 5000 para Flask (ou ajuste conforme sua configuração)
EXPOSE 8501 5000

# Use argumentos para definir o modo de execução (Streamlit ou Flask)
ARG APP_MODE
ENV APP_MODE=${APP_MODE}

# Comando para rodar o aplicativo com base no APP_MODE
CMD ["sh", "-c", "if [ '$APP_MODE' = 'streamlit' ]; then streamlit run src/streamlit/model.py --server.port=8501 --server.address=0.0.0.0; else flask --app src/app.py run --host=0.0.0.0 --port=5000; fi"]
