# Usando uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instala todas as dependências especificadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exemplo de pacotes adicionais que podem ser instalados diretamente, caso necessário
# RUN apt-get update && apt-get install -y libpq-dev

# Expõe a porta em que o FastAPI vai rodar
EXPOSE 8000

# Copia todo o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Configura variáveis de ambiente 
# ENV ENV_VAR_NAME=value

# Comando para rodar o FastAPI com o Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
