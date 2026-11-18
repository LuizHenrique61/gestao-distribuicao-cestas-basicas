"""Acesso aos dados da tabela estoque (registro único id_estoque = 1)."""
from app.repositories.database import get_db


def obter_quantidade() -> int:
    linha = get_db().execute("SELECT quantidade_disponivel FROM estoque WHERE id_estoque = 1").fetchone()
    return linha["quantidade_disponivel"]


def alterar_quantidade(variacao: int) -> None:
    get_db().execute(
        "UPDATE estoque SET quantidade_disponivel = quantidade_disponivel + ?, "
        "data_atualizacao = DATE('now') WHERE id_estoque = 1",
        (variacao,),
    )
