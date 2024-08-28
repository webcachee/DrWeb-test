from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    """
    Creates and configures a Flask application instance.

    This function initializes the Flask application with configuration settings, sets up
    the SQLAlchemy database connection, and initializes Flask-Migrate for database migrations.
    It also registers the main blueprint for handling routes.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
