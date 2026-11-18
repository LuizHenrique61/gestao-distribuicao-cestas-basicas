"""Criação e configuração da aplicação Flask."""
import os
import secrets
from datetime import timedelta

import click
from flask import Flask


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(
        # Sem SECRET_KEY definida, gera uma chave aleatória a cada execução:
        # nunca usamos uma chave fixa publicada no repositório.
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
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
    _criar_voluntario_inicial(app)
    return app


def _criar_voluntario_inicial(app: Flask) -> None:
    """Em produção, cria o primeiro acesso a partir de variáveis de ambiente.

    Assim nenhuma senha fica gravada no código ou no repositório.
    """
    email = os.environ.get("VOLUNTARIO_EMAIL")
    senha = os.environ.get("VOLUNTARIO_SENHA")
    if not email or not senha or app.config.get("TESTING"):
        return
    from app.repositories import voluntario_repository
    from app.services import auth_service

    with app.app_context():
        if voluntario_repository.buscar_por_email(email.strip().lower()) is None:
            auth_service.criar_voluntario(os.environ.get("VOLUNTARIO_NOME", "Voluntário"), email, senha)


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
