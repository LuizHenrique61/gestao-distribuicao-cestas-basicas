"""Testes do RNF01: autenticação, hash de senha e proteção das rotas."""
import sqlite3

import pytest

from app.services import ValidacaoErro, auth_service
from tests.conftest import EMAIL_TESTE, SENHA_TESTE


def test_senha_nao_e_armazenada_em_texto_limpo(app):
    con = sqlite3.connect(app.config["DATABASE"])
    senha_hash = con.execute("SELECT senha_hash FROM voluntario WHERE email = ?", (EMAIL_TESTE,)).fetchone()[0]
    assert SENHA_TESTE not in senha_hash
    assert senha_hash.startswith("$argon2id$")


def test_login_valido_libera_acesso(anonimo):
    resposta = anonimo.post("/login", data={"email": EMAIL_TESTE, "senha": SENHA_TESTE})
    assert resposta.status_code == 302
    assert anonimo.get("/").status_code == 200


def test_login_com_senha_errada_e_negado(anonimo):
    resposta = anonimo.post("/login", data={"email": EMAIL_TESTE, "senha": "errada"})
    assert "E-mail ou senha incorretos." in resposta.get_data(as_text=True)
    assert anonimo.get("/").status_code == 302


def test_mensagem_igual_para_email_inexistente(anonimo):
    resposta = anonimo.post("/login", data={"email": "nao@existe.org", "senha": "qualquer"})
    assert "E-mail ou senha incorretos." in resposta.get_data(as_text=True)


@pytest.mark.parametrize("rota", ["/", "/familias", "/familias/nova", "/familias/aguardando", "/estoque"])
def test_rotas_protegidas_redirecionam_para_login(anonimo, rota):
    resposta = anonimo.get(rota)
    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/login")


def test_operacao_sem_login_nao_grava_dados(anonimo, app):
    anonimo.post("/familias/nova", data={"nome_responsavel": "Invasor", "quantidade_membros": "1", "endereco": "X"})
    con = sqlite3.connect(app.config["DATABASE"])
    assert con.execute("SELECT COUNT(*) FROM familia").fetchone()[0] == 0


def test_logout_encerra_a_sessao(client):
    assert client.get("/").status_code == 200
    client.post("/logout")
    assert client.get("/").status_code == 302


def test_senha_curta_e_email_duplicado_sao_rejeitados(app):
    with app.app_context():
        with pytest.raises(ValidacaoErro, match="pelo menos 8"):
            auth_service.criar_voluntario("Ana", "ana@teste.org", "123")
        with pytest.raises(ValidacaoErro, match="Já existe"):
            auth_service.criar_voluntario("Outro", EMAIL_TESTE.upper(), "senha-longa-123")
