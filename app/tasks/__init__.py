from flask import Blueprint

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route('/')
def list_tasks():
    """Lista todas las tareas del usuario."""
    return {'message': 'Tasks list'}, 200


@tasks_bp.route('/<int:task_id>')
def get_task(task_id):
    """Obtiene una tarea específica."""
    return {'message': f'Task {task_id}'}, 200


@tasks_bp.route('/create', methods=['POST'])
def create_task():
    """Crea una nueva tarea."""
    return {'message': 'Task created'}, 201


@tasks_bp.route('/<int:task_id>/update', methods=['PUT'])
def update_task(task_id):
    """Actualiza una tarea."""
    return {'message': f'Task {task_id} updated'}, 200


@tasks_bp.route('/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    """Elimina una tarea."""
    return {'message': f'Task {task_id} deleted'}, 200
