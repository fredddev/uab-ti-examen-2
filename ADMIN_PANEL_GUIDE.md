# Acceso al Panel de Administración desde la UI

## Cómo Navegar al Panel de Admin

Si eres un usuario con rol **admin**, puedes acceder al panel de administración de dos formas:

---

## 📱 Forma 1: Desde el Dropdown del Usuario (RECOMENDADO)

1. **Inicia sesión** con tu usuario admin
   - Username: `admin`
   - Password: `admin123`

2. **Mira la barra de navegación** en la parte superior derecha
   
3. **Haz clic en tu nombre de usuario** (verás un dropdown)
   - Notarás que aparece un **badge rojo "Admin"** al lado de tu nombre

4. **En el dropdown, haz clic en:**
   - ⚙️ **Panel de Administración**

5. ¡Listo! Serás redirigido a `/auth/admin`

---

## 🔗 Forma 2: URL Directa

Si prefieres ir directamente:

```
http://localhost:5001/auth/admin
```

---

## ✅ Elementos de UI Actualizados

### Barra de Navegación (Navbar)
- ✓ Se muestra un **badge "Admin"** rojo junto a tu nombre
- ✓ En el dropdown aparece la opción **"⚙️ Panel de Administración"**
- ✓ Solo visible para usuarios con rol `admin`

### Panel de Administración
- ✓ Título con icono: **"⚙️ Panel de Administración"**
- ✓ Badge "Admin" en la esquina superior derecha
- ✓ Tarjetas de estadísticas (Total, Admins, Usuarios normales)
- ✓ Tabla completa de usuarios con detalles

---

## 🔒 Seguridad

Si eres un usuario **normal** (rol `user`):
- ❌ No verás el badge "Admin"
- ❌ No verás la opción "Panel de Administración"
- ❌ Si intentas acceder a `/auth/admin`, serás redirigido a la página principal
- ❌ Verás un mensaje: "No tienes permisos para acceder a esta página"

---

## 📊 Información Visible en el Panel

Una vez dentro del panel de administración, verás:

1. **Estadísticas:**
   - Total de usuarios registrados
   - Cantidad de administradores
   - Cantidad de usuarios normales

2. **Tabla de Usuarios:**
   - ID del usuario
   - Nombre de usuario
   - Email
   - Rol (Admin / User)
   - Fecha de creación
   - Indicador "Tú" si es tu usuario

---

## 💡 Tips

- El dropdown del usuario es **responsive** y funciona en móviles
- El enlace del panel de admin se carga automáticamente solo para admins
- No requiere recargar la página, funciona con JavaScript de Bootstrap

---

## Próximas Mejoras (Opcional)

Si quieres agregar más funcionalidades al panel:
- [ ] Botón para cambiar roles de usuarios
- [ ] Eliminar usuarios
- [ ] Exportar lista de usuarios
- [ ] Ver estadísticas de tareas
- [ ] Administrar categorías
