"""
Ejemplo completo de Blueprint con CRUD para Tareas

Este archivo muestra cómo implementar un blueprint funcional con
operaciones CRUD utilizando Flask-SQLAlchemy.

Para usar: Reemplazar el contenido de app/tasks/__init__.py
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, User, Category
from datetime import datetime

# Crear blueprint
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


# ============================================================================
# RUTAS GET - Lectura
# ============================================================================

@tasks_bp.route('/', methods=['GET'])
def list_tasks():
    """
    Lista todas las tareas del usuario.
    
    Query params:
        - completed: true/false para filtrar por estado
        - priority: low, medium, high
        - sort: created_at (desc), due_date, priority
    
    Returns:
        {
            "count": 5,
            "tasks": [
                {
                    "id": 1,
                    "title": "Comprar leche",
                    "priority": "high",
                    "completed": false,
                    "category": "Compras"
                }
            ]
        }
    """
    # Obtener parámetros (en producción usar Flask-Login para usuario real)
    user_id = request.args.get('user_id', 1, type=int)
    completed = request.args.get('completed', type=str)
    priority = request.args.get('priority', type=str)
    sort_by = request.args.get('sort', 'created_at', type=str)
    
    # Construir query
    query = Task.query.filter_by(user_id=user_id)
    
    # Aplicar filtros
    if completed is not None:
        completed_bool = completed.lower() == 'true'
        query = query.filter_by(completed=completed_bool)
    
    if priority:
        query = query.filter_by(priority=priority)
    
    # Ordenar
    if sort_by == 'due_date':
        query = query.order_by(Task.due_date)
    elif sort_by == 'priority':
        query = query.order_by(Task.priority)
    else:
        query = query.order_by(Task.created_at.desc())
    
    # Ejecutar query
    tasks = query.all()
    
    return jsonify({
        'count': len(tasks),
        'tasks': [
            {
                'id': t.id,
                'title': t.title,
                'description': t.description,
                'priority': t.priority,
                'completed': t.completed,
                'due_date': t.due_date.isoformat() if t.due_date else None,
                'category': t.category.name if t.category else None,
                'created_at': t.created_at.isoformat()
            }
            for t in tasks
        ]
    }), 200


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Obtiene una tarea específica.
    
    Args:
        task_id: ID de la tarea
    
    Returns:
        {
            "id": 1,
            "title": "Comprar leche",
            "description": "Ir al supermercado",
            "priority": "medium",
            "completed": false,
            "due_date": "2025-03-15T18:00:00",
            "category": "Compras",
            "user_id": 1,
            "created_at": "2025-03-07T10:30:00",
            "updated_at": "2025-03-07T10:30:00"
        }
    """
    task = Task.query.get_or_404(task_id)
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'completed': task.completed,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'category': task.category.name if task.category else None,
        'user_id': task.user_id,
        'created_at': task.created_at.isoformat(),
        'updated_at': task.updated_at.isoformat()
    }), 200


# ============================================================================
# RUTAS POST - Creación
# ============================================================================

@tasks_bp.route('/create', methods=['POST'])
def create_task():
    """
    Crea una nueva tarea.
    
    Body (JSON):
        {
            "title": "Comprar leche",
            "description": "Ir al supermercado",
            "priority": "medium",              # Opcional
            "due_date": "2025-03-15T18:00:00", # Opcional
            "category_id": 3                   # Opcional
        }
    
    Returns:
        {
            "message": "Task created successfully",
            "id": 5,
            "task": { ... }
        }
    """
    data = request.get_json() or {}
    
    # Validar campos requeridos
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    if len(data.get('title', '')) < 3:
        return jsonify({'error': 'Title must be at least 3 characters'}), 400
    
    # Usuario en producción sería el autenticado con Flask-Login
    user_id = request.args.get('user_id', 1, type=int)
    
    # Validar que el usuario exista
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Validar categoría si se proporciona
    category_id = data.get('category_id')
    if category_id:
        category = Category.query.get(category_id)
        if not category or category.user_id != user_id:
            return jsonify({'error': 'Category not found'}), 404
    
    # Crear tarea
    task = Task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        user_id=user_id,
        category_id=category_id
    )
    
    # Procesar fecha opcional
    if data.get('due_date'):
        try:
            task.due_date = datetime.fromisoformat(data['due_date'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid due_date format. Use ISO format'}), 400
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task created successfully',
        'id': task.id,
        'task': {
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'completed': task.completed
        }
    }), 201


# ============================================================================
# RUTAS PUT - Actualización
# ============================================================================

@tasks_bp.route('/<int:task_id>/update', methods=['PUT'])
def update_task(task_id):
    """
    Actualiza una tarea existente.
    
    Body (JSON) - Todos los campos son opcionales:
        {
            "title": "Nuevo título",
            "description": "Nueva descripción",
            "priority": "high",
            "completed": true,
            "due_date": "2025-03-20T15:00:00",
            "category_id": 2
        }
    
    Returns:
        {
            "message": "Task updated successfully",
            "task": { ... }
        }
    """
    task = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    
    # Actualizar campos si se proporcionan
    if 'title' in data:
        if len(data['title']) < 3:
            return jsonify({'error': 'Title must be at least 3 characters'}), 400
        task.title = data['title']
    
    if 'description' in data:
        task.description = data['description']
    
    if 'priority' in data:
        valid_priorities = ['low', 'medium', 'high']
        if data['priority'] not in valid_priorities:
            return jsonify({'error': f'Priority must be one of {valid_priorities}'}), 400
        task.priority = data['priority']
    
    if 'completed' in data:
        task.completed = bool(data['completed'])
    
    if 'due_date' in data:
        if data['due_date'] is None:
            task.due_date = None
        else:
            try:
                task.due_date = datetime.fromisoformat(data['due_date'])
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid due_date format'}), 400
    
    if 'category_id' in data:
        if data['category_id'] is None:
            task.category_id = None
        else:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Category not found'}), 404
            task.category_id = data['category_id']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': {
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'completed': task.completed,
            'updated_at': task.updated_at.isoformat()
        }
    }), 200


# ============================================================================
# RUTAS PATCH - Operaciones Específicas
# ============================================================================

@tasks_bp.route('/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    """
    Cambia el estado de completación de una tarea.
    
    Returns:
        {
            "message": "Task updated",
            "completed": true
        }
    """
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    
    return jsonify({
        'message': 'Task toggled',
        'completed': task.completed
    }), 200


@tasks_bp.route('/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """Marca una tarea como completada."""
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    
    return jsonify({'message': 'Task marked as completed'}), 200


@tasks_bp.route('/<int:task_id>/incomplete', methods=['PATCH'])
def incomplete_task(task_id):
    """Marca una tarea como sin completar."""
    task = Task.query.get_or_404(task_id)
    task.completed = False
    db.session.commit()
    
    return jsonify({'message': 'Task marked as incomplete'}), 200


# ============================================================================
# RUTAS DELETE - Eliminación
# ============================================================================

@tasks_bp.route('/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    """
    Elimina una tarea.
    
    Returns:
        {
            "message": "Task deleted successfully",
            "id": 5
        }
    """
    task = Task.query.get_or_404(task_id)
    task_id_deleted = task.id
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task deleted successfully',
        'id': task_id_deleted
    }), 200


@tasks_bp.route('/delete-completed', methods=['DELETE'])
def delete_completed_tasks():
    """
    Elimina todas las tareas completadas del usuario.
    
    Returns:
        {
            "message": "3 completed tasks deleted",
            "count": 3
        }
    """
    user_id = request.args.get('user_id', 1, type=int)
    
    # Contar tareas antes de eliminar
    completed_tasks = Task.query.filter_by(user_id=user_id, completed=True).all()
    count = len(completed_tasks)
    
    # Eliminar
    for task in completed_tasks:
        db.session.delete(task)
    
    db.session.commit()
    
    return jsonify({
        'message': f'{count} completed tasks deleted',
        'count': count
    }), 200


# ============================================================================
# RUTAS DE ESTADÍSTICAS
# ============================================================================

@tasks_bp.route('/stats', methods=['GET'])
def task_stats():
    """
    Obtiene estadísticas de tareas del usuario.
    
    Returns:
        {
            "total": 10,
            "completed": 6,
            "pending": 4,
            "high_priority": 3,
            "completion_rate": 60.0
        }
    """
    user_id = request.args.get('user_id', 1, type=int)
    
    total = Task.query.filter_by(user_id=user_id).count()
    completed = Task.query.filter_by(user_id=user_id, completed=True).count()
    pending = total - completed
    high_priority = Task.query.filter_by(user_id=user_id, priority='high').count()
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'high_priority': high_priority,
        'completion_rate': round(completion_rate, 2)
    }), 200


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@tasks_bp.errorhandler(404)
def not_found(error):
    """Maneja errores 404."""
    return jsonify({'error': 'Task not found'}), 404


@tasks_bp.errorhandler(400)
def bad_request(error):
    """Maneja errores 400."""
    return jsonify({'error': 'Bad request'}), 400
