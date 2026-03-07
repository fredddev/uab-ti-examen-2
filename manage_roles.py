"""
Script para gestionar roles de usuarios de forma fácil desde la línea de comandos.

Uso:
    python manage_roles.py list                          # Listar todos los usuarios
    python manage_roles.py set <username> admin           # Convertir user a admin
    python manage_roles.py set <username> user            # Convertir admin a user
    python manage_roles.py make-admin <username>          # Atajo para convertir a admin
    python manage_roles.py make-user <username>           # Atajo para convertir a user

Ejemplo:
    python manage_roles.py set juan admin                # Juan será administrador
    python manage_roles.py make-admin maria              # María será administradora
"""

import sys
from app import create_app, db
from app.models import User


def list_users():
    """Listar todos los usuarios con sus roles."""
    users = User.query.all()
    
    if not users:
        print("No hay usuarios registrados.")
        return
    
    print("\n" + "="*70)
    print(f"{'ID':<5} {'Usuario':<20} {'Email':<30} {'Rol':<10}")
    print("="*70)
    
    for user in users:
        print(f"{user.id:<5} {user.username:<20} {user.email:<30} {user.role:<10}")
    
    print("="*70 + "\n")


def change_role(username, new_role):
    """Cambiar el rol de un usuario."""
    # Validar el rol
    if new_role not in ['admin', 'user']:
        print(f"❌ Error: Rol inválido. Debe ser 'admin' o 'user', no '{new_role}'")
        return False
    
    # Buscar el usuario
    user = User.query.filter_by(username=username).first()
    
    if not user:
        print(f"❌ Error: Usuario '{username}' no encontrado.")
        return False
    
    # Cambiar el rol
    old_role = user.role
    user.role = new_role
    db.session.commit()
    
    print(f"✓ Rol de {user.username} actualizado: {old_role} → {new_role}")
    return True


def main():
    """Función principal."""
    app = create_app()
    
    with app.app_context():
        if len(sys.argv) < 2:
            print(__doc__)
            return
        
        command = sys.argv[1].lower()
        
        # Comando: list
        if command == 'list':
            list_users()
        
        # Comando: set <username> <role>
        elif command == 'set':
            if len(sys.argv) < 4:
                print("Uso: python manage_roles.py set <username> <admin|user>")
                return
            
            username = sys.argv[2]
            new_role = sys.argv[3].lower()
            change_role(username, new_role)
        
        # Comando: make-admin <username>
        elif command == 'make-admin':
            if len(sys.argv) < 3:
                print("Uso: python manage_roles.py make-admin <username>")
                return
            
            username = sys.argv[2]
            change_role(username, 'admin')
        
        # Comando: make-user <username>
        elif command == 'make-user':
            if len(sys.argv) < 3:
                print("Uso: python manage_roles.py make-user <username>")
                return
            
            username = sys.argv[2]
            change_role(username, 'user')
        
        else:
            print(f"❌ Comando desconocido: {command}")
            print(__doc__)


if __name__ == '__main__':
    main()
