import sqlite3


def test_pagina_inicial_carrega(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "Gestão de Cestas Básicas" in resposta.get_data(as_text=True)


def test_estoque_inicial_criado(app):
    con = sqlite3.connect(app.config["DATABASE"])
    qtd = con.execute("SELECT quantidade_disponivel FROM estoque WHERE id_estoque = 1").fetchone()
    assert qtd == (0,)
