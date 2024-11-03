import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

# Dividir o título e o botão em colunas para posicioná-los lado a lado
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("Avalia Aí - Chat Simples")
with col2:
    if st.button('Ver Lista de Usuários'):
        # Redireciona automaticamente para a URL da lista de usuários no Django
        st.write('<meta http-equiv="refresh" content="0; url=http://localhost:8000/users/">', unsafe_allow_html=True)

# Verifica se existe o histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens armazenadas no histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura a entrada do usuário e exibe a resposta
if prompt := st.chat_input("Digite sua pergunta:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    mensagens_completas = [
        SystemMessage(content="Você é um assistente amigável."),
        *[
            HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
            for msg in st.session_state.messages
        ]
    ]

    with st.chat_message("assistant"):
        try:
            response = chat.invoke(mensagens_completas).content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
