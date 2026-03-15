from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Task, Category

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route('/')
@login_required
def list_tasks():
    """Lista tareas con filtros opcionales"""

    status_filter = request.args.get('status')
    category_filter = request.args.get('category')

    query = Task.query.filter_by(user_id=current_user.id)

    # filtro por estado
    if status_filter and status_filter != 'todos':
        query = query.filter(Task.status == status_filter)

    # filtro por categoría
    if category_filter and category_filter != 'todas':
        query = query.filter(Task.category_id == category_filter)

    tasks = query.all()

    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'tasks_list.html',
        tasks=tasks,
        categories=categories,
        status_filter=status_filter,
        category_filter=category_filter
    )


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

from flask import send_file
import openpyxl
from io import BytesIO

@tasks_bp.route('/export')
@login_required
def export_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    # Crear archivo Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Tareas"

    # Encabezados
    sheet.append([
        "Title",
        "Description",
        "Status",
        "Category",
        "User"
    ])

    # Datos
    for task in tasks:
        category_name = task.category.name if task.category else "Sin categoría"

        sheet.append([
            task.title,
            task.description,
            task.status,
            category_name,
            current_user.username
        ])

    # Guardar en memoria
    file_stream = BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)

    return send_file(
        file_stream,
        as_attachment=True,
        download_name="tareas.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

from groq import Groq
from flask import jsonify
import os

@tasks_bp.route('/analizar_reporte')
@login_required
def analizar_reporte():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    pendientes = sum(1 for t in tasks if t.status == "pendiente")
    completadas = sum(1 for t in tasks if t.status == "completado")
    en_progreso = sum(1 for t in tasks if t.status == "en_progreso")

    datos = f"Hay {pendientes} tareas pendientes, {completadas} completadas y {en_progreso} en progreso."

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Eres un analista de productividad."},
            {"role": "user", "content": f"Analiza este reporte de tareas y da recomendaciones: {datos}"}
        ]
    )

    respuesta = completion.choices[0].message.content

    return jsonify({"respuesta": respuesta})