"""Testes das regras de negócio: cadastro (RF01), entrega e estoque (RF02/RF03),
histórico (RF04), famílias aguardando (RF05) e segurança das entradas."""
import pytest

from app.services import ValidacaoErro, entrega_service, familia_service


def cadastrar(nome="João Silva", membros=4, endereco="Rua A, 10"):
    return familia_service.cadastrar_familia(nome, membros, "", endereco)


# RF01
def test_cadastro_valido_gera_identificador(app):
    with app.app_context():
        id_familia = cadastrar()
        familia = familia_service.buscar_familia(id_familia)
        assert familia["nome_responsavel"] == "João Silva"
        assert familia["status"] == "aguardando"


@pytest.mark.parametrize("nome, membros, endereco", [
    ("", 4, "Rua A"),        # sem responsável
    ("João", 4, ""),         # sem endereço
    ("João", 0, "Rua A"),    # membros zero
    ("João", "abc", "Rua A"),  # membros não numérico
])
def test_cadastro_invalido_e_rejeitado(app, nome, membros, endereco):
    with app.app_context():
        with pytest.raises(ValidacaoErro):
            familia_service.cadastrar_familia(nome, membros, "", endereco)
        assert familia_service.listar_familias() == []


# RF02 / RF03
def test_entrega_reduz_estoque_e_marca_familia_atendida(app):
    with app.app_context():
        id_familia = cadastrar()
        entrega_service.adicionar_ao_estoque(5)
        entrega_service.registrar_entrega(id_familia, 2)
        assert entrega_service.quantidade_em_estoque() == 3
        assert familia_service.buscar_familia(id_familia)["status"] == "atendida"


def test_entrega_bloqueada_com_estoque_insuficiente(app):
    with app.app_context():
        id_familia = cadastrar()
        entrega_service.adicionar_ao_estoque(1)
        with pytest.raises(ValidacaoErro, match="Estoque insuficiente"):
            entrega_service.registrar_entrega(id_familia, 2)
        assert entrega_service.quantidade_em_estoque() == 1
        assert entrega_service.historico_da_familia(id_familia) == []


def test_entrega_para_familia_inexistente_e_rejeitada(app):
    with app.app_context():
        entrega_service.adicionar_ao_estoque(5)
        with pytest.raises(ValidacaoErro, match="Família não encontrada"):
            entrega_service.registrar_entrega(999, 1)


# RF04
def test_historico_mostra_apenas_entregas_da_familia(app):
    with app.app_context():
        joao = cadastrar("João")
        maria = cadastrar("Maria")
        entrega_service.adicionar_ao_estoque(5)
        entrega_service.registrar_entrega(joao, 1)
        entrega_service.registrar_entrega(joao, 1)
        entrega_service.registrar_entrega(maria, 1)
        assert len(entrega_service.historico_da_familia(joao)) == 2
        assert len(entrega_service.historico_da_familia(maria)) == 1


# RF05
def test_lista_aguardando_exclui_familias_atendidas(app):
    with app.app_context():
        joao = cadastrar("João")
        cadastrar("Maria")
        entrega_service.adicionar_ao_estoque(1)
        entrega_service.registrar_entrega(joao, 1)
        nomes = [f["nome_responsavel"] for f in familia_service.listar_familias("aguardando")]
        assert nomes == ["Maria"]


# Segurança (RNF02): entradas tratadas como dados
def test_entrada_com_sql_e_html_e_armazenada_como_texto(client, app):
    nome = "Robert'); DROP TABLE familia;-- <script>alert(1)</script>"
    client.post("/familias/nova", data={"nome_responsavel": nome, "quantidade_membros": "1", "endereco": "Rua A"})
    with app.app_context():
        assert familia_service.listar_familias()[0]["nome_responsavel"] == nome
    pagina = client.get("/familias").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in pagina
    assert "&lt;script&gt;" in pagina


# Transação: se uma etapa da entrega falhar, nada é gravado
def test_falha_no_meio_da_entrega_desfaz_tudo(app, monkeypatch):
    from app.repositories import familia_repository

    with app.app_context():
        id_familia = cadastrar()
        entrega_service.adicionar_ao_estoque(5)

        def falhar(*_args):
            raise RuntimeError("falha simulada")

        monkeypatch.setattr(familia_repository, "atualizar_status", falhar)
        with pytest.raises(RuntimeError):
            entrega_service.registrar_entrega(id_familia, 2)

        assert entrega_service.quantidade_em_estoque() == 5
        assert entrega_service.historico_da_familia(id_familia) == []
