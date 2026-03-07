"""
Script para crear un usuario administrador inicial.

Uso:
    python create_admin.py <username> <email> <password>

Ejemplos:
    python create_admin.py admin admin@example.com admin123
    python create_admin.py juan juan@example.com miPassword123
"""

import sys
from app import create_app, db
from app.models import User


def create_admin_user(username, email, password):
    """Crear un nuevo usuario con rol admin."""
    app = create_app()
    
    with app.app_context():
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"❌ Error: El usuario '{username}' ya existe.")
            return False
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print(f"❌ Error: El email '{email}' ya está registrado.")
            return False
        
        # Crear nuevo usuario admin
        user = User(
            username=username,
            email=email,
            role='admin'  # Rol de administrador
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            print(f"✓ Usuario administrador creado exitosamente:")
            print(f"  • Username: {username}")
            print(f"  • Email: {email}")
            print(f"  • Rol: admin")
            print(f"\n  Ahora puedes acceder a: http://localhost:5000/auth/admin")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear el usuario: {str(e)}")
            return False


def main():
    """Función principal."""
    if len(sys.argv) < 4:
        print(__doc__)
        print("\nEjemplo de uso:")
        print("  python create_admin.py admin admin@example.com contraseña123")
        return
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    # Validaciones simples
    if len(username) < 3:
        print("❌ Error: El username debe tener al menos 3 caracteres.")
        return
    
    if len(password) < 6:
        print("❌ Error: La contraseña debe tener al menos 6 caracteres.")
        return
    
    if '@' not in email:
        print("❌ Error: El email no es válido.")
        return
    
    create_admin_user(username, email, password)


if __name__ == '__main__':
    main()
