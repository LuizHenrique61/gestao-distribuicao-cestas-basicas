"""Camada de apresentação: rotas e telas usadas pelos voluntários."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.services import ValidacaoErro, entrega_service, familia_service

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html", estoque=entrega_service.quantidade_em_estoque())


# RF01 - cadastro de famílias
@bp.route("/familias")
def listar_familias():
    return render_template("familias.html", familias=familia_service.listar_familias(), titulo="Famílias cadastradas")


@bp.route("/familias/nova", methods=["GET", "POST"])
def nova_familia():
    if request.method == "POST":
        try:
            familia_service.cadastrar_familia(
                request.form.get("nome_responsavel"),
                request.form.get("quantidade_membros"),
                request.form.get("telefone"),
                request.form.get("endereco"),
            )
            flash("Família cadastrada com sucesso.", "sucesso")
            return redirect(url_for("main.listar_familias"))
        except ValidacaoErro as erro:
            flash(str(erro), "erro")
    return render_template("familia_form.html", dados=request.form)


@bp.route("/familias/<int:id_familia>")
def detalhe_familia(id_familia):
    familia = familia_service.buscar_familia(id_familia)
    if familia is None:
        abort(404)
    return render_template("familia_detalhe.html", familia=familia, estoque=entrega_service.quantidade_em_estoque())


# RF02 e RF03 - registro de entrega com baixa no estoque
@bp.route("/familias/<int:id_familia>/entregas", methods=["POST"])
def registrar_entrega(id_familia):
    try:
        entrega_service.registrar_entrega(id_familia, request.form.get("quantidade_cestas"), request.form.get("observacao"))
        flash("Entrega registrada e estoque atualizado.", "sucesso")
    except ValidacaoErro as erro:
        flash(str(erro), "erro")
    return redirect(url_for("main.detalhe_familia", id_familia=id_familia))


@bp.route("/estoque", methods=["GET", "POST"])
def estoque():
    if request.method == "POST":
        try:
            entrega_service.adicionar_ao_estoque(request.form.get("quantidade"))
            flash("Entrada de cestas registrada.", "sucesso")
            return redirect(url_for("main.estoque"))
        except ValidacaoErro as erro:
            flash(str(erro), "erro")
    return render_template("estoque.html", quantidade=entrega_service.quantidade_em_estoque())
