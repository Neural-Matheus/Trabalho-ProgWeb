# Trabalho-ProgWeb
Repositório destinado ao trabalho de programação web do segundo semestre de 2024.

# Preparação do Ambiente de Desenvolvimento

Nesta seção, detalhamos a preparação do ambiente de desenvolvimento para o projeto. Todo o ambiente foi configurado para ser executado de maneira isolada e replicável através de contêineres **Docker**, garantindo que todos os pacotes, ferramentas e variáveis de ambiente sejam instalados e configurados corretamente. O uso do **Docker** facilita a portabilidade e evita problemas de incompatibilidade de versões entre diferentes sistemas.

## Configuração com Docker
O projeto foi containerizado utilizando **Docker** e pode ser executado de maneira consistente em qualquer ambiente que tenha o **Docker** instalado. Abaixo estão os principais componentes e ferramentas que serão configurados:

### 1. **Dockerfile**
O **Dockerfile** contém todas as instruções necessárias para construir a imagem do projeto, incluindo a instalação de bibliotecas como **Python**, **FastAPI**, **PostgreSQL**, **TensorFlow**, **Pandas**, entre outros. Todos os pacotes e dependências estão definidos no **requirements.txt** ou no **Pipfile**, garantindo que as versões corretas sejam instaladas.

### 2. **Docker Compose**
Utilizamos o **Docker Compose** para orquestrar os diferentes serviços do projeto. Ele automatiza o processo de subir múltiplos contêineres, como o servidor **FastAPI**, o banco de dados **PostgreSQL** e outros serviços auxiliares necessários para o funcionamento da aplicação. O arquivo **docker-compose.yml** contém as definições dos serviços, redes e volumes.

### 3. **Variáveis de Ambiente**
As variáveis de ambiente sensíveis, como as credenciais do banco de dados e chaves de API, estão armazenadas em um arquivo **.env** que é carregado automaticamente pelos contêineres no momento da execução. Este arquivo não é versionado por motivos de segurança, mas um exemplo (**.env.example**) é fornecido para facilitar a configuração inicial.

### 4. **Pacotes e Dependências**
Todas as dependências de Python estão listadas no **requirements.txt**, que é utilizado dentro do **Dockerfile** para garantir que todas as bibliotecas necessárias, como **TensorFlow**, **Pandas**, **scikit-learn**, **FastAPI**, entre outras, sejam instaladas no ambiente do contêiner.

## Passos Básicos para Executar o Projeto
1. Certifique-se de ter o **Docker** e **Docker Compose** instalados em sua máquina. Para instalar o Docker, siga a [documentação oficial do Docker](https://docs.docker.com/get-docker/).
2. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/Neural-Matheus/Trabalho-ProgWeb
   cd Trabalho-ProgWeb
   ```
3. Configure as variáveis de ambiente, copiando o arquivo **.env.example** para **.env** e preenchendo com as informações corretas.
   ```bash
   cp .env.example .env
   ```
4. Suba os contêineres utilizando o **Docker Compose**:
   ```bash
   docker-compose up --build
   ```
5. Acesse o sistema através do endpoint fornecido (http://localhost:8000).
