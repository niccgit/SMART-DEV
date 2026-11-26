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
