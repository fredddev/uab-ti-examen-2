from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.task import Task
from app.models.category import Category
from . import tasks_bp
from groq import Groq
from flask import jsonify
import os


@tasks_bp.route('/tasks')
@login_required
def list_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.all()

    return render_template(
        "tasks_list.html",
        tasks=tasks,
        categories=categories
    )

@tasks_bp.route('/tasks/create', methods=['POST'])
@login_required
def create_task():

    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category_id')

    new_task = Task(
        title=title,
        description=description,
        status='pendiente',
        user_id=current_user.id,
        category_id=category_id if category_id else None
    )

    db.session.add(new_task)
    db.session.commit()

    flash('Tarea creada correctamente', 'success')

    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['POST'])
@login_required
def edit_task(task_id):

    task = Task.query.get_or_404(task_id)

    # Seguridad: verificar que la tarea pertenece al usuario
    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea', 'danger')
        return redirect(url_for('tasks.list_tasks'))

    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.status = request.form.get('status')
    task.category_id = request.form.get('category_id')

    db.session.commit()

    flash('Tarea actualizada correctamente', 'success')

    return redirect(url_for('tasks.list_tasks'))

@tasks_bp.route('/tasks/analizar_reporte')
@login_required
def analizar_reporte():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    pendientes = sum(1 for t in tasks if t.status == "pendiente")
    completadas = sum(1 for t in tasks if t.status == "completado")
    en_progreso = sum(1 for t in tasks if t.status == "en_progreso")

    datos = f"Hay {pendientes} tareas pendientes, {completadas} completadas y {en_progreso} en progreso."

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
Analiza el siguiente reporte de tareas y responde EXACTAMENTE con este formato:

DIAGNOSTICO:
explica el estado actual de las tareas.

RECOMENDACIONES:
1. recomendación
2. recomendación
3. recomendación

CONCLUSION:
resumen final del análisis.

Datos del sistema:
{datos}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Eres un analista de productividad."},
            {"role": "user", "content": f"Analiza este reporte de tareas y da recomendaciones: {datos}"}
        ]
    )

    respuesta = completion.choices[0].message.content

    return jsonify({"respuesta": respuesta})
    

