from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.config import config
import os


# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


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
    
    # Determinar la ruta del directorio raíz del proyecto
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_folder = os.path.join(root_path, 'templates')
    
    app = Flask(__name__, template_folder=template_folder)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar user_loader para Flask-Login
    setup_user_loader(app)
    
    return app


def setup_user_loader(app):
    """Configura el user_loader callback para Flask-Login."""
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Carga un usuario por su ID."""
        return User.query.get(int(user_id))


def register_blueprints(app):
    """Registra todos los blueprints de la aplicación."""
    
    from app.auth import auth_bp
    from app.users import users_bp
    from app.tasks import tasks_bp
    from app.categories import categories_bp
    from app.chatbot import chatbot_bp
    from app.dashboard import dashboard_bp
    from flask import redirect, url_for
    from flask_login import current_user, login_required
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(dashboard_bp)
    
    # Ruta raíz que redirige al login o al dashboard
    @app.route('/')
    def index():
        """Ruta raíz que redirige al login si no está autenticado, o al dashboard si lo está."""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('auth.login'))
    
    # Ruta dashboard protegida
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """
        Panel de control protegido del usuario.
        Requiere autenticación via @login_required decorator.
        Redirige automáticamente al login si el usuario no está autenticado.
        """
        return redirect(url_for('dashboard.dashboard'))
