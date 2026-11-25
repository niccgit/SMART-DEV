import bcrypt
from banco import conectar

def criar_adm_inicial():
    conexao = conectar()
    total = conexao.execute(
        "SELECT COUNT(*) FROM usuarios"
    ).fetchone()[0]

if total > 0:
    conexao.close()
    return

nome = "Administrador"
email = "root@gmail.com"
senha = "1234"
tipo = "admin"

salt = bcrypt.gensalt()

senha_hash = bcrypt.hashpw(
    senha.encode("utf-8"),
    salt
)

conexao.execute("""  
    INSERT INTO usuarios
    (nome, email, salt, senha_hash, tipo, trocar_senha)
    VALUES(?,?,?,?,?,?)
    """,(
        nome,
        email,
        salt.decode,
        senha_hash.decode,
        tipo
))

conexao.commit()
conexao.close()

def verificar_login():
    conexao = conectar()
    usuario = conexao.execute("""
    SELECT * FROM usuarios WHERE email = ?
    """,(email)).fetchone()

    if usuario is None:
        conexao.close()
        return None
    
    salt = usuario["salt"].encode("utf-8")
    senha_hash = usuario["senha_hash"].encode("utf-8")
    senha_digitada = senha.encode("utf-8")
    senha_correta = bcrypt.checkpw(
        senha_digitada,
        senha_hash
    )

    if not senha_correta:
        conexao.close()
        return None
    
    dados_usuarios = {
        "id": usuario['id'],
        "nome": usuario['nome'],
        "email": usuario['email'],
        "trocar_senha": usuario['trocar_senha']
    }

    conexao.close()

    return dados_usuarios
