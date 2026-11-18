"""Camada de apresentação: rotas e telas usadas pelos voluntários."""
from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


# Próximas rotas (implementação incremental):
# RF01 - /familias/nova        -> cadastrar família
# RF02 - /entregas/nova        -> registrar entrega
# RF03 - /estoque              -> consultar/atualizar estoque
# RF04 - /familias/<id>        -> histórico de entregas
# RF05 - /familias/aguardando  -> famílias aguardando atendimento
