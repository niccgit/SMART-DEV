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
