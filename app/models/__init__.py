"""
Módulo de modelos de la aplicación.
Contiene todas las definiciones de modelos de base de datos.
"""

from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """Modelo para usuarios de la aplicación."""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relaciones
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Modelo para categorías de tareas."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relaciones
    tasks = db.relationship('Task', backref='category', lazy=True)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='uq_user_category_name'),)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Task(db.Model):
    """Modelo para tareas."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Task {self.title}>'
