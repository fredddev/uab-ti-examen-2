# Ejemplos de Uso - Modelos y Database

Este archivo muestra ejemplos prácticos de cómo crear y usar modelos con Flask-SQLAlchemy.

## 1. Crear un Nuevo Modelo

### Opción A: Agregar a `app/models/__init__.py`

```python
from app import db

class Project(db.Model):
    """Modelo para proyectos."""
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relación
    user = db.relationship('User', backref='projects')
    
    def __repr__(self):
        return f'<Project {self.name}>'
```

### Opción B: Crear archivo separado `app/models/project.py`

```python
from app import db

class Project(db.Model):
    __tablename__ = 'project'
    # ... mismo código ...
```

Luego importar en `app/models/__init__.py`:

```python
from app.models.project import Project
```

## 2. Crear Migración

```bash
# 1. Generar migración
flask db migrate -m "Add Project model"

# 2. Revisar archivo generado en migrations/versions/
# 3. Aplicar a la base de datos
flask db upgrade
```

## 3. Usar el Modelo en Rutas

### Ejemplo en `app/tasks/__init__.py`

```python
from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, User, Category

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route('/', methods=['GET'])
def list_tasks():
    """Lista todas las tareas del usuario."""
    # Simulando usuario autenticado (usar Flask-Login en producción)
    user_id = 1
    
    tasks = Task.query.filter_by(user_id=user_id, completed=False).all()
    return {
        'tasks': [
            {
                'id': t.id,
                'title': t.title,
                'priority': t.priority,
                'category': t.category.name if t.category else None
            }
            for t in tasks
        ]
    }, 200


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obtiene una tarea específica."""
    task = Task.query.get_or_404(task_id)
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'priority': task.priority,
        'due_date': task.due_date.iso format() if task.due_date else None,
        'category': task.category.name if task.category else None
    }, 200


@tasks_bp.route('/create', methods=['POST'])
def create_task():
    """Crea una nueva tarea."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return {'error': 'Title is required'}, 400
    
    task = Task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        user_id=1,  # Reemplazar con usuario autenticado
        category_id=data.get('category_id')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return {
        'message': 'Task created',
        'id': task.id
    }, 201


@tasks_bp.route('/<int:task_id>/update', methods=['PUT'])
def update_task(task_id):
    """Actualiza una tarea."""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    if 'priority' in data:
        task.priority = data['priority']
    if 'due_date' in data:
        task.due_date = data['due_date']
    
    db.session.commit()
    
    return {'message': f'Task {task_id} updated'}, 200


@tasks_bp.route('/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    """Elimina una tarea."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    return {'message': f'Task {task_id} deleted'}, 200


@tasks_bp.route('/complete/<int:task_id>', methods=['PATCH'])
def complete_task(task_id):
    """Marca una tarea como completada."""
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    
    return {'message': f'Task {task_id} marked as completed'}, 200
```

## 4. Operaciones Comunes con BD

### Insertar Registro

```python
from app import db
from app.models import User

user = User(
    username='juan',
    email='juan@example.com',
    password='hashed_password'
)
db.session.add(user)
db.session.commit()

# O múltiples registros
users = [
    User(username='user1', email='user1@ex.com', password='pwd1'),
    User(username='user2', email='user2@ex.com', password='pwd2'),
]
db.session.add_all(users)
db.session.commit()
```

### Consultar Registros

```python
# Todos los registros
all_users = User.query.all()

# Primer registro
first_user = User.query.first()

# Filtrar por campo
user = User.query.filter_by(username='juan').first()

# Filtrar con condiciones complejas
from sqlalchemy import and_, or_

active_admins = User.query.filter(
    and_(
        User.role == 'admin',
        User.active == True
    )
).all()

# Contar
count = User.query.count()

# Límite y offset
users = User.query.limit(10).offset(0).all()  # Paginación

# Ordenar
users = User.query.order_by(User.created_at.desc()).all()
```

### Actualizar Registros

```python
# Obtenery actualizar
user = User.query.get(1)
user.email = 'newemail@example.com'
db.session.commit()

# Actualizar múltiples
db.session.query(Task).filter_by(user_id=1).update({'completed': True})
db.session.commit()
```

### Eliminar Registros

```python
# Obtener y eliminar
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# Eliminar múltiples
db.session.query(Task).filter_by(completed=True).delete()
db.session.commit()
```

### Relaciones

```python
# Acceder relación uno a muchos
user = User.query.get(1)
user_tasks = user.tasks  # Obtenertodas las tareas del usuario

# Crear con relación
task = Task(
    title='Mi Tarea',
    user_id=1  # O user=user_object
)

# Filtrar por relación
tasks = Task.query.filter_by(user=user).all()

# Join con relación
from sqlalchemy import join

tasks_with_user = db.session.query(Task, User).join(User).all()
```

### Transacciones

```python
try:
    task1 = Task(title='Tarea 1', user_id=1)
    task2 = Task(title='Tarea 2', user_id=1)
    
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(f"Error: {e}")
```

## 5. Uso en Flask Shell

```bash
flask shell
```

```python
>>> from app import db
>>> from app.models import User, Task, Category

>>> # Crear
>>> u = User(username='laura', email='laura@ex.com', password='pwd')
>>> db.session.add(u)
>>> db.session.commit()
>>> u.id
1

>>> # Leer
>>> User.query.all()
[<User laura>]

>>> # Actualizar
>>> u.email = 'laura.updated@ex.com'
>>> db.session.commit()

>>> # Eliminar
>>> db.session.delete(u)
>>> db.session.commit()

>>> # Relaciones
>>> user = User.query.first()
>>> user.tasks
[<Task Tarea 1>, <Task Tarea 2>]

>>> # Contar
>>> Task.query.count()
10

>>> # Filtrar
>>> Task.query.filter_by(completed=False).count()
5
```

## 6. Patrones de Consulta Útiles

### Paginación

```python
page = 1
per_page = 10
tasks = Task.query.paginate(page=page, per_page=per_page)

tasks.items      # Elementos de está página
tasks.total      # Total de elementos
tasks.pages      # Total de páginas
tasks.has_next   # Hay siguiente página
tasks.next_num   # Número de siguiente página
```

### Búsqueda de Texto

```python
search_term = 'importante'
tasks = Task.query.filter(Task.title.ilike(f'%{search_term}%')).all()
```

### Agregaciones

```python
from sqlalchemy import func

# Contar
count = db.session.query(func.count(Task.id)).filter_by(user_id=1).scalar()

# Sum
total = db.session.query(func.sum(Task.id)).scalar()

# Average
avg = db.session.query(func.avg(Task.priority)).scalar()
```

---

## 📝 Mejores Prácticas

1. **Siempre usar `db.session.commit()`** después de cambios
2. **Validar datos** antes de insertar en BD
3. **Usar blueprints** para organizar rutas
4. **Context manager** para app context si es necesario:
   ```python
   with app.app_context():
       users = User.query.all()
   ```
5. **Índices** en campos que se consultan frecuentemente
6. **Relaciones lazy** adecuadamente para performance
