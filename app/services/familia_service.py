"""Regras de negócio do cadastro de famílias (RF01)."""
from app.repositories import familia_repository
from app.repositories.database import transacao
from app.services import ValidacaoErro


def cadastrar_familia(nome_responsavel: str, quantidade_membros, telefone: str, endereco: str) -> int:
    nome_responsavel = (nome_responsavel or "").strip()
    endereco = (endereco or "").strip()
    telefone = (telefone or "").strip() or None

    if not nome_responsavel:
        raise ValidacaoErro("Informe o nome do responsável.")
    if not endereco:
        raise ValidacaoErro("Informe o endereço.")
    try:
        quantidade_membros = int(quantidade_membros)
    except (TypeError, ValueError):
        raise ValidacaoErro("A quantidade de membros deve ser um número.")
    if quantidade_membros <= 0:
        raise ValidacaoErro("A quantidade de membros deve ser maior que zero.")

    with transacao():
        return familia_repository.inserir(nome_responsavel, quantidade_membros, telefone, endereco)


def listar_familias(status: str | None = None):
    return familia_repository.listar(status)


def buscar_familia(id_familia: int):
    return familia_repository.buscar(id_familia)
