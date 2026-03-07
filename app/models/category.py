"""
Modelo de Categoría de tareas.
"""

from app import db


class Category(db.Model):
    """
    Modelo para categorías de tareas.
    
    Atributos:
        id (int): ID único de la categoría
        name (str): Nombre de la categoría
        description (str): Descripción de la categoría
        user_id (int): FK al usuario propietario
        created_at (DateTime): Fecha de creación
    
    Relaciones:
        user: Usuario propietario de la categoría
        tasks: Todas las tareas en esta categoría
    """
    __tablename__ = 'categories'
    
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
