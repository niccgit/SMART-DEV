import bcrypt
from banco import conectar

def criar_adm_inicial():
    conexao = conectar()
    total = conexao.execute(
        "SELECT COUNT(*) FROM usuarios"
    ).fetchone()[0]

# if total > 0:
#    conexao.close()
#    return

nome = "Administrador"
email = "root@gmail.com"
senha = "1234"
tipo = "admin"

salt = bcrypt.gensalt()

senha_hash = bcrypt.hashpw(
    senha.encode("utf-8"),
    salt
)

