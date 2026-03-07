# Flask Task Manager

Aplicación web para gestionar tareas usando Flask con buenas prácticas de arquitectura.

## Estructura del Proyecto

```
project/
├── app/
│   ├── __init__.py          # Factory function create_app()
│   ├── config.py            # Configuración de la aplicación
│   ├── models/
│   │   └── __init__.py      # Modelos de BD (User, Category, Task)
│   ├── auth/
│   │   └── __init__.py      # Blueprint de autenticación
│   ├── users/
│   │   └── __init__.py      # Blueprint de usuarios
│   ├── tasks/
│   │   └── __init__.py      # Blueprint de tareas
│   ├── categories/
│   │   └── __init__.py      # Blueprint de categorías
│   ├── templates/           # Templates HTML
│   └── static/              # Archivos estáticos (CSS, JS, imágenes)
├── migrations/              # Migraciones de base de datos (Flask-Migrate)
├── run.py                   # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias de Python
└── .gitignore              # Archivo de gitignore
```

## Características

- ✅ **Arquitectura modular**: Uso de blueprints para organizar funcionalidades
- ✅ **Factory Pattern**: Función `create_app()` para inicializar la aplicación
- ✅ **Gestión de BD**: Flask-SQLAlchemy para ORM
- ✅ **Migraciones**: Flask-Migrate para control de versiones de BD
- ✅ **Autenticación**: Flask-Login para sesiones de usuario
- ✅ **Configuración flexible**: Diferentes configs para dev, producción y tests
- ✅ **Modelos predefinidos**: User, Category, Task

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Crear archivo .env (opcional)**
   ```
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=tu-clave-secreta-aqui
   DATABASE_URL=sqlite:///app.db
   ```

## Uso

### Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en `http://127.0.0.1:5001`

### Inicializar migraciones

```bash
flask db init
```

### Crear una migración

```bash
flask db migrate -m "Descripción del cambio"
```

### Aplicar migraciones

```bash
flask db upgrade
```

### Flask Shell

Para interactuar con la aplicación en una shell:

```bash
flask shell
```

## Modelos de Base de Datos

### User
- id (Integer, PK)
- username (String, unique)
- email (String, unique)
- password (String)
- created_at (DateTime)
- updated_at (DateTime)

### Category
- id (Integer, PK)
- name (String)
- description (Text)
- user_id (FK)
- created_at (DateTime)

### Task
- id (Integer, PK)
- title (String)
- description (Text)
- completed (Boolean)
- due_date (DateTime)
- priority (String: low, medium, high)
- user_id (FK)
- category_id (FK)
- created_at (DateTime)
- updated_at (DateTime)

## Próximos Pasos

1. **Implementar rutas**: Completar las funciones en cada blueprint
2. **Templates HTML**: Crear templates en `app/templates/`
3. **Estilos CSS**: Agregar estilos en `app/static/css/`
4. **Autenticación**: Implementar login y registro con Flask-Login
5. **Validación**: Usar WTForms para validación de formularios
6. **API REST**: Convertir a API REST con JSONs

## Variables de Entorno

- `FLASK_ENV`: development, production, testing (default: development)
- `FLASK_DEBUG`: True/False para activar modo debug (default: True)
- `FLASK_HOST`: Host donde correr la app (default: 127.0.0.1)
- `FLASK_PORT`: Puerto donde correr la app (default: 5000)
- `SECRET_KEY`: Clave secreta para sesiones (default: dev-secret-key)
- `DATABASE_URL`: URL de conexión a BD (default: sqlite:///app.db)

## Soporte de Tecnologías

- **Flask 2.3.3**: Framework web micro
- **Flask-SQLAlchemy 3.0.5**: ORM para gestión de BD
- **Flask-Migrate 4.0.5**: Control de versiones de esquema BD
- **Flask-Login 0.6.2**: Gestión de autenticación y sesiones
- **python-dotenv 1.0.0**: Gestión de variables de entorno

## Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

---

**Nota**: Recuerda cambiar la `SECRET_KEY` en producción y configurar `SESSION_COOKIE_SECURE = True` cuando uses HTTPS.
