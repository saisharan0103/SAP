from flask import Flask
from data.db import run_migrations
from integration.routes import bp as api_bp


def create_app() -> Flask:
    run_migrations()
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
