import streamlit as st
import re
import pandas as pd
import base64

st.set_page_config(page_title="Com carinho, Flor - Sistema", layout="wide")

def carregar_css(nome_arquivo):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        st.markdown(f"<style>{arquivo.read()}</style>", unsafe_allow_html=True)

def carregar_imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = carregar_imagem_base64("Logo Com carinho, Flor.jpg")

estrutura_setores = {
    "Administração": ["Cadastrar funcionário", "Gerenciar usuários"],
    "Financeiro": ["Movimentações", "Pagamentos"],
    "Atendimento ao Cliente": ["Cadastrar novo pedido", "Consultar Pedidos"],
    "Gestão de E-commerce": ["Catálogo de produtos"],
    "Estoque": ["Estoque"],
    "Montagem": ["Fila de montagem"]
}

if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = [
        {"Nome": "Giovanna (Admin)", "CPF": "111.111.111-11", "Setor": "Administração", "Email": "admin@flor.com", "Senha": "Admin123"},
        {"Nome": "Ana (Financeiro)", "CPF": "222.222.222-22", "Setor": "Financeiro", "Email": "fin@flor.com", "Senha": "Finan123"},
        {"Nome": "Lucas (Atendimento)", "CPF": "333.333.333-33", "Setor": "Atendimento ao Cliente", "Email": "atend@flor.com", "Senha": "Atend123"},
        {"Nome": "Carla (E-commerce)", "CPF": "444.444.444-44", "Setor": "Gestão de E-commerce", "Email": "ecom@flor.com", "Senha": "Ecom1234"},
        {"Nome": "Pedro (Estoque)", "CPF": "555.555.555-55", "Setor": "Estoque", "Email": "estoque@flor.com", "Senha": "Estoq123"},
        {"Nome": "Marcos (Montagem)", "CPF": "666.666.666-66", "Setor": "Montagem", "Email": "montagem@flor.com", "Senha": "Monta123"}
    ]
