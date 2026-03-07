# Ejemplos de Rutas Protegidas

Este archivo contiene ejemplos prácticos de cómo crear rutas protegidas con Flask-Login en diferentes escenarios.

---

## 1. Ruta Protegida Simple

```python
from flask import Blueprint, render_template
from flask_login import login_required, current_user

my_bp = Blueprint('myapp', __name__)

@my_bp.route('/protected')
@login_required
def protected_route():
    """Esta ruta requiere que el usuario esté autenticado."""
    return f"Hola {current_user.username}"
```

**Comportamiento:**
- Usuario autenticado → Muestra el contenido
- Usuario NO autenticado → Redirige a `/auth/login?next=/protected`

---

## 2. Ruta con Verificación de Propiedad

```python
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Task

@my_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Editar una tarea solo si pertenece al usuario."""
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenece al usuario autenticado
    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        db.session.commit()
        flash('Tarea actualizada exitosamente.', 'success')
        return redirect(url_for('tasks.list_tasks'))
    
    return render_template('edit_task.html', task=task)
```

**Puntos de seguridad:**
1. `@login_required` - Requiere autenticación
2. `Task.query.get_or_404(task_id)` - Retorna 404 si no existe
3. `if task.user_id != current_user.id` - Verifica propiedad
4. `flash()` - Mensaje informativo al usuario

---

## 3. Ruta con Verificación de Rol

```python
from flask import Blueprint, abort
from flask_login import login_required, current_user

@my_bp.route('/admin/users')
@login_required
def admin_users():
    """Solo administradores pueden acceder."""
    # Verificar que es administrador
    if current_user.role != 'admin':
        abort(403)  # Forbidden
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)
```

**Alternativa usando un decorador personalizado:**

```python
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@my_bp.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)
```

---

## 4. Ruta API Protegida (JSON)

```python
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Task

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Obtener todas las tareas del usuario en formato JSON."""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status
        }
        for task in tasks
    ]), 200

@api_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """Crear una nueva tarea vía API."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'El título es requerido'}), 400
    
    try:
        task = Task(
            title=data.get('title'),
            description=data.get('description', ''),
            user_id=current_user.id,
            status='pendiente'
        )
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'id': task.id,
            'title': task.title,
            'status': task.status
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
```

---

## 5. Ruta Condicional (Depende de Autenticación)

```python
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

@my_bp.route('/dashboard')
def dashboard():
    """Dashboard que actúa diferente según autenticación."""
    if current_user.is_authenticated:
        # Usuario autenticado - mostrar panel de control
        return render_template('dashboard.html', user=current_user)
    else:
        # Usuario no autenticado - redirigir al login
        return redirect(url_for('auth.login'))
```

---

## 6. Acceder a Datos del Usuario en Plantillas

```html
<!-- base.html o cualquier plantilla -->

{% if current_user.is_authenticated %}
    <!-- Usuario autenticado -->
    <div>
        <p>Hola, {{ current_user.username }}!</p>
        <p>Email: {{ current_user.email }}</p>
        <p>Rol: {{ current_user.role }}</p>
        <p>ID: {{ current_user.id }}</p>
        
        <a href="{{ url_for('auth.logout') }}">Cerrar sesión</a>
    </div>
{% else %}
    <!-- Usuario NO autenticado -->
    <div>
        <a href="{{ url_for('auth.login') }}">Iniciar sesión</a>
        <a href="{{ url_for('auth.register') }}">Registrarse</a>
    </div>
{% endif %}
```

---

## 7. Ruta de Descarga con Autenticación

```python
from flask import Blueprint, send_file
from flask_login import login_required, current_user
from app.models import Task
import io

@my_bp.route('/tasks/<int:task_id>/export')
@login_required
def export_task(task_id):
    """Exportar una tarea como PDF (solo si pertenece al usuario)."""
    task = Task.query.get_or_404(task_id)
    
    # Verificar propiedad
    if task.user_id != current_user.id:
        abort(403)
    
    # Generar PDF o documento
    pdf_data = generate_pdf(task)
    
    return send_file(
        io.BytesIO(pdf_data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'tarea_{task_id}.pdf'
    )
```

---

## 8. Patrón: Verificación Centralizada

```python
def check_resource_ownership(resource, user_id):
    """
    Función auxiliar para verificar que un recurso pertenece a un usuario.
    """
    if resource.user_id != user_id:
        abort(403)  # Forbidden
    return True

# Uso en rutas:
@my_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    check_resource_ownership(task, current_user.id)  # Verifica propiedad
    
    # ... continuar con la actualización
```

---

## 9. Listar Recursos Filtración Automática

```python
# MALO - Obtiene TODAS las tareas
@my_bp.route('/tasks')
@login_required
def list_all_tasks():
    tasks = Task.query.all()  # ❌ Expone tareas de otros usuarios
    return render_template('tasks.html', tasks=tasks)

# BIEN - Obtiene solo las tareas del usuario
@my_bp.route('/tasks')
@login_required
def list_user_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()  # ✓ Seguro
    return render_template('tasks.html', tasks=tasks)
```

---

## 10. Manejo de Errores de Autenticación

```python
from flask import Blueprint
from flask_login import login_required, current_user
from werkzeug.exceptions import Forbidden, Unauthorized

@my_bp.route('/secure-data')
@login_required
def secure_data():
    """Ruta que puede lanzar diferentes errores."""
    try:
        # Verificar acceso
        if not current_user.is_active:
            raise Forbidden('Tu cuenta está desactivada.')
        
        # Obtener datos
        resource = get_user_resource(current_user.id)
        if not resource:
            raise Unauthorized('No tienes acceso a este recurso.')
        
        return jsonify(resource)
    
    except Forbidden as e:
        return jsonify({'error': str(e)}), 403
    except Unauthorized as e:
        return jsonify({'error': str(e)}), 401
```

---

## Mejores Prácticas

### ✅ DO (Hacer)

1. **Siempre usar `@login_required`** en rutas que requieren autenticación
2. **Verificar propiedad de recursos** antes de modificar/acceder
3. **Filtrar queries por usuario**: `Task.query.filter_by(user_id=current_user.id)`
4. **Usar `current_user` en plantillas** para datos dinámicos
5. **Loguear accesos denegados** para auditoría
6. **Usar HTTPS en producción** para proteger sesiones

### ❌ DON'T (No hacer)

1. ❌ Omitir `@login_required` en rutas privadas
2. ❌ Confiar solo en URLs privadas (siempre validar en backend)
3. ❌ Devolver datos sensibles en errores 404
4. ❌ Modificar `current_user` directamente en la ruta
5. ❌ Guardar contraseñas en texto plano
6. ❌ Usar sesiones inseguras

---

## Testing

```python
# test_protected_routes.py
import pytest
from app import create_app, db
from app.models import User, Task

@pytest.fixture
def client():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_protected_route_without_login(client):
    """Acceder a ruta protegida sin autenticación."""
    response = client.get('/tasks/')
    assert response.status_code == 302  # Redirige
    assert '/auth/login' in response.location

def test_protected_route_with_login(client):
    """Acceder a ruta protegida con autenticación."""
    # Crear usuario
    user = User(username='test', email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    # Login
    client.post('/auth/login', data={
        'username': 'test',
        'password': 'password'
    })
    
    # Acceder a ruta protegida
    response = client.get('/tasks/')
    assert response.status_code == 200

def test_resource_ownership(client):
    """Verificar que no puedes acceder a recursos de otros usuarios."""
    # Crear dos usuarios
    user1 = User(username='user1', email='user1@example.com')
    user1.set_password('password')
    user2 = User(username='user2', email='user2@example.com')
    user2.set_password('password')
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # Crear tarea para user1
    task = Task(title='Tarea', user_id=user1.id)
    db.session.add(task)
    db.session.commit()
    
    # Login como user2
    client.post('/auth/login', data={
        'username': 'user2',
        'password': 'password'
    })
    
    # Intentar editar tarea de user1
    response = client.post(f'/tasks/{task.id}/update', data={
        'title': 'Modificada'
    })
    
    # Debería estar denegado
    assert response.status_code == 302  # Redirige o falla
    
    # Verificar que la tarea NO fue modificada
    db.session.refresh(task)
    assert task.title == 'Tarea'
```

---

## Referencia Rápida

| Decorador/Función | Propósito |
|------------------|-----------|
| `@login_required` | Proteger ruta - requiere autenticación |
| `current_user` | Acceder al usuario autenticado actual |
| `current_user.is_authenticated` | Verificar si hay usuario activo |
| `login_user(user)` | Iniciar sesión de usuario |
| `logout_user()` | Cerrar sesión de usuario |
| `User.query.get_or_404(id)` | Obtener usuario o 404 |

---

**Fecha:** March 7, 2026  
**Framework:** Flask 3.0.0  
**Extensión:** Flask-Login 0.6.3
