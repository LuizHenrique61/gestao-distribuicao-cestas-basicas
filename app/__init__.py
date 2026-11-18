"""Criação e configuração da aplicação Flask."""
import os

from flask import Flask


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-alterar-em-producao"),
        DATABASE=os.path.join(app.root_path, "..", "cestas.db"),
    )
    if config:
        app.config.update(config)

    from app.repositories import database
    database.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    return app
