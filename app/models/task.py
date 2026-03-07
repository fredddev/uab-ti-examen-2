"""
Modelo de Tarea.
"""

from app import db


class Task(db.Model):
    """
    Modelo para tareas.
    
    Atributos:
        id (int): ID único de la tarea
        title (str): Título de la tarea
        description (str): Descripción detallada
        status (str): Estado de la tarea (pendiente, en_progreso, completado)
        user_id (int): FK al usuario propietario
        category_id (int): FK a la categoría (opcional)
        created_at (DateTime): Fecha de creación
        updated_at (DateTime): Fecha de última actualización
    
    Relaciones:
        user: Usuario propietario de la tarea
        category: Categoría de la tarea
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(
        db.String(20), 
        default='pendiente', 
        nullable=False
    )  # pendiente, en_progreso, completado
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    
    def __repr__(self):
        return f'<Task {self.title}>'
