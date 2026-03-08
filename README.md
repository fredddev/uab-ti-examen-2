# TaskApp - Gestor de Tareas

Una aplicación web simple para gestionar tareas del día a día.

---

## 🚀 Cómo Levantar la Aplicación (Primera Vez)

### Paso 1: Instalar Dependencias

Abre PowerShell en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

> ⏱️ Esto puede tomar unos 2-3 minutos la primera vez.

---

### Paso 2: Configurar la Base de Datos

#### Si es la PRIMERA VEZ:

1. Abre el archivo `.env` en la carpeta principal
2. Busca la línea `DB_PASSWORD=`
3. Cambia `123456` por la contraseña de tu MySQL

**Ejemplo:**
```env
DB_USER=root
DB_PASSWORD=tu_password_aqui  ← Cambia esto
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_tareas_uab
```

4. Guarda el archivo

---

### Paso 3: Inicializar la Base de Datos

En PowerShell, ejecuta:

```bash
flask db upgrade
```

> Esto crea las tablas necesarias y los usuarios de prueba automáticamente.

---

### Paso 4: Ejecutar la Aplicación

En PowerShell, ejecuta:

```bash
python run.py
```

Deberías ver algo como:
```
 * Running on http://127.0.0.1:5001
```

---

## 🌐 Acceder a la Aplicación

Abre tu navegador y ve a:

```
http://localhost:5001
```

> Si ves un error de conexión, asegúrate que MySQL está corriendo.

---

## 👤 Usuarios y Contraseñas

La aplicación viene con 2 usuarios de prueba listos para usar:

### Usuario Administrador
```
👤 Usuario: admin
🔐 Contraseña: admin123
⚙️ Acceso: Panel de Administración + Todas las funciones
```

### Usuario Normal
```
👤 Usuario: user
🔐 Contraseña: user123456
📋 Acceso: Dashboard de tareas + Funciones básicas
```

---

## 🎯 Qué Puedes Hacer

### Con usuario "admin":
- ✅ Ver panel de administración
- ✅ Listar todos los usuarios
- ✅ Gestionar tareas
- ✅ Crear categorías

### Con usuario "user":
- ✅ Crear y gestionar tus tareas
- ✅ Ver tu perfil
- ✅ Crear categorías

---

## 📍 Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `http://localhost:5001` | Página de inicio |
| `http://localhost:5001/auth/login` | Iniciar sesión |
| `http://localhost:5001/auth/register` | Registrar nueva cuenta |
| `http://localhost:5001/auth/admin` | Panel de administración (solo admin) |
| `http://localhost:5001/tasks` | Mis tareas |
| `http://localhost:5001/profile` | Mi perfil |

---

## 🆘 Soluciona Problemas

### "No se puede conectar a la base de datos"
- ✓ Verifica que MySQL está corriendo
- ✓ Verifica el archivo `.env` con los datos correctos
- ✓ Asegúrate que la base de datos `db_tareas_uab` existe

### "Error: No se encuentra flask"
- ✓ Ejecuta `pip install -r requirements.txt` nuevamente

### "Puerto 5001 ya está en uso"
- ✓ Cierra la aplicación anterior o cambia el puerto en `.env`

---

## 📂 Estructura de Carpetas

```
project/
├── app/                 # Código principal de la app
├── templates/           # Páginas HTML
├── migrations/          # Base de datos
├── run.py              # Archivo para iniciar la app
├── requirements.txt    # Dependencias necesarias
├── .env                # Configuración (edita esto)
└── README.md           # Este archivo
```

---

## 💾 Cambiar la Contraseña de los Usuarios de Prueba

Si quieres cambiar las contraseñas, abre PowerShell en la carpeta del proyecto:

```bash
python manage_roles.py set <usuario> admin
```

---

## ✅ Checklist Rápido

- [ ] Python 3.8+ instalado
- [ ] Archivo `.env` configurado con credenciales de MySQL
- [ ] MySQL corriendo
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] `flask db upgrade` ejecutado
- [ ] `python run.py` corriendo
- [ ] Navegador abierto en `http://localhost:5001`

---

## 📞 ¿Necesitas Ayuda?

1. Verifica que seguiste todos los pasos en orden
2. Mira el archivo `ROLES_IMPLEMENTATION.md` para info sobre roles
3. Revisa el archivo `ADMIN_PANEL_GUIDE.md` para el panel admin

---

**¡Listo! Ahora puedes gestionar tus tareas. Disfruta la app! 🎉**

🏷️ Módulo Categorías

Gestiona todas las categorías de tus tareas, desde la creación hasta la búsqueda, con control de permisos según el tipo de usuario.

🚀 Funcionalidades Implementadas

➕ Crear Categoría

Solo administradores pueden crear.

Formulario con validación: nombre obligatorio y descripción opcional.

Redirige automáticamente a la lista al guardar.

📝 Editar Categoría

Administradores pueden actualizar nombre y descripción.

Los campos no modificados permanecen intactos.

Redirección a la lista tras guardar.

🗑️ Eliminar Categoría

Confirmación de eliminación para evitar errores.

Solo administradores pueden eliminar.

🔍 Buscar Categoría

Campo de búsqueda por nombre.

Filtrado dinámico usando SQLAlchemy (ilike).

Resultados se muestran directamente en la tabla.

📋 Listado de Categorías

Tabla con ID, nombre, descripción y acciones.

Botones de editar y eliminar para cada categoría.

Integración con Bootstrap 5 para un diseño limpio y responsive.

🛠️ Lo que aprendimos

✅ Crear un módulo CRUD completo en Flask.

✅ Control de permisos basado en roles (admin vs usuario normal).

✅ Formularios con CSRF seguro y dinámico.

✅ Búsqueda y filtrado eficiente con SQLAlchemy.

✅ Plantillas limpias y responsive usando Jinja2 y Bootstrap.

✅ UX consistente: redirecciones y confirmaciones que guían al usuario.
