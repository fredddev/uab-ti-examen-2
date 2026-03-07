# Configuración Flask-Migrate en run.py

## Código Actual (ya está correcto) ✓

```python
# run.py
import os
from dotenv import load_dotenv

# PRIMERO: Cargar variables de entorno
load_dotenv()

# SEGUNDO: Importar la app
from app import create_app, db

# Crear la aplicación
app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Contexto para la shell de Flask."""
    return {'db': db}


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', True)
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5001))
    
    app.run(host=host, port=port, debug=debug)
```

## Configuración en app/__init__.py ✓

```python
# app/__init__.py
from flask_migrate import Migrate  # ✓ Importado

db = SQLAlchemy()
migrate = Migrate()  # ✓ Inicializado

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # ✓ Inicializado correctamente
    db.init_app(app)
    migrate.init_app(app, db)  # Vincula Flask-Migrate con SQLAlchemy
    login_manager.init_app(app)
    
    register_blueprints(app)
    return app
```

## Configuración en app/config.py ✓

```python
# app/config.py
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # ✓ Recomendado para migration
```

---

## Ejemplo: Estructura de Modelos

Para que Flask-Migrate funcione correctamente, asegúrate de que tus modelos se importan en `app/models/__init__.py`:

```python
# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from app import db

# ✓ Importar TODOS los modelos aquí
from app.models.user import User
from app.models.task import Task
from app.models.category import Category

# Hacerlos disponibles desde models
__all__ = ['User', 'Task', 'Category']
```

```python
# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    tasks = db.relationship('Task', backref='user', lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## Variables de Entorno Recomendadas (.env)

```bash
# Base de Datos
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=flask_app

# Flask
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1

# Seguridad (cambiar en producción)
SECRET_KEY=dev-secret-key-change-in-production
```

---

## Checklist Inicial ✓

- [x] Flask-Migrate importado en app/__init__.py
- [x] migrate.init_app(app, db) configurado
- [x] SQLALCHEMY_DATABASE_URI configurado en app/config.py
- [x] Flask-Migrate en requirements.txt
- [x] Modelos definidos correctamente
- [ ] Ejecutar: `flask db init`
- [ ] Ejecutar: `flask db migrate -m "Initial migration"`
- [ ] Ejecutar: `flask db upgrade`

---

## Troubleshooting: Errores Comunes

### Error: "Can't locate revision identified by"
**Causa**: Migraciones no sincronizadas  
**Solución**:
```bash
flask db current          # Ver estado actual
flask db history          # Ver historial
flask db stamp head       # Sincronizar (úsalo con cuidado)
```

### Error: "ImportError" en migraciones
**Causa**: Modelos no importados en app/models/__init__.py  
**Solución**: Agrega tus modelos a `app/models/__init__.py`

### Base de datos no se actualiza
**Causa**: Falta ejecutar `flask db upgrade`  
**Solución**:
```bash
flask db upgrade          # Aplicar todas las migraciones
flask db upgrade -1       # Revertir última migración
```

---

## Comandos de Ayuda

```bash
flask db --help           # Ver todos los comandos disponibles
flask db init --help      # Ayuda específica de init
flask db migrate --help   # Ayuda específica de migrate
```
