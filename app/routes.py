"""Camada de apresentação: rotas e telas usadas pelos voluntários."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services import ValidacaoErro, familia_service

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


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
