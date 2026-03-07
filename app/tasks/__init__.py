from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Task, Category

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route('/')
@login_required
def list_tasks():
    """Lista todas las tareas del usuario en el dashboard."""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.all()
    return render_template('dashboard.html', tasks=tasks, categories=categories)


@tasks_bp.route('/<int:task_id>')
@login_required
def get_task(task_id):
    """Obtiene una tarea específica."""
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenece al usuario
    if task.user_id != current_user.id:
        flash('No tienes permiso para ver esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    return render_template('task_detail.html', task=task)


@tasks_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    """Crea una nueva tarea."""
    title = request.form.get('title')
    description = request.form.get('description', '')
    category_id = request.form.get('category_id', None)
    
    if not title:
        flash('El título de la tarea es requerido.', 'danger')
    else:
        try:
            task = Task(
                title=title,
                description=description,
                user_id=current_user.id,
                category_id=category_id if category_id else None,
                status='pendiente'
            )
            db.session.add(task)
            db.session.commit()
            flash(f'✓ Tarea "{title}" creada exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la tarea.', 'danger')
            print(f'Error: {str(e)}')
    
    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    """Actualiza una tarea."""
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenece al usuario
    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    try:
        task.title = request.form.get('title', task.title)
        task.description = request.form.get('description', task.description)
        task.category_id = request.form.get('category_id', task.category_id)
        status = request.form.get('status', task.status)
        task.status = status if status in ['pendiente', 'en_progreso', 'completado'] else task.status
        
        db.session.commit()
        flash('✓ Tarea actualizada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al actualizar la tarea.', 'danger')
        print(f'Error: {str(e)}')
    
    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Elimina una tarea."""
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenece al usuario
    if task.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    try:
        title = task.title
        db.session.delete(task)
        db.session.commit()
        flash(f'✓ Tarea "{title}" eliminada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la tarea.', 'danger')
        print(f'Error: {str(e)}')
    
    return redirect(url_for('tasks.list_tasks'))
