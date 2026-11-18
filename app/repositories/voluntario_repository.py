"""Acesso aos dados da tabela voluntario (consultas parametrizadas)."""
from app.repositories.database import get_db


def inserir(nome: str, email: str, senha_hash: str) -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO voluntario (nome, email, senha_hash) VALUES (?, ?, ?)",
        (nome, email, senha_hash),
    )
    db.commit()
    return cursor.lastrowid


def buscar_por_email(email: str):
    return get_db().execute("SELECT * FROM voluntario WHERE email = ?", (email,)).fetchone()


def atualizar_hash(id_voluntario: int, senha_hash: str) -> None:
    db = get_db()
    db.execute("UPDATE voluntario SET senha_hash = ? WHERE id_voluntario = ?", (senha_hash, id_voluntario))
    db.commit()
