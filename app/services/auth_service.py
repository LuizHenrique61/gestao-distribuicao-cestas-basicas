"""Regras de autenticação dos voluntários (RNF01).

Senhas nunca são armazenadas em texto limpo: guardamos apenas o hash Argon2id
(com salt aleatório embutido), gerado pela biblioteca argon2-cffi.
Hash é uma função de mão única: não existe "descriptografar" a senha.
"""
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from app.repositories import voluntario_repository
from app.repositories.database import transacao
from app.services import ValidacaoErro

_hasher = PasswordHasher()  # Argon2id com parâmetros recomendados pela biblioteca

TAMANHO_MINIMO_SENHA = 8
MENSAGEM_LOGIN_INVALIDO = "E-mail ou senha incorretos."


def _normalizar_email(email: str) -> str:
    return (email or "").strip().lower()


def criar_voluntario(nome: str, email: str, senha: str) -> int:
    nome = (nome or "").strip()
    email = _normalizar_email(email)
    if not nome or "@" not in email:
        raise ValidacaoErro("Informe nome e e-mail válidos.")
    if len(senha or "") < TAMANHO_MINIMO_SENHA:
        raise ValidacaoErro(f"A senha deve ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres.")
    if voluntario_repository.buscar_por_email(email) is not None:
        raise ValidacaoErro("Já existe um voluntário com este e-mail.")
    with transacao():
        return voluntario_repository.inserir(nome, email, _hasher.hash(senha))


def autenticar(email: str, senha: str):
    """Retorna o voluntário se e-mail e senha conferirem; caso contrário, lança ValidacaoErro.

    A mensagem é a mesma para e-mail inexistente e senha errada, para não
    revelar quais e-mails estão cadastrados.
    """
    voluntario = voluntario_repository.buscar_por_email(_normalizar_email(email))
    if voluntario is None:
        raise ValidacaoErro(MENSAGEM_LOGIN_INVALIDO)
    try:
        _hasher.verify(voluntario["senha_hash"], senha or "")
    except (VerificationError, InvalidHashError):
        raise ValidacaoErro(MENSAGEM_LOGIN_INVALIDO)

    if _hasher.check_needs_rehash(voluntario["senha_hash"]):
        with transacao():
            voluntario_repository.atualizar_hash(voluntario["id_voluntario"], _hasher.hash(senha))
    return voluntario
