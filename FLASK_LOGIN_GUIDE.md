# Guía: Protección de Rutas con Flask-Login

## Overview

Este documento explica cómo está configurada la protección de rutas en la aplicación Flask usando Flask-Login.

---

## 1. Configuración Inicial de Flask-Login

### En `app/__init__.py`

```python
from flask_login import LoginManager

# Inicializar el LoginManager
login_manager = LoginManager()

# En create_app():
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Ruta a la que redirigir si no está autenticado
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

# Registrar el user_loader callback
@login_manager.user_loader
def load_user(user_id):
    """Carga un usuario por su ID."""
    return User.query.get(int(user_id))
```

### Modelo User

El modelo `User` hereda de `UserMixin` de Flask-Login:

```python
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # ... otros campos
```

---

## 2. Decorador @login_required

El decorador `@login_required` protege las rutas para que solo usuarios autenticados puedan acceder.

### Sintaxis

```python
from flask_login import login_required

@app.route('/protected')
@login_required
def protected_route():
    return "Esta ruta está protegida"
```

### Comportamiento

1. **Usuario autenticado**: La ruta se ejecuta normalmente
2. **Usuario NO autenticado**: 
   - Es redirigido a `login_manager.login_view` (por defecto: `auth.login`)
   - Se muestra `login_manager.login_message`
   - La URL original se pasa como parámetro `next` (ej: `/auth/login?next=/dashboard`)

---

## 3. Rutas Protegidas en la Aplicación

### Ruta Raíz `/`

```python
@app.route('/')
def index():
    """Redirige al login o al dashboard según autenticación."""
    if current_user.is_authenticated:
        return redirect(url_for('tasks.list_tasks'))
    return redirect(url_for('auth.login'))
```

### Ruta Dashboard `/dashboard`

```python
@app.route('/dashboard')
@login_required
def dashboard():
    """Panel de control protegido del usuario."""
    return redirect(url_for('tasks.list_tasks'))
```

### Rutas de Autenticación (`/auth/`)

- `GET /auth/register` - Formulario de registro (público)
- `POST /auth/register` - Procesar registro (público)
- `GET /auth/login` - Formulario de login (público)
- `POST /auth/login` - Procesar login (público)
- `GET /auth/logout` - **Cerrar sesión (PROTEGIDO)** ✓

```python
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))
```

### Rutas de Tareas (`/tasks/`) - TODAS PROTEGIDAS

```python
@tasks_bp.route('/')
@login_required
def list_tasks():
    """Lista las tareas del usuario autenticado."""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks, categories=categories)

@tasks_bp.route('/<int:task_id>')
@login_required
def get_task(task_id):
    """Obtiene una tarea específica (solo si pertenece al usuario)."""
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No tienes permiso para ver esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('task_detail.html', task=task)

@tasks_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    """Crea una nueva tarea para el usuario autenticado."""
    # ...

@tasks_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    """Actualiza una tarea (solo si pertenece al usuario)."""
    # ...

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Elimina una tarea (solo si pertenece al usuario)."""
    # ...
```

### Rutas de Usuarios (`/users/`) - TODAS PROTEGIDAS

```python
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

### Rutas de Categorías (`/categories/`) - TODAS PROTEGIDAS

```python
@categories_bp.route('/')
@login_required
def list_categories():
    """Lista las categorías del usuario autenticado."""
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return {'message': 'Categories list', 'data': [...]}, 200

@categories_bp.route('/<int:category_id>')
@login_required
def get_category(category_id):
    """Obtiene una categoría específica (solo si pertenece al usuario)."""
    category = Category.query.get_or_404(category_id)
    if category.user_id != current_user.id:
        return {'error': 'No tienes permiso para ver esta categoría'}, 403
    return {'message': f'Category {category_id}', 'data': ...}, 200

@categories_bp.route('/create', methods=['POST'])
@login_required
def create_category():
    """Crea una nueva categoría para el usuario autenticado."""
    # ...

@categories_bp.route('/<int:category_id>/update', methods=['PUT'])
@login_required
def update_category(category_id):
    """Actualiza una categoría (solo si pertenece al usuario)."""
    # ...

@categories_bp.route('/<int:category_id>/delete', methods=['DELETE'])
@login_required
def delete_category(category_id):
    """Elimina una categoría (solo si pertenece al usuario)."""
    # ...
```

---

## 4. Usar `current_user` en Rutas

Para acceder al usuario autenticado en una ruta:

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

En plantillas Jinja2:

```html
<!-- Mostrar información del usuario autenticado -->
<p>Bienvenido, {{ current_user.username }}</p>

<!-- Verificar si está autenticado -->
{% if current_user.is_authenticated %}
    <a href="/logout">Cerrar sesión</a>
{% else %}
    <a href="/login">Iniciar sesión</a>
{% endif %}
```

---

## 5. Control de Acceso Granular

Además del decorador `@login_required`, la aplicación verifica que los recursos pertenezcan al usuario:

```python
@tasks_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Verificar que la tarea pertenece al usuario autenticado
    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    # ... continuar con la actualización
```

---

## 6. Flujo de Autenticación

### Login

1. Usuario accede a `/auth/login`
2. Ingresa credenciales (username y password)
3. Se valida contra la base de datos
4. Se llama a `login_user(user)` de Flask-Login
5. Se crea una sesión en el navegador
6. Se redirige a la siguiente página (parámetro `next`) o al dashboard

```python
if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    
    if user and user.check_password(form.password.data):
        login_user(user, remember=False)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('tasks.list_tasks'))
```

### Logout

1. Usuario accede a `/auth/logout`
2. Se llama a `logout_user()`
3. Se elimina la sesión
4. Se redirige a la página de login

```python
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))
```

---

## 7. Mensajes de Error

Cuando un usuario no autenticado intenta acceder a una ruta protegida:

1. Es redirigido a `/auth/login?next=/ruta/protegida`
2. Se muestra el mensaje: "Por favor inicia sesión para acceder a esta página."
3. Después de iniciar sesión, es redirigido a `/ruta/protegida`

---

## 8. Resumén de Rutas Públicas vs Protegidas

### Públicas (sin autenticación)
- `GET /` - Redirige según autenticación
- `GET /auth/register` - Formulario de registro
- `POST /auth/register` - Procesar registro
- `GET /auth/login` - Formulario de login
- `POST /auth/login` - Procesar autenticación

### Protegidas (requieren autenticación)
- ✓ `GET /dashboard` - Panel de control
- ✓ `GET /tasks/` - Lista de tareas
- ✓ `GET /tasks/<id>` - Detalle de tarea
- ✓ `POST /tasks/create` - Crear tarea
- ✓ `POST /tasks/<id>/update` - Actualizar tarea
- ✓ `POST /tasks/<id>/delete` - Eliminar tarea
- ✓ `GET /users/` - Lista de usuarios
- ✓ `GET /users/<id>` - Perfil de usuario
- ✓ `GET /categories/` - Lista de categorías
- ✓ `POST /categories/create` - Crear categoría
- ✓ `PUT /categories/<id>/update` - Actualizar categoría
- ✓ `DELETE /categories/<id>/delete` - Eliminar categoría
- ✓ `GET /auth/logout` - Cerrar sesión

---

## 9. Testing

Para probar rutas protegidas:

```bash
# Sin autenticación - Debería redirigir a login
curl -c cookies.txt http://localhost:5000/dashboard

# Con autenticación
curl -c cookies.txt -X POST http://localhost:5000/auth/login \
  -d "username=testuser&password=testpass"

curl -b cookies.txt http://localhost:5000/dashboard
```

---

## 10. Dependencias Requeridas

```
Flask==3.0.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
werkzeug  (para hash de contraseñas)
```

Ver `requirements.txt` para la lista completa.

---

## Referencias

- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Flask Security Considerations](https://flask.palletsprojects.com/security/)
