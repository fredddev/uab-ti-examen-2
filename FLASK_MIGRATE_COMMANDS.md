# 🚀 Comandos Flask-Migrate - Referencia Rápida

## 📍 Ubicación: Ejecutar en la carpeta raíz del proyecto
```
C:\UNIVERSIDAD UAB\Taller de aplicaciones en internet\app grupal\app>
```

---

## 1️⃣ PRIMERA VEZ - Setup Inicial

### Paso 1: Inicializar migraciones
```bash
flask db init
```
**Resultado**: Crea carpeta `migrations/`

### Paso 2: Generar migración inicial
```bash
flask db migrate -m "Initial migration with User and Task models"
```
**Resultado**: Crea archivo en `migrations/versions/`

### Paso 3: Aplicar cambios a BD
```bash
flask db upgrade
```
**Resultado**: Actualiza la base de datos MySQL

---

## 2️⃣ DESARROLLO NORMAL - Ciclo Repetido

### Después de modificar un modelo:

```bash
# 1. Detectar cambios
flask db migrate -m "Add email column to User"

# 2. Aplicar cambios
flask db upgrade
```

---

## 3️⃣ COMANDOS ÚTILES

| Comando | Descripción |
|---------|-------------|
| `flask db init` | Inicializar migraciones (UNA SOLA VEZ) |
| `flask db migrate -m "msg"` | Crear nueva migración |
| `flask db upgrade` | Aplicar migraciones a BD |
| `flask db downgrade` | Revertir última migración |
| `flask db current` | Ver versión actual de BD |
| `flask db history` | Ver historial de migraciones |
| `flask db branches` | Ver ramas de migraciones |
| `flask db merge [revisions]` | Fusionar ramas divergentes |

---

## 4️⃣ EJEMPLOS DE USO REAL

### Ejemplo A: Agregar columna a tabla existente
```bash
# 1. Modificas app/models/user.py
#    Agregas: email = db.Column(db.String(120), unique=True)

# 2. Crear migración
flask db migrate -m "Add email column to User model"

# 3. Revisar archivo generado
#    cat migrations/versions/001_*.py

# 4. Aplicar cambios
flask db upgrade
```

### Ejemplo B: Agregar nueva tabla
```bash
# 1. Crear nuevo modelo en app/models/
# 2. Importar en app/models/__init__.py
# 3. Crear migración
flask db migrate -m "Add Product model"

# 4. Aplicar
flask db upgrade
```

### Ejemplo C: Cambiar relación entre tablas
```bash
# 1. Modificar relación en modelos
# 2. Generar migración
flask db migrate -m "Update Task-User relationship"

# 3. Aplicar
flask db upgrade
```

---

## 5️⃣ WORKFLOW COMPLETO EN EQUIPO

```bash
# Compañero A - Modifica modelo
# Compañero A ejecuta:
flask db migrate -m "Add payment status"
flask db upgrade
git push migrations/  # Comparte cambios

# Compañero B - Recibe cambios
git pull
flask db upgrade      # Aplica migraciones

# Compañero B - Hace su cambio
flask db migrate -m "Add refund reason"
flask db upgrade
git push migrations/
```

---

## 6️⃣ SINCRONIZAR CON RAMA DE GIT

```bash
# Si cambias de rama de git:
git checkout feature/nueva-tabla

# Asegúrate de estar al día:
flask db upgrade

# Si hay cambios pendientes:
flask db upgrade head
```

---

## 7️⃣ REVERTIR CAMBIOS (Cuidado)

```bash
# Revertir 1 migración
flask db downgrade

# Revertir a una versión específica
flask db downgrade [hash_de_revisión]

# Ver el hash en history
flask db history
```

---

## ⚠️ ERRORES FRECUENTES

### Error 1: "Can't import module"
```bash
# Solución: Verificar que el modelo está en app/models/__init__.py
```

### Error 2: "No changes detected"
```bash
# Solución: El modelo debe heredar de db.Model
class MyModel(db.Model):
    __tablename__ = 'my_table'
    # ...
```

### Error 3: "Target database is not up to date"
```bash
# Solución:
flask db migrate -m "Sync"
flask db upgrade
```

---

## 📝 TEMPLATE - Mensaje de Migración

```bash
# Bien descriptivo:
flask db migrate -m "Add user authentication with email verification"

# No descriptivo:
flask db migrate -m "Update"  # ❌ Evitar
```

---

## 🔐 SEGURIDAD EN PRODUCCIÓN

```bash
# En producción, revisa SIEMPRE antes de upgrade:
cat migrations/versions/latest_migration.py

# Luego aplica:
flask db upgrade
```

---

## 📚 DOCUMENTACIÓN

- Guía completa: [FLASK_MIGRATE_GUIDE.md](FLASK_MIGRATE_GUIDE.md)
- Configuración: [FLASK_MIGRATE_CONFIG.md](FLASK_MIGRATE_CONFIG.md)
- Modelos ejemplo: [MODELS_EXAMPLES.md](MODELS_EXAMPLES.md)

---

## 🎯 Siguientes Pasos

1. Ejecutar en terminal: `flask db init`
2. Ejecutar: `flask db migrate -m "Initial migration"`
3. Ejecutar: `flask db upgrade`
4. Verificar que las tablas se crearon en MySQL
5. ¡A desarrollar! 🚀
