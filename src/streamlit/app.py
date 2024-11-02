import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader

api_key = ''
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

def carrega_site(url_site):
    loader = WebBaseLoader(url_site)
    lista_documentos = loader.load()
    documento = ''.join(doc.page_content for doc in lista_documentos)
    return documento

def carrega_pdf(caminho_pdf):
    loader = PyPDFLoader(caminho_pdf)
    lista_documentos = loader.load()
    documento = ''.join(doc.page_content for doc in lista_documentos)
    return documento

def carrega_youtube(url_youtube):
    loader = YoutubeLoader.from_youtube_url(url_youtube, language=['pt'])
    lista_documentos = loader.load()
    documento = ''.join(doc.page_content for doc in lista_documentos)
    return documento

def main():
    st.title('Avalia Aí')

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
