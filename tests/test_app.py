import sqlite3


def test_pagina_inicial_carrega(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "Gestão de Cestas Básicas" in resposta.get_data(as_text=True)


def test_estoque_inicial_criado(app):
    con = sqlite3.connect(app.config["DATABASE"])
    qtd = con.execute("SELECT quantidade_disponivel FROM estoque WHERE id_estoque = 1").fetchone()
    assert qtd == (0,)


def test_rota_de_saude_e_publica_e_responde_ok(anonimo):
    resposta = anonimo.get("/saude")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"status": "ok", "banco": "ok"}


def test_voluntario_inicial_criado_por_variaveis_de_ambiente(tmp_path, monkeypatch):
    from app import create_app
    from app.repositories import voluntario_repository

    monkeypatch.setenv("VOLUNTARIO_EMAIL", "Admin@Remar.org")
    monkeypatch.setenv("VOLUNTARIO_SENHA", "senha-de-producao-123")
    app = create_app({"DATABASE": str(tmp_path / "prod.db"), "SECRET_KEY": "x"})
    with app.app_context():
        assert voluntario_repository.buscar_por_email("admin@remar.org") is not None
