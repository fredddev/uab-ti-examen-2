# Guía Flask-Migrate - Gestión de Migraciones de Base de Datos

## Estado Actual ✓

Tu proyecto ya tiene Flask-Migrate **completamente integrado**:

```python
# app/__init__.py
from flask_migrate import Migrate

migrate = Migrate()
migrate.init_app(app, db)  # Inicializado correctamente
```

## 📋 Requisitos

Todos están instalados (verificar en requirements.txt):
```
Flask-Migrate==4.0.7
Flask-SQLAlchemy==3.1.1
SQLAlchemy
```

---

## 🚀 Comandos Esenciales

### 1. INICIALIZAR MIGRACIONES (Primera vez)
```bash
flask db init
```
**Qué hace:**
- Crea la carpeta `migrations/` en la raíz del proyecto
- Prepara el entorno para rastrear cambios en modelos
- **Solo se ejecuta UNA VEZ**

**Resultado esperado:**
```
migrations/
  ├── env.py
  ├── script.py.mako
  ├── alembic.ini
  └── versions/
```

---

### 2. CREAR MIGRACIÓN (Después de modificar modelos)
```bash
flask db migrate -m "Descripción de cambios"
```

**Ejemplos:**
```bash
# Cambios iniciales de modelos
flask db migrate -m "Initial migration with User and Task models"

# Agregar nueva columna
flask db migrate -m "Add email column to User model"

# Cambiar relación
flask db migrate -m "Update Task-User relationship"
```

**Qué hace:**
- Detecta cambios en los modelos SQLAlchemy
- Genera un script de migración en `migrations/versions/`
- Crea archivo como: `001_initial_migration.py`
- **No modifica la BD, solo prepara los cambios**

---

### 3. APLICAR MIGRACIONES (Actualizar BD)
```bash
flask db upgrade
```

**Qué hace:**
- Ejecuta todas las migraciones pendientes
- Actualiza la estructura de la BD
- Modifica las tablas según los cambios detectados

**Aplicar una migración específica:**
```bash
flask db upgrade [revision]
```

---

### 4. REVERTIR CAMBIOS
```bash
# Revertir una migración
flask db downgrade

# Revertir a una revisión específica
flask db downgrade [revision]

# Ver historial de migraciones
flask db history
```

---

## 📝 Ciclo Completo de Trabajo

### Primer Setup
```bash
# 1. Inicializar migraciones
flask db init

# 2. Crear migración inicial (con los modelos actuales)
flask db migrate -m "Initial models setup"

# 3. Aplicar a la BD
flask db upgrade
```

### Desarrollo Normal
```bash
# 1. Modificar modelo en app/models/
# 2. Crear migración
flask db migrate -m "Add new feature"

# 3. Revisar el archivo generado en migrations/versions/
# 4. Aplicar cambios
flask db upgrade
```

---

## 🔍 Estructura de Migraciones

Después de `flask db init`, verás:

```
app/
├── models/
│   └── __init__.py (tus modelos)
└── migrations/           ← NUEVA CARPETA
    ├── versions/
    │   ├── 001_xxx.py
    │   ├── 002_xxx.py
    │   └── ...
    ├── env.py
    ├── script.py.mako
    └── alembic.ini
```

---

## 💡 Buenas Prácticas

### ✅ HACER
- Crear migraciones después de CADA cambio importante en modelos
- Usar mensajes descriptivos: `"Add user profile fields"`
- Revisar el archivo generado antes de `upgrade`
- Compartir la carpeta `migrations/` en control de versiones
- Hacer `upgrade` al cambiar rama o tirar cambios

### ❌ NO HACER
- Modificar directamente archivos en `migrations/versions/`
- Usar `flask db stamp` sin saber lo que haces
- Ignorar migraciones pendientes
- Crear migraciones sin probarlas

---

## 🐛 Troubleshooting

### Error: "No such table"
```bash
# Asegúrate de haber hecho upgrade
flask db upgrade
```

### Error: "Target database is not up to date"
```bash
# Crea una migración de los cambios
flask db migrate -m "Sync models"

# Luego aplica
flask db upgrade
```

### La migración no detecta cambios
```bash
# Asegúrate de:
# 1. Importar el modelo en app/models/__init__.py
# 2. El modelo heredar de db.Model
# 3. Esperar a que se guarde el archivo

# Intenta forzar:
flask db migrate --auto-generate -m "Description"
```

---

## 📚 Archivos Clave

- `app/__init__.py` - Inicialización de Migrate (ya configurado ✓)
- `app/config.py` - Configuración de BD (ya configurado ✓)
- `app/models/` - Define tus modelos aquí
- `migrations/` - Se crea con `flask db init`
- `.flaskenv` - Variables de entorno (opcional, crear si falta)

---

## 🔗 Referencia Rápida

```bash
# Setup inicial
flask db init               # Primera vez
flask db migrate -m "msg"   # Crear migración
flask db upgrade            # Aplicar cambios

# Consultas
flask db current            # Versión actual
flask db history            # Ver historial
flask db branches           # Ver ramas

# Revertir
flask db downgrade          # Volver atrás
flask db stamp [rev]        # Marcar sin aplicar
```

---

## ✨ Siguiente Paso

Para comenzar, ejecuta en la terminal:

```bash
cd c:\UNIVERSIDAD\ UAB\Taller\ de\ aplicaciones\ en\ internet\app\ grupal\app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

¡Y listo! 🎉
