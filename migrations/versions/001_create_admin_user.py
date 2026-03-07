"""Create default admin and user users.

Revision ID: 001_create_admin_user
Revises: fe0470f7e3cf
Create Date: 2026-03-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision = '001_create_admin_user'
down_revision = 'fe0470f7e3cf'
branch_labels = None
depends_on = None


def upgrade():
    """Crear o actualizar los usuarios admin y user."""
    
    # Conexión a la base de datos
    connection = op.get_bind()
    
    # ===== USUARIO ADMIN =====
    # Verificar si el usuario admin ya existe
    result = connection.execute(
        sa.text("SELECT id FROM user WHERE username = 'admin'")
    )
    
    admin_user = result.fetchone()
    
    if admin_user:
        # Si existe, actualizar la contraseña
        password_hash = generate_password_hash('admin123')
        connection.execute(
            sa.text(
                "UPDATE user SET password_hash = :password, role = 'admin' WHERE username = 'admin'"
            ),
            {"password": password_hash}
        )
        print("✓ Usuario admin actualizado")
    else:
        # Si no existe, crear el usuario
        password_hash = generate_password_hash('admin123')
        
        connection.execute(
            sa.text(
                """INSERT INTO user (username, email, password_hash, role, created_at, updated_at) 
                   VALUES (:username, :email, :password, :role, NOW(), NOW())"""
            ),
            {
                "username": "admin",
                "email": "admin@admin.com",
                "password": password_hash,
                "role": "admin"
            }
        )
        print("✓ Usuario admin creado")
    
    # ===== USUARIO USER =====
    # Verificar si el usuario user ya existe
    result = connection.execute(
        sa.text("SELECT id FROM user WHERE username = 'user'")
    )
    
    user_user = result.fetchone()
    
    if user_user:
        # Si existe, actualizar la contraseña
        password_hash = generate_password_hash('user123456')
        connection.execute(
            sa.text(
                "UPDATE user SET password_hash = :password, role = 'user' WHERE username = 'user'"
            ),
            {"password": password_hash}
        )
        print("✓ Usuario user actualizado")
    else:
        # Si no existe, crear el usuario
        password_hash = generate_password_hash('user123456')
        
        connection.execute(
            sa.text(
                """INSERT INTO user (username, email, password_hash, role, created_at, updated_at) 
                   VALUES (:username, :email, :password, :role, NOW(), NOW())"""
            ),
            {
                "username": "user",
                "email": "user@user.com",
                "password": password_hash,
                "role": "user"
            }
        )
        print("✓ Usuario user creado")


def downgrade():
    """Eliminar los usuarios admin y user en caso de hacer downgrade."""
    
    connection = op.get_bind()
    
    # Eliminar los usuarios
    connection.execute(
        sa.text("DELETE FROM user WHERE username IN ('admin', 'user')")
    )
    print("✓ Usuarios admin y user eliminados")
