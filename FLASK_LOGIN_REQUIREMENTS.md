# Resumen de Protección de Rutas con Flask-Login

## ✅ Lo que se ha implementado

### 1. **Configuración de Flask-Login** (Already in place)

En [app/__init__.py](app/__init__.py):

```python
from flask_login import LoginManager

login_manager = LoginManager()

# En create_app():
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Ruta de redirección
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

**Comportamiento:**
- Usuarios NO autenticados → Redirigidos a `/auth/login`
- Mensaje personalizado mostrado en la página de login
- Usuario se carga automáticamente desde la sesión

---

### 2. **Decorador @login_required en todas las rutas**

#### ✓ Rutas de Tareas (`/tasks/`) - PROTEGIDAS

[app/tasks/__init__.py](app/tasks/__init__.py):

```python
from flask_login import login_required, current_user

@tasks_bp.route('/')
@login_required
def list_tasks():
    """Lista las tareas del usuario autenticado."""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks, categories=categories)

@tasks_bp.route('/<int:task_id>')
@login_required
def get_task(task_id):
    # Verificar que la tarea pertenece al usuario
    if task.user_id != current_user.id:
        flash('No tienes permiso para ver esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))

@tasks_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    task = Task(
        title=request.form.get('title'),
        user_id=current_user.id,  # Asignar al usuario autenticado
        # ...
    )

@tasks_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    # Seguridad: Verificar propiedad
    if task.user_id != current_user.id:
        return redirect(url_for('tasks.list_tasks'))

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    # Seguridad: Verificar propiedad
    if task.user_id != current_user.id:
        return redirect(url_for('tasks.list_tasks'))
```

#### ✓ Rutas de Usuarios (`/users/`) - PROTEGIDAS

[app/users/__init__.py](app/users/__init__.py):

```python
from flask_login import login_required

@users_bp.route('/')
@login_required
def list_users():
    """Lista todos los usuarios."""
    return {'message': 'Users list'}, 200

@users_bp.route('/<int:user_id>')
@login_required
def get_user(user_id):
    """Obtiene un usuario específico."""
    return {'message': f'User {user_id}'}, 200

@users_bp.route('/<int:user_id>/profile')
@login_required
def user_profile(user_id):
    """Obtiene el perfil de un usuario."""
    user = User.query.get_or_404(user_id)
    return {'message': f'User {user_id} profile'}, 200
```

#### ✓ Rutas de Categorías (`/categories/`) - PROTEGIDAS

[app/categories/__init__.py](app/categories/__init__.py):

```python
from flask_login import login_required, current_user

@categories_bp.route('/')
@login_required
def list_categories():
    """Lista las categorías del usuario autenticado."""
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return {'message': 'Categories list', 'data': [c.to_dict() for c in categories]}, 200

@categories_bp.route('/<int:category_id>')
@login_required
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    # Seguridad: Solo ver categorías propias
    if category.user_id != current_user.id:
        return {'error': 'No tienes permiso para ver esta categoría'}, 403
    return {'message': f'Category {category_id}', 'data': category.to_dict()}, 200

@categories_bp.route('/create', methods=['POST'])
@login_required
def create_category():
    """Crea una nueva categoría para el usuario autenticado."""
    data = request.get_json()
    category = Category(
        name=data.get('name'),
        user_id=current_user.id,  # Asignar al usuario autenticado
        # ...
    )

@categories_bp.route('/<int:category_id>/update', methods=['PUT'])
@login_required
def update_category(category_id):
    # Seguridad: Verificar propiedad
    if category.user_id != current_user.id:
        return {'error': 'No tienes permiso para editar esta categoría'}, 403

@categories_bp.route('/<int:category_id>/delete', methods=['DELETE'])
@login_required
def delete_category(category_id):
    # Seguridad: Verificar propiedad
    if category.user_id != current_user.id:
        return {'error': 'No tienes permiso para eliminar esta categoría'}, 403
```

#### ✓ Rutas de Autenticación (`/auth/`)

[app/auth/routes.py](app/auth/routes.py):

```python
@auth_bp.route('/logout')
@login_required
def logout():
    """Ruta para logout del usuario."""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))
```

---

### 3. **Ruta Dashboard Protegida**

En [app/__init__.py](app/__init__.py):

```python
@app.route('/dashboard')
@login_required
def dashboard():
    """
    Panel de control protegido del usuario.
    Requiere autenticación via @login_required decorator.
    Redirige automáticamente al login si el usuario no está autenticado.
    """
    return redirect(url_for('tasks.list_tasks'))
```

**Acceso:**
- `GET /dashboard` → Redirige a `/tasks/` (lista de tareas del usuario)
- Usuario NO autenticado → Redirige a `/auth/login?next=/dashboard`

---

### 4. **Plantilla Dashboard Mejorada**

[templates/dashboard.html](templates/dashboard.html):

```html
<!-- Mostrar el nombre del usuario autenticado -->
<p class="text-muted">Bienvenido, <strong>{{ current_user.username }}</strong></p>

<!-- Estadísticas de tareas -->
<div class="card text-center">
    <h5>Total</h5>
    <h2>{{ tasks|length }}</h2>
</div>

<div class="card text-center">
    <h5>Pendientes</h5>
    <h2>{{ tasks|selectattr('status', 'equalto', 'pendiente')|list|length }}</h2>
</div>

<!-- Verificar autenticación -->
{% if current_user.is_authenticated %}
    <p>Sesión activa: {{ current_user.username }}</p>
{% endif %}
```

---

## 📊 Tabla de Rutas

| Ruta | Método | Protección | Descripción |
|------|--------|-----------|-------------|
| `/` | GET | ✓ Condicional | Redirige según autenticación |
| `/dashboard` | GET | ✓ @login_required | Panel de control protegido |
| `/auth/register` | GET, POST | × | Registro de usuarios (público) |
| `/auth/login` | GET, POST | × | Inicio de sesión (público) |
| `/auth/logout` | GET | ✓ @login_required | Cerrar sesión |
| `/tasks/` | GET | ✓ @login_required | Lista de tareas |
| `/tasks/<id>` | GET | ✓ @login_required | Detalle de tarea |
| `/tasks/create` | POST | ✓ @login_required | Crear tarea |
| `/tasks/<id>/update` | POST | ✓ @login_required | Actualizar tarea |
| `/tasks/<id>/delete` | POST | ✓ @login_required | Eliminar tarea |
| `/users/` | GET | ✓ @login_required | Lista de usuarios |
| `/users/<id>` | GET | ✓ @login_required | Perfil de usuario |
| `/users/<id>/profile` | GET | ✓ @login_required | Detalles del usuario |
| `/categories/` | GET | ✓ @login_required | Lista de categorías |
| `/categories/<id>` | GET | ✓ @login_required | Detalle de categoría |
| `/categories/create` | POST | ✓ @login_required | Crear categoría |
| `/categories/<id>/update` | PUT | ✓ @login_required | Actualizar categoría |
| `/categories/<id>/delete` | DELETE | ✓ @login_required | Eliminar categoría |

---

## 🔐 Características de Seguridad

### 1. **Verificación de Propiedad**

Todas las rutas que modifican recursos verifican que pertenezcan al usuario:

```python
@tasks_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenece al usuario autenticado
    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
```

### 2. **Aislamiento de Datos**

Las consultas filtran automáticamente por usuario:

```python
# Solo obtener tareas del usuario autenticado
tasks = Task.query.filter_by(user_id=current_user.id).all()

# Solo obtener categorías del usuario autenticado
categories = Category.query.filter_by(user_id=current_user.id).all()
```

### 3. **Redirección Automática**

El decorador `@login_required` maneja automáticamente:
- Redirección a `/auth/login?next=/ruta-original`
- Redirección a la ruta original después de login
- Mensaje personalizado de autenticación requerida

---

## 🚀 Cómo Usar

### 1. **Acceder a Datos del Usuario Autenticado**

```python
from flask_login import current_user

@app.route('/profile')
@login_required
def profile():
    username = current_user.username
    email = current_user.email
    user_id = current_user.id
    return f"Perfil de {username}"
```

### 2. **En Plantillas Jinja2**

```html
<!-- Mostrar nombre del usuario -->
<p>Bienvenido, {{ current_user.username }}</p>

<!-- Verificar si está autenticado -->
{% if current_user.is_authenticated %}
    <a href="/auth/logout">Cerrar sesión</a>
{% else %}
    <a href="/auth/login">Iniciar sesión</a>
{% endif %}
```

### 3. **Proteger Nuevas Rutas**

```python
from flask_login import login_required, current_user

@app.route('/nueva-ruta')
@login_required
def nueva_ruta():
    user = current_user  # Usuario autenticado
    return render_template('template.html')
```

---

## 📝 Requisitos Cumplidos

- ✅ Usar decorator `@login_required` - Implementado en todas las rutas protegidas
- ✅ Redirigir usuarios no autenticados al login - Configurado en `login_manager.login_view`
- ✅ Crear página dashboard protegida - Rutas `/dashboard` y `/tasks/` protegidas

---

## 📚 Documentación Adicional

Ver [FLASK_LOGIN_GUIDE.md](FLASK_LOGIN_GUIDE.md) para:
- Guía detallada de configuración
- Ejemplos de código
- Flujo de autenticación
- Testing de rutas protegidas

---

## ✓ Verificación

Para verificar que la aplicación está correctamente configurada:

```bash
# Iniciar la aplicación
python run.py

# Intentar acceder a una ruta protegida sin autenticación
curl http://localhost:5000/tasks/

# Debería redirigir a:
# http://localhost:5000/auth/login?next=/tasks/

# Iniciar sesión en el navegador
# Luego acceder a la ruta nuevamente
```

---

**Fecha:** March 7, 2026  
**Framework:** Flask 3.0.0  
**Extensión:** Flask-Login 0.6.3
