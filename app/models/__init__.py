"""
Módulo de modelos de la aplicación.
Contiene todas las definiciones de modelos de base de datos para MySQL.

Importar en otros archivos:
    from app import db
    from app.models import User, Category, Task
"""

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .category import Category
from .task import Task


class User(UserMixin, db.Model):
    """
    Modelo para usuarios de la aplicación.
    Compatible con Flask-Login.
    
    Atributos:
        id (int): ID único del usuario
        username (str): Nombre de usuario único
        email (str): Email único del usuario
        password_hash (str): Contraseña hasheada con werkzeug.security
        role (str): Rol del usuario ('admin' o 'user'). Default: 'user'
        created_at (DateTime): Fecha de creación
        updated_at (DateTime): Fecha de última actualización
    
    Relaciones:
        tasks: Todas las tareas del usuario
        categories: Todas las categorías del usuario
    
    Métodos:
        set_password(password): Hashea y asigna la contraseña
        check_password(password): Verifica si la contraseña es correcta
    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin' o 'user'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    
    # Relaciones
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    
    __all__ = ['User']
    
    def set_password(self, password):
        """
        Hashea y asigna la contraseña del usuario.
        
        Args:
            password (str): Contraseña en texto plano
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con la hasheada.
        
        Args:
            password (str): Contraseña en texto plano a verificar
            
        Returns:
            bool: True si la contraseña es correcta, False en caso contrario
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
