import streamlit as st

import bcrypt
from banco import conectar

if not st.session_state.get("autenticado", False):
    st.error("Você precisa fazer login para realizar esta página.")
    st.stop()

if st.session_state.get("tipo") != "admin":
    st.error("Acesso permitido somente para administradores")
    st.stop()

st.title("Coordenação")
st.write(
    "Cadastre, consulte, edite e inative funcionários da floricultura"
)
aba1, aba2, aba3 =  st.tabs([
    "Cadastrar funcionário",
    "Gerenciar usuários"
])

with aba1:
    st.subheader("Cadastro funcionário")
    with st.form("formulario_cadastro"):

        nome = st.text_input("Nome completo")
        email = st.text_input("Digite seu email")


