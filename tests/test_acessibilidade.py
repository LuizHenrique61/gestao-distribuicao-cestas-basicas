"""Testes dos recursos de acessibilidade presentes em todas as telas."""
import pytest


@pytest.mark.parametrize("rota", ["/", "/familias", "/familias/nova", "/estoque"])
def test_telas_tem_link_pular_e_barra_de_acessibilidade(client, rota):
    html = client.get(rota).get_data(as_text=True)
    assert 'href="#conteudo"' in html
    assert 'id="conteudo"' in html
    assert 'data-a11y="contraste"' in html
    assert 'data-a11y="fonte"' in html
    assert 'aria-pressed="false"' in html


def test_tela_de_login_tambem_e_acessivel(anonimo):
    html = anonimo.get("/login").get_data(as_text=True)
    assert 'lang="pt-BR"' in html
    assert 'href="#conteudo"' in html
    assert '<label for="email">' in html and '<label for="senha">' in html


def test_mensagens_sao_anunciadas_por_leitor_de_tela(client):
    resposta = client.post("/familias/nova", data={"nome_responsavel": "", "quantidade_membros": "1", "endereco": "X"})
    html = resposta.get_data(as_text=True)
    assert 'aria-live="polite"' in html
    assert 'role="alert"' in html


def test_script_de_acessibilidade_e_servido(client):
    resposta = client.get("/static/js/acessibilidade.js")
    assert resposta.status_code == 200
    assert b"aria-pressed" in resposta.data
