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
    executar("""
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            motivo TEXT,
            data TEXT NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)
    criar_root()

def criar_root():
    usuario = consultar(
        "SELECT * FROM usuarios WHERE email_corporativo = ?",
        (email_root,)
    )
    if len(usuario) == 0:
        executar("""
            INSERT INTO usuarios
            (nome_completo, cpf, setor, email_corporativo, senha, situacao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Root",
            "000.000.000-00",
            "Administração",
            email_root,
            criptografar_senha(senha_root),
            "Ativo"
        ))

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

def buscar_usuario_login(email, senha):
    senha = criptografar_senha(senha)
    usuario = consultar("""
        SELECT id, nome_completo, cpf, setor,
               email_corporativo, situacao
        FROM usuarios
        WHERE email_corporativo = ? COLLATE NOCASE
        AND senha = ?
        AND situacao = 'Ativo'
    """, (email.strip(), senha))
    if len(usuario) > 0:
        return usuario[0]
    return None

def listar_usuarios():
    usuarios = consultar("""
        SELECT id, nome_completo, cpf, setor,
               email_corporativo, situacao
        FROM usuarios
        ORDER BY id
    """)
    return usuarios

def cadastrar_usuario(nome, cpf, setor, email, senha):
    nome = nome.strip()
    cpf = cpf.strip()
    email = email.strip()
    if not nome or not cpf or not setor or not email or not senha:
        return False, "Preencha todos os campos."
    erro = validar_senha(senha)
    if erro:
        return False, erro
    cpf_existente = consultar(
        "SELECT id FROM usuarios WHERE cpf = ?",
        (cpf,)
    )
    if len(cpf_existente) > 0:
        return False, "Esse CPF já está cadastrado."
    email_existente = consultar(
        "SELECT id FROM usuarios WHERE email_corporativo = ?",
        (email,)
    )
    if len(email_existente) > 0:
        return False, "Esse e-mail já está cadastrado."
    executar("""
        INSERT INTO usuarios
        (nome_completo, cpf, setor, email_corporativo, senha, situacao)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nome,
        cpf,
        setor,
        email,
        criptografar_senha(senha),
        "Ativo"
    ))
    return True, "Funcionário cadastrado com sucesso!"

def atualizar_usuario(id_usuario, nome, setor, situacao, nova_senha=""):
    if not nome.strip():
        return False, "O nome não pode ficar vazio."
    if nova_senha:
        erro = validar_senha(nova_senha)
        if erro:
            return False, erro
    executar("""
        UPDATE usuarios
        SET nome_completo = ?,
            setor = ?,
            situacao = ?
        WHERE id = ?
    """, (nome.strip(), setor, situacao, id_usuario))
    if nova_senha:
        executar("""
            UPDATE usuarios
            SET senha = ?
            WHERE id = ?
        """, (criptografar_senha(nova_senha), id_usuario))
    return True, "Funcionário atualizado com sucesso!"


def listar_pedidos_montagem():
    return consultar("""
        SELECT *
        FROM pedidos
        ORDER BY id
    """)

def atualizar_status_pedido(id_pedido, novo_status):
    status_permitidos = [
        "Pendente",
        "Em progresso",
        "Finalizado"
    ]
    if novo_status not in status_permitidos:
        return False, "Status inválido."
    pedido = consultar(
        "SELECT id FROM pedidos WHERE id = ?",
        (id_pedido,)
    )
    if not pedido:
        return False, "Pedido não encontrado."
    executar("""
        UPDATE pedidos
        SET status = ?
        WHERE id = ?
    """, (novo_status, id_pedido))
    return True, "Status do pedido atualizado com sucesso!"


def listar_estoque():
    produtos = consultar("""
        SELECT id, nome, tipo, quantidade, estoque_minimo
        FROM produtos
        WHERE situacao = 'Ativo'
        ORDER BY nome
    """)
    resultado = []
    for produto in produtos:
        quantidade = produto["quantidade"]
        minimo = produto["estoque_minimo"]
        if quantidade <= 0:
            situacao = "Zerado"
        elif quantidade <= minimo:
            situacao = "Baixo"
        else:
            situacao = "Normal"
        resultado.append({
            "id": produto["id"],
            "produto": produto["nome"],
            "tipo": produto["tipo"],
            "quantidade": quantidade,
            "situacao": situacao
        })
    return resultado

def listar_produtos_estoque():
    return consultar("""
        SELECT id, nome
        FROM produtos
        WHERE situacao = 'Ativo'
        ORDER BY nome
    """)

def registrar_entrada_estoque(id_produto, quantidade):
    if quantidade <= 0:
        return False, "Informe uma quantidade maior que zero."
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id
        FROM produtos
        WHERE id = ? AND situacao = 'Ativo'
    """, (id_produto,))
    produto = cursor.fetchone()
    if produto is None:
        conexao.close()
        return False, "Produto não encontrado ou inativo."
    cursor.execute("""
        UPDATE produtos
        SET quantidade = quantidade + ?
        WHERE id = ?
    """, (quantidade, id_produto))
    cursor.execute("""
        INSERT INTO movimentacoes_estoque
        (produto_id, tipo, quantidade, motivo, data)
        VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
    """, (id_produto, "Entrada", quantidade, "Reposição"))
    conexao.commit()
    conexao.close()
    return True, "Entrada registrada com sucesso."

def registrar_saida_estoque(id_produto, quantidade, motivo):
    if quantidade <= 0:
        return False, "Informe uma quantidade maior que zero."
    if not motivo:
        return False, "Selecione o motivo da saída."
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT quantidade
        FROM produtos
        WHERE id = ? AND situacao = 'Ativo'
    """, (id_produto,))
    produto = cursor.fetchone()
    if produto is None:
        conexao.close()
        return False, "Produto não encontrado ou inativo."
    if quantidade > produto["quantidade"]:
        conexao.close()
        return False, "A quantidade de saída é maior que o estoque disponível."
    cursor.execute("""
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
    """, (quantidade, id_produto))
    cursor.execute("""
        INSERT INTO movimentacoes_estoque
        (produto_id, tipo, quantidade, motivo, data)
        VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
    """, (id_produto, "Saída", quantidade, motivo))
    conexao.commit()
    conexao.close()
    return True, "Saída registrada com sucesso."

