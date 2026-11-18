"""Criação e configuração da aplicação Flask."""
import os
from datetime import timedelta

import click
from flask import Flask


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-alterar-em-producao"),
        DATABASE=os.path.join(app.root_path, "..", "cestas.db"),
        # RNF01: sessão expira após 30 minutos de inatividade
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
        SESSION_REFRESH_EACH_REQUEST=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE", "0") == "1",
    )
    if config:
        app.config.update(config)

    from app.repositories import database
    database.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    _registrar_comandos(app)
    return app


def _registrar_comandos(app: Flask) -> None:
    @app.cli.command("criar-voluntario")
    @click.option("--nome", prompt="Nome do voluntário")
    @click.option("--email", prompt="E-mail")
    @click.password_option(prompt="Senha")
    def criar_voluntario(nome, email, password):
        """Cria um voluntário com acesso ao sistema."""
        from app.services import ValidacaoErro, auth_service

        try:
            auth_service.criar_voluntario(nome, email, password)
            click.echo("Voluntário criado com sucesso.")
        except ValidacaoErro as erro:
            raise click.ClickException(str(erro))
