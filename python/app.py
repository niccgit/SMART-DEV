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
