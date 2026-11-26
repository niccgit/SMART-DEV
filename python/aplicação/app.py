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

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = None

def validar_senha(senha):
    if len(senha) < 8 or len(senha) > 16:
        return False, "A senha deve ter entre 8 e 16 caracteres."
    if not re.search(r"[a-z]", senha):
        return False, "Falta pelo menos 1 letra minúscula."
    if not re.search(r"[A-Z]", senha):
        return False, "Falta pelo menos 1 letra maiúscula."
    if not re.search(r"[0-9]", senha):
        return False, "Falta pelo menos 1 número."
    return True, "Ok"

def autenticar_usuario(email, senha):
    for func in st.session_state.funcionarios:
        if func["Email"] == email and func["Senha"] == senha:
            return func
    return None

if st.session_state.usuario_logado is None:
    carregar_css("style.css")
    margem_esq, centro, margem_dir = st.columns([0.5, 3.4, 0.5])
    with centro:
        lado_esq, lado_dir = st.columns([1, 1.05], gap="small")
        with lado_esq:
            st.markdown(f"""
                <div class="painel-esquerdo-login">
                    <div class="moldura-interna-esq">
                        <div class="cantos-ornamento"><span>❖</span><span>❖</span></div>
                        <div class="conteudo-esquerdo-centro">
                            <h1 class="titulo-marca-login marca-italico">Com carinho, Flor</h1>
                            <p class="texto-boas-vindas">
                                Aqui cada buquê nasce com cuidado. Entre para acompanhar pedidos, estoque e finanças da sua floricultura.
                            </p>
                            <div class="circulo-flor-destaque">
                                <img src="data:image/jpeg;base64,{logo_base64}">
                            </div>
                        </div>
                        <div class="cantos-ornamento"><span>❖</span><span>❖</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with lado_dir:
            with st.form("form_login"):
                st.markdown("""
                    <div class="cantos-ornamento-dir"><span>❖</span><span>❖</span></div>
                    <div class="cabecalho-form-login">
                        <h2 class="titulo-login-direito">Login</h2>
                        <div class="divisor-asterisco">
                            <span class="linha"></span><span>✳</span><span class="linha"></span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                email_input = st.text_input("✉  E-MAIL CORPORATIVO", placeholder="seu.email@flor.com")
                senha_input = st.text_input("🔒  SENHA", placeholder="Digite sua senha", type="password")
                btn_entrar = st.form_submit_button("Entrar")

                st.markdown("""
                    <div class="rodape-esqueceu-senha">
                        Esqueceu a senha? <strong style="color: #CF4845;">Procure um administrador</strong> para<br>redefini-la.
                    </div>
                    <div class="cantos-ornamento-dir"><span>❖</span><span>❖</span></div>
                """, unsafe_allow_html=True)
                if btn_entrar:
                    usuario = autenticar_usuario(email_input, senha_input)
                    if usuario:
                        st.session_state.usuario_logado = usuario
                        setor_do_usuario = usuario["Setor"]
                        st.session_state.tela_atual = ESTRUTURA_SETORES[setor_do_usuario][0]
                        st.rerun()
                    else:
                        st.error("E-mail ou senha inválidos.")