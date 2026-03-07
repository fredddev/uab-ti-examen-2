# Implementación de Roles de Usuario en Flask

## Resumen

Se ha implementado un sistema de roles de usuario que permite:
- **admin**: Usuarios con acceso total a funciones administrativas
- **user**: Usuarios estándar con acceso limitado

El rol por defecto es `'user'`. Todos los usuarios nuevos se registran como `'user'`.

---

## 1. Modelo User (Actualizado)

El campo `role` ya está implementado en el modelo `User`:

```python
# En app/models/__init__.py
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin' o 'user'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
```

### Valores permitidos para `role`:
- `'admin'` - Usuario administrador con permisos especiales
- `'user'` - Usuario estándar (valor por defecto)

---

## 2. Decorators para Protección de Vistas

Se han creado dos decorators en `app/auth/decorators.py`:

### `@require_admin`

Protege una vista para que solo usuarios con rol `'admin'` puedan acceder.

**Ubicación:** `app/auth/decorators.py`

**Uso:**

```python
from flask import render_template
from app.auth.decorators import require_admin

@app.route('/admin/dashboard')
@require_admin
def admin_dashboard():
    """Solo accesible para usuarios admin."""
    return render_template('admin_dashboard.html')
```

**Comportamiento:**
- Si el usuario no está autenticado → Redirige a login
- Si el usuario no es admin → Redirige a tareas con mensaje de error
- Si el usuario es admin → Permite el acceso

### `@require_role(role)`

Decorator parametrizado para restringir a un rol específico (útil si se añaden más roles en el futuro).

**Uso:**

```python
from app.auth.decorators import require_role

@app.route('/moderador/panel')
@require_role('moderador')
def moderator_panel():
    """Solo accesible para usuarios con rol 'moderador'."""
    return render_template('moderator_panel.html')
```

---

## 3. Vistas Protegidas Implementadas

### Panel de Administración

**Ruta:** `/auth/admin`
**Decorador:** `@require_admin`
**Archivo:** `app/auth/routes.py` → función `admin_panel()`

**Ejemplo:**

```python
@auth_bp.route('/admin')
@require_admin
def admin_panel():
    """Panel de administración - solo para admins."""
    total_users = User.query.count()
    admin_users = User.query.filter_by(role='admin').count()
    regular_users = User.query.filter_by(role='user').count()
    
    users_list = User.query.all()
    
    return render_template(
        'admin_panel.html',
        total_users=total_users,
        admin_users=admin_users,
        regular_users=regular_users,
        users_list=users_list
    )
```

---

## 4. Cómo Cambiar el Rol de un Usuario

### Opción A: Usando Shell de Flask

```bash
# Acceder al shell de Flask
flask shell

# O si usas run.py:
python -c "from app import create_app, db; from app.models import User; app = create_app(); 
app.app_context().push(); 
user = User.query.filter_by(username='tu_username').first(); 
user.role = 'admin'; 
db.session.commit(); 
print(f'Usuario {user.username} ahora es {user.role}')"
```

### Opción B: Script Python

Crea `change_role.py`:

```python
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Buscar al usuario
    user = User.query.filter_by(username='nombre_usuario').first()
    
    if user:
        user.role = 'admin'  # Cambiar a 'admin'
        db.session.commit()
        print(f'✓ {user.username} ahora es {user.role}')
    else:
        print('✗ Usuario no encontrado')
```

Ejecutar:
```bash
python change_role.py
```

### Opción C: Interfaz Web (Recomendado para Producción)

Crear una vista en el panel de administración para cambiar roles:

```python
@auth_bp.route('/admin/users/<int:user_id>/change-role/<new_role>', methods=['POST'])
@require_admin
def change_user_role(user_id, new_role):
    """Cambiar el rol de un usuario."""
    if new_role not in ['admin', 'user']:
        flash('Rol inválido.', 'danger')
        return redirect(url_for('auth.admin_panel'))
    
    user = User.query.get_or_404(user_id)
    user.role = new_role
    db.session.commit()
    
    flash(f'Rol de {user.username} actualizado a {new_role}.', 'success')
    return redirect(url_for('auth.admin_panel'))
```

---

## 5. Ejemplos de Uso

### Proteger una vista con @require_admin

```python
from flask import Blueprint, render_template
from app.auth.decorators import require_admin

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/admin')
@require_admin
def admin_settings():
    """Solo administradores pueden acceder a la configuración."""
    return render_template('admin_settings.html')
```

### Verificar rol en una vista sin restricción

```python
from flask import render_template, current_user

@app.route('/dashboard')
@login_required
def dashboard():
    """Cualquier usuario autenticado puede ver el dashboard."""
    is_admin = current_user.role == 'admin'
    
    return render_template('dashboard.html', is_admin=is_admin)
```

### En Templates (Jinja2)

```html
<!-- Mostrar opciones solo para admins -->
{% if current_user.is_authenticated and current_user.role == 'admin' %}
    <a href="{{ url_for('auth.admin_panel') }}">Panel de Administración</a>
    <a href="{{ url_for('auth.change_user_role') }}">Administrar Usuarios</a>
{% endif %}
```

---

## 6. Verificación de Roles en el Código

### Con current_user

```python
from flask_login import current_user

if current_user.is_authenticated:
    if current_user.role == 'admin':
        # Hacer algo solo para admins
        pass
    elif current_user.role == 'user':
        # Hacer algo solo para users
        pass
```

### Con condicionales en templates

```html
<!-- Sección solo para admins -->
<section>
    {% if current_user.role == 'admin' %}
        <p>Contenido exclusivo para administradores</p>
    {% endif %}
</section>

<!-- Sección solo para users regulares -->
<section>
    {% if current_user.role == 'user' %}
        <p>Contenido para usuarios normales</p>
    {% endif %}
</section>
```

---

## 7. Migraciones de Base de Datos

Si esta es la primera vez que usas el campo `role`, genera una migración:

```bash
# Crear migración automática
flask db migrate -m "Add role field to User model"

# Aplicar la migración
flask db upgrade
```

Si la migración no detecta cambios automáticamente, crea una migración manual en `migrations/versions/`:

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('user', sa.Column('role', sa.String(20), nullable=False, server_default='user'))

def downgrade():
    op.drop_column('user', 'role')
```

---

## 8. Checklist de Implementación

- ✅ Campo `role` en modelo `User`
- ✅ Decorator `@require_admin` creado
- ✅ Decorator `@require_role(role)` creado
- ✅ Ruta de admin panel implementada: `/auth/admin`
- ✅ Métodos para verificar roles en código

### Próximos pasos (Opcional):

- [ ] Crear template `admin_panel.html`
- [ ] Implementar interfaz web para cambiar roles
- [ ] Agregar más vistas protegidas según necesidades
- [ ] Crear logs de auditoría para cambios de rol
- [ ] Agregar permisos más granulares si lo requieren

---

## 9. Archivos Nuevos/Modificados

| Archivo | Cambio |
|---------|--------|
| `app/models/__init__.py` | Campo `role` ya existe en User |
| `app/auth/decorators.py` | **NUEVO** - Decorators para protección |
| `app/auth/routes.py` | Agregada ruta `/auth/admin` con `@require_admin` |
| `ROLES_IMPLEMENTATION.md` | **NUEVO** - Esta guía |

---

## 10. Troubleshooting

### Error: ImportError: cannot import name 'require_admin'

Asegúrate de que el archivo `app/auth/decorators.py` existe y está correctamente importado.

```python
# Correcto:
from app.auth.decorators import require_admin

# No funciona:
from app.decorators import require_admin  # ❌ Ruta incorrecta
```

### Usuario admin sin acceso al panel

1. Verifica que el usuario tiene `role = 'admin'` en la BD
2. Cierra sesión y vuelve a iniciar
3. Revisa los logs para ver si hay errores

### Template admin_panel.html no encontrado

Crea el template en `templates/admin_panel.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Panel de Administración</h1>

<div class="row">
    <div class="col-md-4">
        <div class="card">
            <h3>Total de Usuarios</h3>
            <p>{{ total_users }}</p>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <h3>Administradores</h3>
            <p>{{ admin_users }}</p>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <h3>Usuarios Normales</h3>
            <p>{{ regular_users }}</p>
        </div>
    </div>
</div>

<h2>Lista de Usuarios</h2>
<table class="table">
    <thead>
        <tr>
            <th>Usuario</th>
            <th>Email</th>
            <th>Rol</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users_list %}
        <tr>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

---

## Resumen

**Implementación completada:**
- ✅ Campo `role` en modelo User (default: 'user')
- ✅ Decorators `@require_admin` y `@require_role()` para protección
- ✅ Ruta protegida `/auth/admin` con ejemplo funcional
- ✅ Documentación y ejemplos de uso

**Para proteger una vista de admin:** Simplemente agrega `@require_admin` encima de tu función.
