"""Seed categories and tasks test data.

Revision ID: 002_seed_categories_tasks
Revises: 001_create_admin_user
Create Date: 2026-03-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = '002_seed_categories_tasks'
down_revision = '001_create_admin_user'
branch_labels = None
depends_on = None


# ---------------------------------------------------------------------------
# Datos de prueba
# ---------------------------------------------------------------------------

CATEGORIES = [
    {
        "name": "Trabajo",
        "description": "Tareas relacionadas con el trabajo y proyectos profesionales",
    },
    {
        "name": "Personal",
        "description": "Tareas de desarrollo personal y objetivos de vida",
    },
    {
        "name": "Estudio",
        "description": "Tareas de estudio, formación y aprendizaje",
    },
    {
        "name": "Hogar",
        "description": "Tareas del hogar, limpieza y mantenimiento",
    },
    {
        "name": "Salud",
        "description": "Tareas relacionadas con salud, ejercicio y bienestar",
    },
]

# 30 tareas distribuidas en las 5 categorías (6 por categoría).
# El campo category_index hace referencia al índice en CATEGORIES (0-based).
TASKS = [
    # --- Trabajo (6) ---
    {
        "title": "Revisar correos del cliente",
        "description": "Leer y responder todos los correos pendientes del cliente principal.",
        "status": "completado",
        "category_index": 0,
    },
    {
        "title": "Preparar informe mensual",
        "description": "Redactar el informe de actividades del mes con métricas y KPIs.",
        "status": "en_progreso",
        "category_index": 0,
    },
    {
        "title": "Reunión de planificación semanal",
        "description": "Asistir a la reunión de planificación del equipo y tomar notas.",
        "status": "pendiente",
        "category_index": 0,
    },
    {
        "title": "Actualizar documentación del proyecto",
        "description": "Revisar y actualizar todos los documentos técnicos del proyecto activo.",
        "status": "pendiente",
        "category_index": 0,
    },
    {
        "title": "Revisión de código (code review)",
        "description": "Revisar los pull requests pendientes de los compañeros de equipo.",
        "status": "en_progreso",
        "category_index": 0,
    },
    {
        "title": "Presentación para el cliente",
        "description": "Preparar slides para la demo del nuevo módulo ante el cliente.",
        "status": "pendiente",
        "category_index": 0,
    },
    # --- Personal (6) ---
    {
        "title": "Leer libro de hábitos",
        "description": "Leer al menos 30 páginas del libro 'Atomic Habits' de James Clear.",
        "status": "en_progreso",
        "category_index": 1,
    },
    {
        "title": "Organizar agenda semanal",
        "description": "Planificar las actividades de la próxima semana con prioridades.",
        "status": "completado",
        "category_index": 1,
    },
    {
        "title": "Llamar a la familia",
        "description": "Hacer una videollamada con los padres y hermanos.",
        "status": "pendiente",
        "category_index": 1,
    },
    {
        "title": "Revisar finanzas personales",
        "description": "Actualizar la hoja de cálculo de gastos e ingresos del mes.",
        "status": "pendiente",
        "category_index": 1,
    },
    {
        "title": "Planificar vacaciones",
        "description": "Investigar destinos, precios de vuelos y alojamiento para las vacaciones.",
        "status": "pendiente",
        "category_index": 1,
    },
    {
        "title": "Actualizar CV",
        "description": "Añadir los proyectos y habilidades más recientes al currículum.",
        "status": "completado",
        "category_index": 1,
    },
    # --- Estudio (6) ---
    {
        "title": "Completar curso de Python avanzado",
        "description": "Terminar los módulos 7, 8 y 9 del curso online de Python.",
        "status": "en_progreso",
        "category_index": 2,
    },
    {
        "title": "Estudiar patrones de diseño",
        "description": "Repasar los patrones creacionales y estructurales con ejemplos en código.",
        "status": "pendiente",
        "category_index": 2,
    },
    {
        "title": "Practicar algoritmos de ordenamiento",
        "description": "Implementar y analizar la complejidad de QuickSort, MergeSort y HeapSort.",
        "status": "completado",
        "category_index": 2,
    },
    {
        "title": "Leer documentación de Flask",
        "description": "Revisar la documentación oficial de Flask para blueprints y extensiones.",
        "status": "completado",
        "category_index": 2,
    },
    {
        "title": "Repasar SQL avanzado",
        "description": "Practicar consultas con JOINs complejos, CTEs y funciones de ventana.",
        "status": "pendiente",
        "category_index": 2,
    },
    {
        "title": "Aprender Docker básico",
        "description": "Crear y desplegar contenedores Docker con una aplicación Flask.",
        "status": "en_progreso",
        "category_index": 2,
    },
    # --- Hogar (6) ---
    {
        "title": "Limpiar y organizar el escritorio",
        "description": "Ordenar cables, documentos y accesorios del espacio de trabajo.",
        "status": "completado",
        "category_index": 3,
    },
    {
        "title": "Hacer la compra semanal",
        "description": "Comprar frutas, verduras y productos de primera necesidad.",
        "status": "pendiente",
        "category_index": 3,
    },
    {
        "title": "Reparar la persiana del dormitorio",
        "description": "Revisar el mecanismo de la persiana rota y comprar piezas si hace falta.",
        "status": "pendiente",
        "category_index": 3,
    },
    {
        "title": "Pasar la aspiradora",
        "description": "Limpiar todas las habitaciones con aspiradora y fregona.",
        "status": "completado",
        "category_index": 3,
    },
    {
        "title": "Pagar facturas del mes",
        "description": "Pagar luz, agua, internet y comunidad de vecinos.",
        "status": "en_progreso",
        "category_index": 3,
    },
    {
        "title": "Revisar nevera y despensa",
        "description": "Eliminar productos caducados y reorganizar los alimentos.",
        "status": "pendiente",
        "category_index": 3,
    },
    # --- Salud (6) ---
    {
        "title": "Salir a correr 5 km",
        "description": "Completar una carrera de 5 km en menos de 30 minutos.",
        "status": "completado",
        "category_index": 4,
    },
    {
        "title": "Rutina de estiramientos matutinos",
        "description": "Realizar 15 minutos de estiramientos al despertar durante toda la semana.",
        "status": "en_progreso",
        "category_index": 4,
    },
    {
        "title": "Pedir cita con el médico",
        "description": "Solicitar revisión anual con el médico de cabecera.",
        "status": "pendiente",
        "category_index": 4,
    },
    {
        "title": "Reducir consumo de azúcar",
        "description": "Evitar bebidas azucaradas y dulces procesados durante dos semanas.",
        "status": "en_progreso",
        "category_index": 4,
    },
    {
        "title": "Sesión de meditación",
        "description": "Practicar 10 minutos de meditación mindfulness antes de dormir.",
        "status": "pendiente",
        "category_index": 4,
    },
    {
        "title": "Beber 2 litros de agua al día",
        "description": "Registrar la ingesta diaria de agua y alcanzar los 2 litros recomendados.",
        "status": "completado",
        "category_index": 4,
    },
]


def upgrade():
    connection = op.get_bind()

    # ------------------------------------------------------------------
    # 1. Obtener el ID del usuario 'user' (creado en la migración 001)
    # ------------------------------------------------------------------
    result = connection.execute(
        sa.text("SELECT id FROM user WHERE username = 'user'")
    )
    row = result.fetchone()

    if row is None:
        print("⚠ Usuario 'user' no encontrado. Saltando seed de categorías y tareas.")
        return

    user_id = row[0]

    # ------------------------------------------------------------------
    # 2. Insertar categorías (omitir si ya existen para ese usuario)
    # ------------------------------------------------------------------
    category_ids = []
    base_date = datetime(2026, 1, 1, 8, 0, 0)

    for i, cat in enumerate(CATEGORIES):
        existing = connection.execute(
            sa.text(
                "SELECT id FROM categories WHERE user_id = :uid AND name = :name"
            ),
            {"uid": user_id, "name": cat["name"]},
        ).fetchone()

        if existing:
            category_ids.append(existing[0])
            print(f"  ↷ Categoría ya existe: {cat['name']}")
        else:
            created_at = base_date + timedelta(days=i)
            connection.execute(
                sa.text(
                    """INSERT INTO categories (name, description, user_id, created_at)
                       VALUES (:name, :description, :user_id, :created_at)"""
                ),
                {
                    "name": cat["name"],
                    "description": cat["description"],
                    "user_id": user_id,
                    "created_at": created_at,
                },
            )
            new_id = connection.execute(
                sa.text(
                    "SELECT id FROM categories WHERE user_id = :uid AND name = :name"
                ),
                {"uid": user_id, "name": cat["name"]},
            ).fetchone()[0]
            category_ids.append(new_id)
            print(f"  ✓ Categoría creada: {cat['name']}")

    # ------------------------------------------------------------------
    # 3. Insertar tareas (omitir si ya existe una tarea con el mismo
    #    título para ese usuario)
    # ------------------------------------------------------------------
    for j, task in enumerate(TASKS):
        existing = connection.execute(
            sa.text(
                "SELECT id FROM tasks WHERE user_id = :uid AND title = :title"
            ),
            {"uid": user_id, "title": task["title"]},
        ).fetchone()

        if existing:
            print(f"  ↷ Tarea ya existe: {task['title']}")
            continue

        cat_id = category_ids[task["category_index"]]
        created_at = base_date + timedelta(days=j, hours=j % 8)
        connection.execute(
            sa.text(
                """INSERT INTO tasks (title, description, status, user_id, category_id, created_at, updated_at)
                   VALUES (:title, :description, :status, :user_id, :category_id, :created_at, :updated_at)"""
            ),
            {
                "title": task["title"],
                "description": task["description"],
                "status": task["status"],
                "user_id": user_id,
                "category_id": cat_id,
                "created_at": created_at,
                "updated_at": created_at,
            },
        )
        print(f"  ✓ Tarea creada: {task['title']}")

    print(f"\n✅ Seed completado: {len(CATEGORIES)} categorías y {len(TASKS)} tareas insertadas para el usuario 'user'.")


def downgrade():
    connection = op.get_bind()

    result = connection.execute(
        sa.text("SELECT id FROM user WHERE username = 'user'")
    )
    row = result.fetchone()
    if row is None:
        return

    user_id = row[0]

    # Eliminar las tareas del seed
    for task in TASKS:
        connection.execute(
            sa.text(
                "DELETE FROM tasks WHERE user_id = :uid AND title = :title"
            ),
            {"uid": user_id, "title": task["title"]},
        )

    # Eliminar las categorías del seed
    for cat in CATEGORIES:
        connection.execute(
            sa.text(
                "DELETE FROM categories WHERE user_id = :uid AND name = :name"
            ),
            {"uid": user_id, "name": cat["name"]},
        )

    print("↩ Seed de categorías y tareas revertido.")
