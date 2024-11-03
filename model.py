import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

# Funções de carregamento de documentos (site, PDF, YouTube) permanecem as mesmas

def main():
    st.title('Avalia Aí')

    # Botão para navegar para a lista de usuários (hosteada no Django)
    if st.button('Ver Lista de Usuários'):
        # Redireciona para a URL da lista de usuários no Django
        st.markdown("[Lista de Usuários](http://localhost:8000/users/)")  # Supondo que Django está rodando na porta 8000

    # Interface principal do chat
    st.header('Selecione a fonte de informação:')
    opcoes = ['Site', 'PDF', 'Vídeo do YouTube']
    escolha = st.selectbox('Escolha uma opção:', opcoes)

    documento = ''
    if escolha == 'Site':
        url_site = st.text_input('Digite a URL do site:')
        if url_site:
            documento = carrega_site(url_site)
    elif escolha == 'PDF':
        caminho_pdf = st.file_uploader('Envie o arquivo PDF:', type='pdf')
        if caminho_pdf:
            documento = carrega_pdf(caminho_pdf)
    elif escolha == 'Vídeo do YouTube':
        url_youtube = st.text_input('Digite a URL do vídeo do YouTube:')
        if url_youtube:
            documento = carrega_youtube(url_youtube)

    if documento:
        st.success('Documento carregado com sucesso!')

        if 'mensagens' not in st.session_state:
            st.session_state.mensagens = []
        pergunta = st.text_input('Você:', key='input')

        if st.button('Enviar'):
            if pergunta:
                st.session_state.mensagens.append(HumanMessage(content=pergunta))
                mensagem_system = SystemMessage(content=f'Você é um assistente amigável chamado Avalia Aí. Você utiliza as seguintes informações para formular as suas respostas: {documento}')
                mensagens_completas = [mensagem_system] + st.session_state.mensagens

                template = ChatPromptTemplate.from_messages(mensagens_completas)
                chain = template | chat

                try:
                    resposta = chain.invoke({}).content
                    st.session_state.mensagens.append(AIMessage(content=resposta))
                    st.text_area('Avalia Aí:', value=resposta, height=200)
                except Exception as e:
                    st.error(f'Ocorreu um erro: {e}')

        if st.session_state.mensagens:
            for msg in st.session_state.mensagens:
                if isinstance(msg, HumanMessage):
                    st.write(f'**Você:** {msg.content}')
                elif isinstance(msg, AIMessage):
                    st.write(f'**AsimoBot:** {msg.content}')

if __name__ == '__main__':
    main()
