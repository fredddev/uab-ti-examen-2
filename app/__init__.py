from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import config
import os


# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name=None):
    """
    Factory function para crear y configurar la aplicación Flask.
    
    Args:
        config_name (str): Nombre de la configuración ('development', 'production', 'testing').
                          Si no se especifica, se utiliza la variable de entorno FLASK_ENV.
    
    Returns:
        Flask: Aplicación Flask configurada.
    """
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Registrar blueprints
    register_blueprints(app)
    
    return app


def register_blueprints(app):
    """Registra todos los blueprints de la aplicación."""
    
    from app.auth import auth_bp
    from app.users import users_bp
    from app.tasks import tasks_bp
    from app.categories import categories_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(categories_bp)
