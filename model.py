import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
with col1:
    st.title("Avalia Aí")
with col2:
    if st.button('Ver Lista de Usuários'):
        st.write('<meta http-equiv="refresh" content="0; url=http://localhost:8000/users/">', unsafe_allow_html=True)
with col3:
    if st.button('Voltar para o Login'):
        st.write('<meta http-equiv="refresh" content="0; url=http://localhost:8000/login/">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Informe a avaliação de usuário:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    mensagens_completas = [
        SystemMessage(content=
                      """
                    Hello, AI! Please act as an expert in review analysis and product improvement with years of consultancy experience in this field. I will provide a product review, and I need you to perform 3 tasks in this order:

                    Analyze the overall sentiment of the review.
                    Identify the positive and negative points mentioned.
                    Suggest a specific improvement I can implement based on the customer's feedback.
                    Use <<TEXT>> as placeholders for the information, and provide your response in Brazilian Portuguese in the following format:

                    Sentimento predominante: <<summary of sentiment analysis>>
                    Pontos positivos:
                    <<list of positive points>>
                    Pontos negativos:
                    <<list of negative points>>

                    Sugestão de melhoria:
                    <<specific, actionable improvement suggestion>>
                      """
        ),
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
