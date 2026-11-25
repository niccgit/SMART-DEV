
import sqlite3
import hashlib

DB_NAME = "floricultura.db"

email_root = "root@email.com"
senha_root = "1234"


def conectar():
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row
    return conexao

def consultar(sql, parametros=()):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    resultado = cursor.fetchall()
    conexao.close()
    return [dict(linha) for linha in resultado]

def executar(sql, parametros=()):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    conexao.commit()
    conexao.close()

def criptografar_senha(senha):
    senha = hashlib.sha256(
        senha.encode("utf-8")
    ).hexdigest()
    return senha

def criar_tabelas():

    executar("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            setor TEXT NOT NULL,
            email_corporativo TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            situacao TEXT NOT NULL DEFAULT 'Ativo'
        )
    """)

    executar("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL
        )
    """)

    executar("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario TEXT NOT NULL,
            setor TEXT NOT NULL,
            mes_referencia TEXT NOT NULL,
            valor REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente'
        )
    """)

    executar("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            anonimo INTEGER NOT NULL DEFAULT 0,
            variacao_buque TEXT NOT NULL,
            qtd_itens INTEGER NOT NULL,
            variacao_acessorio TEXT NOT NULL,
            valor_total REAL NOT NULL,
            mensagem_cartao TEXT NOT NULL,
            frete_total REAL NOT NULL,
            endereco_entrega TEXT NOT NULL,
            entrega_agendada INTEGER NOT NULL DEFAULT 0,
            data_hora_entrega TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente'
        )
    """)

    executar("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nome TEXT NOT NULL,
            variacao TEXT NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT NOT NULL,
            imagem TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            estoque_minimo INTEGER NOT NULL DEFAULT 5,
            situacao TEXT NOT NULL DEFAULT 'Ativo'
        )
    """)