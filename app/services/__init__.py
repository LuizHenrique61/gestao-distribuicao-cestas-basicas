"""Camada de aplicação: regras de negócio do MVP."""


class ValidacaoErro(Exception):
    """Erro de regra de negócio, exibido ao voluntário como mensagem amigável."""
