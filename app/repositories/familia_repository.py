"""Acesso aos dados da tabela familia (consultas parametrizadas)."""
from app.repositories.database import get_db


def inserir(nome_responsavel: str, quantidade_membros: int, telefone: str | None, endereco: str) -> int:
    cursor = get_db().execute(
        "INSERT INTO familia (nome_responsavel, quantidade_membros, telefone, endereco) "
        "VALUES (?, ?, ?, ?)",
        (nome_responsavel, quantidade_membros, telefone, endereco),
    )
    return cursor.lastrowid


def listar(status: str | None = None):
    sql = "SELECT * FROM familia"
    params: tuple = ()
    if status:
        sql += " WHERE status = ?"
        params = (status,)
    return get_db().execute(sql + " ORDER BY nome_responsavel", params).fetchall()


def buscar(id_familia: int):
    return get_db().execute("SELECT * FROM familia WHERE id_familia = ?", (id_familia,)).fetchone()


def atualizar_status(id_familia: int, status: str) -> None:
    get_db().execute("UPDATE familia SET status = ? WHERE id_familia = ?", (status, id_familia))
