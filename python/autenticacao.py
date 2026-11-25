from banco import conectar

def criar_adm_inicial():
    conexao = conectar()

    total = conexao.execute(
        "SELECT COUNT(*) FROM usuarios"
    ).fetchone()[0]