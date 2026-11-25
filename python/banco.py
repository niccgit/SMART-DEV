import sqlite3

DB_NAME = "floricultura.db"

def conectar():
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row

    return conexao

def criar_tabela_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        salt TEXT NOT NULL,
        senha_hash TEXT NOT NULL,
        tipo TEXT NOT NULL,
        trocar_senha INTEGER DEFAULT 0
    )
    """

    conexao.commit()
    conexao.close()
    
# tabela c os dados necessarios para os produtos cadastrados na floricultura

    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imagem TEXT NOT NULL,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        variacao TEXT NOT NULL,
        preco TEXT NOT NULL,
        situacao TEXT NOT NULL,
        estoque TEXT NOT NULL
    )
    """
    conexao.commit()
    conexao.close()