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

""")

    criar_root()
def criar_root():

    usuario = consultar(
        "SELECT * FROM usuarios WHERE email_corporativo = ?",
        (email_root,)
    )

    if len(usuario) == 0:
        executar(
            """
            INSERT INTO usuarios
            (nome_completo, cpf, setor, email_corporativo, senha, situacao)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Root",
                "000.000.000-00",
                "Administração",
                email_root,
                criptografar_senha(senha_root),
                "Ativo"
            )
        )

def validar_senha(senha):

    if len(senha) < 8 or len(senha) > 14:
        return "A senha deve ter de 8 a 14 caracteres."

    if not any(letra.isupper() for letra in senha):
        return "A senha precisa de no mínimo uma letra maiúscula."

    if not any(letra.islower() for letra in senha):
        return "A senha precisa de no mínimo uma letra minúscula."

    if not any(numero.isdigit() for numero in senha):
        return "A senha precisa de no mínimo um número."

    return None

def buscar_usuarios(email, senha):

    senha = criptografar_senha(senha)
    usuario = consultar(
        """
        SELECT id, nome_completo, cpf, setor,
               email_corporativo, situacao
        FROM usuarios
        WHERE email_corporativo = ? COLLATE NOCASE
        AND senha = ?
        AND situacao = 'Ativo'
        """,
        (email.strip(), senha)
    )
    if len(usuario) > 0:
        return usuario[0]
    return None

def listar_usuarios():

    usuarios = consultar(
        """
        SELECT id, nome_completo, cpf, setor,
               email_corporativo, situacao
        FROM usuarios
        ORDER BY id
        """
    )
    return usuarios