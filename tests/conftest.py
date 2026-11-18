import pytest

from app import create_app
from app.services import auth_service

EMAIL_TESTE = "voluntario@teste.org"
SENHA_TESTE = "senha-de-teste-123"


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db"), "SECRET_KEY": "teste"})
    with app.app_context():
        auth_service.criar_voluntario("Voluntário Teste", EMAIL_TESTE, SENHA_TESTE)
    return app


@pytest.fixture
def anonimo(app):
    """Cliente sem login."""
    return app.test_client()


@pytest.fixture
def client(app):
    """Cliente já autenticado como voluntário."""
    cliente = app.test_client()
    cliente.post("/login", data={"email": EMAIL_TESTE, "senha": SENHA_TESTE})
    return cliente
