from app import create_app


def make_client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def test_pagina_inicial_carrega(tmp_path):
    resposta = make_client(tmp_path).get("/")
    assert resposta.status_code == 200
    assert "Gestão de Cestas Básicas" in resposta.get_data(as_text=True)


def test_estoque_inicial_criado(tmp_path):
    import sqlite3

    make_client(tmp_path)
    con = sqlite3.connect(tmp_path / "test.db")
    qtd = con.execute("SELECT quantidade_disponivel FROM estoque WHERE id_estoque = 1").fetchone()
    assert qtd == (0,)
