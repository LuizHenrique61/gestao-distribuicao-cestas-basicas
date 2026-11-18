"""Camada de apresentação: rotas e telas usadas pelos voluntários."""
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.services import ValidacaoErro, auth_service, entrega_service, familia_service

bp = Blueprint("main", __name__)

ROTAS_PUBLICAS = {"main.login", "main.saude"}


# RNF01 - toda rota do sistema exige voluntário autenticado (verificado no servidor)
@bp.before_request
def exigir_login():
    if request.endpoint not in ROTAS_PUBLICAS and "id_voluntario" not in session:
        return redirect(url_for("main.login"))


# Monitoramento: verifica se a aplicação e o banco respondem
@bp.route("/saude")
def saude():
    try:
        entrega_service.quantidade_em_estoque()
        return {"status": "ok", "banco": "ok"}, 200
    except Exception:
        return {"status": "erro", "banco": "indisponivel"}, 503


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            voluntario = auth_service.autenticar(request.form.get("email"), request.form.get("senha"))
            session.clear()  # evita reaproveitar uma sessão anterior
            session.permanent = True
            session["id_voluntario"] = voluntario["id_voluntario"]
            session["nome_voluntario"] = voluntario["nome"]
            return redirect(url_for("main.index"))
        except ValidacaoErro as erro:
            flash(str(erro), "erro")
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("main.login"))


@bp.route("/")
def index():
    return render_template("index.html", estoque=entrega_service.quantidade_em_estoque())


# RF01 - cadastro de famílias
@bp.route("/familias")
def listar_familias():
    return render_template("familias.html", familias=familia_service.listar_familias(), titulo="Famílias cadastradas")


# RF05 - famílias aguardando atendimento
@bp.route("/familias/aguardando")
def familias_aguardando():
    return render_template(
        "familias.html",
        familias=familia_service.listar_familias(status="aguardando"),
        titulo="Famílias aguardando atendimento",
    )


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
    return render_template(
        "familia_detalhe.html",
        familia=familia,
        estoque=entrega_service.quantidade_em_estoque(),
        entregas=entrega_service.historico_da_familia(id_familia),  # RF04
    )


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
