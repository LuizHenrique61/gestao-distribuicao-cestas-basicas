"""Acesso aos dados da tabela entrega (consultas parametrizadas)."""
from app.repositories.database import get_db


def inserir(id_familia: int, quantidade_cestas: int, observacao: str | None) -> int:
    cursor = get_db().execute(
        "INSERT INTO entrega (id_familia, quantidade_cestas, observacao) VALUES (?, ?, ?)",
        (id_familia, quantidade_cestas, observacao),
    )
    return cursor.lastrowid


def listar_por_familia(id_familia: int):
    return get_db().execute(
        "SELECT * FROM entrega WHERE id_familia = ? ORDER BY data_entrega DESC, id_entrega DESC",
        (id_familia,),
    ).fetchall()
