"""Regras de negócio de entregas e estoque (RF02 e RF03)."""
from app.repositories import entrega_repository, estoque_repository, familia_repository
from app.repositories.database import get_db
from app.services import ValidacaoErro


def _inteiro_positivo(valor, campo: str) -> int:
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValidacaoErro(f"{campo} deve ser um número.")
    if numero <= 0:
        raise ValidacaoErro(f"{campo} deve ser maior que zero.")
    return numero


def registrar_entrega(id_familia: int, quantidade_cestas, observacao: str | None = None) -> int:
    """Registra a entrega, dá baixa no estoque e marca a família como atendida.

    Tudo acontece na mesma transação: se uma etapa falhar, nada é gravado.
    """
    quantidade_cestas = _inteiro_positivo(quantidade_cestas, "A quantidade de cestas")
    if familia_repository.buscar(id_familia) is None:
        raise ValidacaoErro("Família não encontrada.")

    disponivel = estoque_repository.obter_quantidade()
    if quantidade_cestas > disponivel:
        raise ValidacaoErro(f"Estoque insuficiente: há {disponivel} cesta(s) disponível(is).")

    db = get_db()
    try:
        id_entrega = entrega_repository.inserir(id_familia, quantidade_cestas, (observacao or "").strip() or None)
        estoque_repository.alterar_quantidade(-quantidade_cestas)
        familia_repository.atualizar_status(id_familia, "atendida")
        db.commit()
    except Exception:
        db.rollback()
        raise
    return id_entrega


def historico_da_familia(id_familia: int):
    """RF04: retorna somente as entregas vinculadas à família informada."""
    return entrega_repository.listar_por_familia(id_familia)


def adicionar_ao_estoque(quantidade) -> None:
    quantidade = _inteiro_positivo(quantidade, "A quantidade")
    estoque_repository.alterar_quantidade(quantidade)
    get_db().commit()


def quantidade_em_estoque() -> int:
    return estoque_repository.obter_quantidade()
