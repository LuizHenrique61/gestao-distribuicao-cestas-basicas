"""Ponto de entrada da aplicação."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug desativado por padrão (RNF: não expor detalhes técnicos)
    app.run()
