# Configuración de MySQL

## Requisitos

- MySQL Server instalado y ejecutándose
- PyMySQL instalado (incluido en requirements.txt)

## Pasos para Configurar la Base de Datos MySQL

### 1. Crear la Base de Datos

Abrir MySQL CLI o MySQL Workbench y ejecutar:

```sql
CREATE DATABASE flask_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configurar las Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5001

SECRET_KEY=tu-clave-secreta-super-segura

DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=flask_app
```

**Notas importantes:**
- `DB_USER`: Usuario de MySQL (default: root)
- `DB_PASSWORD`: Contraseña de MySQL
- `DB_HOST`: Host donde corre MySQL (default: localhost)
- `DB_PORT`: Puerto MySQL (default: 3306)
- `DB_NAME`: Nombre de la base de datos a usar

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.7
- Flask-Login 0.6.3
- PyMySQL 1.1.0 (driver MySQL)
- python-dotenv 1.0.0

### 4. Inicializar las Migraciones

```bash
flask db init
```

Esto crea la carpeta `migrations/` para controlar versiones de la BD.

### 5. Crear Primera Migración

```bash
flask db migrate -m "Initial migration: create users, categories and tasks tables"
```

### 6. Aplicar las Migraciones

```bash
flask db upgrade
```

Esto crea las tablas en MySQL.

## Estructura SQLAlchemy

### Importar `db` en los Modelos

En `app/models/__init__.py`:

```python
from app import db  # Importar la instancia de SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
```

### Crear Nuevos Modelos

Archivo: `app/models/mi_modelo.py`

```python
from app import db

class MiModelo(db.Model):
    __tablename__ = 'mi_modelo'  # Nombre de la tabla en BD
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    creado = db.Column(db.DateTime, default=db.func.current_timestamp())
```

## Ejecutar la Aplicación

```bash
python run.py
```

## Verificar Conexión

En Flask Shell:

```bash
flask shell
```

Dentro del shell:

```python
>>> from app import db
>>> db
<SQLAlchemy engine='mysql+pymysql://root:password@localhost:3306/flask_app'>
>>> db.session.execute(db.text('SELECT 1')).scalar()
1
```

Si ves `1`, la conexión es exitosa ✅

## Troubleshooting

### Error: "No module named 'MySQLdb'"
Solución: Usar `PyMySQL` está incluido. Si aún hay problemas:
```bash
pip install PyMySQL
```

### Error: "Access denied for user"
Solución: Verificar credenciales en `.env`:
- Usuario correcto
- Contraseña correcta
- Host correcto

### Error: "Unknown database 'flask_app'"
Solución: Asegurar que la DB fue creada en MySQL:
```sql
CREATE DATABASE flask_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Error: "Connection refused"
Solución: Asegurar que MySQL está ejecutándose:
```bash
# Windows
mysql --version  # Verificar instalación

# Linux
sudo systemctl start mysql

# macOS
mysql.server start
```

## Pool Connection

La configuración incluye optimizaciones:

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,           # Máximo 10 conexiones en el pool
    'pool_recycle': 3600,      # Reciclar conexiones cada 1 hora
    'pool_pre_ping': True,     # Verificar conexiones antes de usar
}
```

Esto previene errores de conexiones expiradas.

## Usar la Aplicación

```python
# En run.py o cualquier archivo
from app import create_app, db

app = create_app()

with app.app_context():
    # Ahora puedes usar db
    from app.models import User
    
    # Crear usuario
    user = User(username='admin', email='admin@app.com', password='hash123')
    db.session.add(user)
    db.session.commit()
```

## Referencias

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/)
