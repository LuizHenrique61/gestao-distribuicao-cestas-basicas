"""Conexão com o SQLite e criação das tabelas."""
import os
import sqlite3

from flask import Flask, current_app, g

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database", "schema.sql")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def transacao():
    """Gerenciador de contexto: confirma tudo ao final ou desfaz se houver erro.

    Uso nos serviços:
        with transacao():
            repositorio.inserir(...)
    """
    return get_db()


def init_db() -> None:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        get_db().executescript(f.read())


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
