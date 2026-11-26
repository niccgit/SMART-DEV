import streamlit as st
import banco
import estilo

st.set_page_config(
    page_title="Com carinho, Flor",
    layout="wide"
)

estilo.aplicar_estilo()
banco.criar_tabelas()

setores = [
    "Administração",
    "Financeiro",
    "Atendimento ao Cliente",
    "Gestão de E-commerce",
    "Estoque",
    "Montagem"
]

telas_por_setor = {

    "Administração": [
        "Cadastrar funcionário",
        "Gerenciar funcionários",
        "Movimentações",
        "Pagamentos",
        "Cadastrar pedido",
        "Consultar pedidos",
        "Catálogo de produtos",
        "Estoque",
        "Fila de montagem"
    ],

    "Financeiro": [
        "Movimentações",
        "Pagamentos"
    ],

    "Atendimento ao Cliente": [
        "Cadastrar pedido",
        "Consultar pedidos"
    ],

    "Gestão de E-commerce": [
        "Catálogo de produtos"
    ],

    "Estoque": [
        "Estoque"
    ],

    "Montagem": [
        "Fila de montagem"
    ]
}

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "tela" not in st.session_state:
    st.session_state.tela = None


def mostrar_login():

    st.title("Com carinho, Flor")
    st.subheader("Acesso ao sistema")
    with st.form("form_login"):
        email = st.text_input("E-mail corporativo")
        senha = st.text_input(
            "Senha",
            type="password"
        )
        entrar = st.form_submit_button("Entrar")

        if entrar:
            usuario = banco.buscar_usuario_login(
                email,
                senha
            )
            if usuario:
                st.session_state.usuario_logado = usuario
                setor = usuario["setor"]
                telas_permitidas = telas_por_setor.get(
                    setor,
                    []
                )

                if telas_permitidas:
                    st.session_state.tela = telas_permitidas[0]
                    st.rerun()
                else:
                    st.error("Setor sem telas cadastradas.")
            else:
                st.error("E-mail ou senha incorretos.")


def mostrar_menu(usuario, telas_permitidas):

    st.sidebar.title("Com carinho, Flor")
    st.sidebar.write(
        f"Olá, {usuario['nome_completo']}!"
    )
    st.sidebar.write(
        f"Setor: {usuario['setor']}"
    )
    st.sidebar.divider()
    indice = telas_permitidas.index(
        st.session_state.tela
    )

    tela_selecionada = st.sidebar.radio(
        "Menu",
        telas_permitidas,
        index=indice
    )

    st.session_state.tela = tela_selecionada
    st.sidebar.divider()
    if st.sidebar.button("Sair"):

        st.session_state.usuario_logado = None
        st.session_state.tela = None

        st.rerun()


def cadastrar_funcionario():

    st.title("Cadastrar funcionário")
    with st.form("form_cadastro_funcionario"):

        nome = st.text_input("Nome completo")
        cpf = st.text_input("CPF")
        setor = st.selectbox(
            "Setor",
            SETORES[1:] if False else SETORES
        )
        email = st.text_input("E-mail corporativo")
        senha = st.text_input(
            "Senha",
            type="password"
        )
        cadastrar = st.form_submit_button(
            "Cadastrar funcionário"
        )

        if cadastrar:
            sucesso, mensagem = banco.cadastrar_usuario(
                nome,
                cpf,
                setor,
                email,
                senha
            )
            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)


def gerenciar_funcionarios(usuario_logado):

    st.title("Gerenciar funcionários")

    usuarios = banco.listar_usuarios()

    if len(usuarios) == 0:
        st.info("Nenhum funcionário cadastrado.")
        return

    st.subheader("Funcionários cadastrados")
    st.dataframe(
        usuarios,
        use_container_width=True
    )

    opcoes_usuarios = {
        usuario["id"]: usuario["nome_completo"]
        for usuario in usuarios
    }

def abrir_tela(nome_tela, usuario):

    if nome_tela == "Cadastrar funcionário":
        cadastrar_funcionario()

    elif nome_tela == "Gerenciar funcionários":
        gerenciar_funcionarios(usuario)

    elif nome_tela == "Movimentações":
        from telas import financeiro
        financeiro.mostrar_movimentacoes()

    elif nome_tela == "Pagamentos":
        from telas import financeiro
        financeiro.mostrar_pagamentos()

    elif nome_tela == "Cadastrar pedido":
        from telas import atendimento
        atendimento.cadastrar_pedido()

    elif nome_tela == "Consultar pedidos":
        from telas import atendimento
        atendimento.consultar_pedidos()

    elif nome_tela == "Catálogo de produtos":
        from telas import ecommerce
        ecommerce.mostrar_catalogo()

    elif nome_tela == "Estoque":
        from telas import estoque
        estoque.mostrar_estoque()

    elif nome_tela == "Fila de montagem":
        from telas import montagem
        montagem.mostrar_fila()

    else:
        st.error("Tela não encontrada.")
