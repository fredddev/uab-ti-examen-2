"""
Rutas para el dashboard inteligente.
"""

from flask import render_template, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Task, Category
from . import dashboard_bp
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json


def analyze_task_data(tasks):
    """
    Analiza los datos de las tareas del usuario y genera insights automáticos.

    Args:
        tasks: Lista de objetos Task del usuario

    Returns:
        dict: Diccionario con métricas y resumen inteligente
    """
    if not tasks:
        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'productivity_percentage': 0,
            'most_used_category': None,
            'most_productive_day': None,
            'upcoming_tasks': 0,
            'summary': "No tienes tareas aún. ¡Crea tu primera tarea para comenzar!"
        }

    # Cálculos básicos
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == 'completado'])
    pending_tasks = len([t for t in tasks if t.status == 'pendiente'])
    productivity_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Categoría más utilizada
    categories = [t.category.name for t in tasks if t.category]
    most_used_category = Counter(categories).most_common(1)[0][0] if categories else None

    # Día con más tareas completadas
    completed_dates = [t.updated_at.date() for t in tasks if t.status == 'completado']
    if completed_dates:
        day_counts = Counter(completed_dates)
        most_productive_day = day_counts.most_common(1)[0][0].strftime('%A')
        # Traducir al español
        day_translation = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        most_productive_day = day_translation.get(most_productive_day, most_productive_day)
    else:
        most_productive_day = None

    now = datetime.now()
    yesterday = now - timedelta(hours=24)

    upcoming_tasks = len([t for t in tasks if t.created_at >= yesterday])

    # Generar resumen inteligente
    summary_parts = []

    # Análisis semanal (últimos 7 días)
    week_ago = now - timedelta(days=7)
    tasks_this_week = [t for t in tasks if t.created_at >= week_ago]
    completed_this_week = [t for t in tasks_this_week if t.status == 'completado']

    if tasks_this_week:
        summary_parts.append(f"Esta semana se crearon {len(tasks_this_week)} tareas y se completaron {len(completed_this_week)}.")

    summary_parts.append(f"La productividad general es del {productivity_percentage:.1f}%.")

    if most_used_category:
        summary_parts.append(f"La categoría más utilizada es '{most_used_category}'.")

    if most_productive_day:
        summary_parts.append(f"El día con más tareas completadas fue {most_productive_day}.")

    if upcoming_tasks > 0:
        summary_parts.append(f"Tienes {upcoming_tasks} tareas que vencen en las próximas 24 horas.")
    elif upcoming_tasks == 0:
        summary_parts.append("No tienes tareas próximas a vencer.")

    summary = " ".join(summary_parts)

    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'productivity_percentage': round(productivity_percentage, 1),
        'most_used_category': most_used_category,
        'most_productive_day': most_productive_day,
        'upcoming_tasks': upcoming_tasks,
        'summary': summary
    }


def prepare_productivity_evolution_data(tasks):
    """
    Prepara datos para el gráfico de evolución de productividad.

    Returns:
        dict: Datos en formato JSON para Chart.js
    """
    # Últimos 7 días
    dates = []
    created_counts = []
    completed_counts = []

    for i in range(6, -1, -1):

        date = datetime.now().date() - timedelta(days=i)
        dates.append(date.strftime('%d/%m'))

        created = len([
            t for t in tasks
            if t.created_at and t.created_at.date() == date
        ])

        completed = len([
            t for t in tasks
            if t.status == 'completado'
            and t.updated_at
            and t.updated_at.date() == date
        ])

        created_counts.append(created)
        completed_counts.append(completed)

    return {
        'labels': dates,
        'datasets': [
            {
                'label': 'Tareas Creadas',
                'data': created_counts,
                'borderColor': 'rgb(54, 162, 235)',
                'backgroundColor': 'rgba(54, 162, 235, 0.1)',
                'tension': 0.1
            },
            {
                'label': 'Tareas Completadas',
                'data': completed_counts,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.1)',
                'tension': 0.1
            }
        ]
    }


def prepare_category_distribution_data(tasks):
    """
    Prepara datos para el gráfico de distribución por categoría.

    Returns:
        dict: Datos en formato JSON para Chart.js
    """
    category_counts = Counter([t.category.name for t in tasks if t.category])

    if not category_counts:
        return {
            'labels': ['Sin categoría'],
            'datasets': [{
                'data': [len([t for t in tasks if not t.category])],
                'backgroundColor': ['#6c757d']
            }]
        }

    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']

    return {
        'labels': list(category_counts.keys()),
        'datasets': [{
            'data': list(category_counts.values()),
            'backgroundColor': colors[:len(category_counts)],
            'hoverOffset': 4
        }]
    }


def prepare_status_distribution_data(tasks):
    """
    Prepara datos para el gráfico de distribución por estado.

    Returns:
        dict: Datos en formato JSON para Chart.js
    """
    status_counts = Counter([t.status for t in tasks])

    # Asegurar que todos los estados estén representados
    all_statuses = ['pendiente', 'en_progreso', 'completado']
    labels = []
    data = []
    colors = []

    status_config = {
        'pendiente': {'label': 'Pendientes', 'color': '#FFC107'},
        'en_progreso': {'label': 'En Progreso', 'color': '#17A2B8'},
        'completado': {'label': 'Completadas', 'color': '#28A745'}
    }

    for status in all_statuses:
        count = status_counts.get(status, 0)
        labels.append(status_config[status]['label'])
        data.append(count)
        colors.append(status_config[status]['color'])

    return {
        'labels': labels,
        'datasets': [{
            'data': data,
            'backgroundColor': colors,
            'borderWidth': 1
        }]
    }


@dashboard_bp.route('/')
@login_required
def dashboard():
    """
    Ruta principal del dashboard inteligente.
    """
    # Obtener tareas del usuario actual
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    # Analizar datos
    insights = analyze_task_data(tasks)

    # Preparar datos para gráficos
    productivity_data = prepare_productivity_evolution_data(tasks)
    category_data = prepare_category_distribution_data(tasks)
    status_data = prepare_status_distribution_data(tasks)

    # Obtener categorías para el formulario
    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'dashboard.html',
        tasks=tasks,
        categories=categories,
        insights=insights,
        productivity_data=json.dumps(productivity_data),
        category_data=json.dumps(category_data),
        status_data=json.dumps(status_data)
    )


@dashboard_bp.route('/api/dashboard-data')
@login_required
def dashboard_data():
    """
    API endpoint para obtener datos del dashboard en formato JSON.
    Útil para actualizaciones AJAX.
    """
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    insights = analyze_task_data(tasks)
    productivity_data = prepare_productivity_evolution_data(tasks)
    category_data = prepare_category_distribution_data(tasks)
    status_data = prepare_status_distribution_data(tasks)

    return jsonify({
        'insights': insights,
        'productivity_data': productivity_data,
        'category_data': category_data,
        'status_data': status_data
    })