import streamlit as st
import re
import pandas as pd
import base64

st.set_page_config(page_title="Com carinho, Flor - Sistema", layout="wide")

def carregar_css(nome):
    with open(nome, "r", encoding="utf-8") as arquivo:
        st.markdown(f"<style>{arquivo.read()}</style>", unsafe_allow_html=True)

def carregar_imagem(caminho):
    with open(caminho, "rb") as imagem:
        return base64.b64encode(imagem.read()).decode()

logo = carregar_imagem("Logo Com carinho, Flor.jpg")

setores = {
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
        {"Nome": "Marcos (Montagem)", "CPF": "666.666.666-66", "Setor": "Montagem", "Email": "montagem@flor.com", "Senha": "Monta123"},
    ]

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = None

carregar_css("style.css")

if st.session_state.usuario_logado is None:
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
                        st.session_state.tela_atual = estrutura_setores[usuario["Setor"]][0]
                        st.rerun()
                    else:
                        st.error("E-mail ou senha inválidos.")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💡 Contas prontas para testar todos os 6 setores"):
            st.write("- **Administração:** `admin@flor.com` | Senha: `Admin123`")
            st.write("- **Financeiro:** `fin@flor.com` | Senha: `Finan123`")
            st.write("- **Atendimento:** `atend@flor.com` | Senha: `Atend123`")
            st.write("- **E-commerce:** `ecom@flor.com` | Senha: `Ecom1234`")
            st.write("- **Estoque:** `estoque@flor.com` | Senha: `Estoq123`")
            st.write("- **Montagem:** `montagem@flor.com` | Senha: `Monta123`")

else:
    usuario = st.session_state.usuario_logado
    setor_usuario = usuario["Setor"]

    with st.sidebar:
        st.title("Com carinho, Flor")
        st.write(f"**Usuário:** {usuario['Nome']}")
        st.write(f"**Setor:** {setor_usuario}")
        st.divider()

        if setor_usuario == "Administração":
            setores_permitidos = list(estrutura_setores.keys())
        else:
            setores_permitidos = [setor_usuario]

        for setor_menu in setores_permitidos:
            aberto = st.session_state.tela_atual in estrutura_setores[setor_menu]
            with st.expander(setor_menu.upper(), expanded=aberto):
                for pagina in estrutura_setores[setor_menu]:
                    tipo = "primary" if st.session_state.tela_atual == pagina else "secondary"
                    if st.button(pagina, key=f"nav_{pagina}", use_container_width=True, type=tipo):
                        st.session_state.tela_atual = pagina
                        st.rerun()

        st.divider()
        if st.button("Sair do Sistema", use_container_width=True):
            st.session_state.usuario_logado = None
            st.session_state.tela_atual = None
            st.rerun()

    tela = st.session_state.tela_atual

    if tela == "Cadastrar funcionário":
        st.header("Cadastrar funcionário")
        with st.form("form_cadastro", clear_on_submit=True):
            nome = st.text_input("NOME COMPLETO*")
            col1, col2 = st.columns(2)
            with col1:
                cpf = st.text_input("CPF*", max_chars=14, placeholder="000.000.000-00")
            with col2:
                setor_cad = st.selectbox("SETOR*", ["Selecione o setor"] + list(estrutura_setores.keys()))
            col3, col4 = st.columns(2)
            with col3:
                email = st.text_input("E-MAIL CORPORATIVO*")
            with col4:
                senha = st.text_input("SENHA*", type="password")
            st.caption("A senha deve ter de 8 a 16 caracteres, com no mínimo 1 minúscula, 1 maiúscula e 1 número.")

            if st.form_submit_button("Cadastrar"):
                nome = nome.strip()
                cpf = cpf.strip()
                email = email.strip()
                ok_senha, msg_senha = validar_senha(senha)

                if not nome or not cpf or setor_cad == "Selecione o setor" or not email or not senha:
                    st.error("Preencha todos os campos obrigatórios (*).")
                elif not validar_cpf(cpf):
                    st.error("CPF inválido. Use o formato 000.000.000-00.")
                elif not validar_email(email):
                    st.error("E-mail inválido.")
                elif any(f["Email"].lower() == email.lower() for f in st.session_state.funcionarios):
                    st.error("Já existe um funcionário com esse e-mail.")
                elif any(f["CPF"] == cpf for f in st.session_state.funcionarios):
                    st.error("Já existe um funcionário com esse CPF.")
                elif not ok_senha:
                    st.error(msg_senha)
                else:
                    st.session_state.funcionarios.append({
                        "Nome": nome, "CPF": cpf, "Setor": setor_cad, "Email": email, "Senha": senha
                    })
                    st.success("Funcionário cadastrado com sucesso!")

    elif tela == "Gerenciar usuários":
        st.header("Gerenciar usuários")
        df = pd.DataFrame(st.session_state.funcionarios).drop(columns=["Senha"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Remover funcionário")
        removiveis = [f["Email"] for f in st.session_state.funcionarios if f["Email"] != usuario["Email"]]
        if removiveis:
            email_remover = st.selectbox("Selecione o e-mail", removiveis)
            if st.button("Remover"):
                st.session_state.funcionarios = [
                    f for f in st.session_state.funcionarios if f["Email"] != email_remover
                ]
                st.success("Funcionário removido.")
                st.rerun()
        else:
            st.info("Não há outros funcionários para remover.")
    
    elif tela == "Movimentações":
        st.header("Movimentações")

    elif tela == "Pagamentos":
        st.header("Pagamentos")

    elif tela == "Cadastrar novo pedido":
        st.header("Cadastrar novo pedido")

    elif tela == "Consultar Pedidos":
        st.header("Consultar pedidos")

    elif tela == "Catálogo de produtos":
        st.header("Catálogo de produtos")

    elif tela == "Estoque":
        st.header("Visão de estoque")     

    elif tela == "Fila de montagem":
        st.header("Fila de montagem")
        col1, col2 = st.columns(2)

        with col1:
            st.button('Botão 1')

        with col2:
            st.button('Botão 2')
            
    else:
        st.header(tela)
        st.info("calma aí paizao, jaja os caba chega nas proximas telas")
