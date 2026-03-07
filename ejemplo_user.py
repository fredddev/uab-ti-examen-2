"""
EJEMPLO REAL: Usando el modelo User con Flask-SQLAlchemy
===========================================================

Este archivo muestra cómo trabajar con el modelo User en tu aplicación Flask.
"""

from app import create_app, db
from app.models import User
import os

# Crear la aplicación
app = create_app(os.environ.get('FLASK_ENV', 'development'))


def ejemplo_1_crear_usuario():
    """1. CREAR UN NUEVO USUARIO"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Crear un nuevo usuario")
    print("="*60)
    
    with app.app_context():
        # Crear instancia del usuario
        new_user = User(
            username='maria_garcia',
            email='maria@example.com',
            role='user'  # o 'admin'
        )
        
        # Hasher y asignar contraseña
        new_user.set_password('contraseña_segura123')
        
        # Guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ Usuario creado: {new_user.username}")
        print(f"   Email: {new_user.email}")
        print(f"   Rol: {new_user.role}")
        print(f"   ID: {new_user.id}")


def ejemplo_2_verificar_contraseña():
    """2. VERIFICAR CONTRASEÑA (para login)"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Verificar contraseña en login")
    print("="*60)
    
    with app.app_context():
        # Buscar usuario por email o username
        user_login = User.query.filter_by(username='maria_garcia').first()
        
        if user_login:
            # Verificar contraseña
            if user_login.check_password('contraseña_segura123'):
                print(f"✅ Login exitoso para {user_login.username}")
                print(f"   Contraseña correcta ✓")
            else:
                print(f"❌ Contraseña incorrecta")
        else:
            print("❌ Usuario no encontrado")


def ejemplo_3_consultas():
    """3. CONSULTAS CON EL MODELO USER"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Diferentes consultas de usuarios")
    print("="*60)
    
    with app.app_context():
        # Obtener todos los usuarios
        all_users = User.query.all()
        print(f"Total de usuarios: {len(all_users)}")
        for user in all_users:
            print(f"  - {user.username} ({user.email}) - Rol: {user.role}")
        
        # Filtrar por rol
        admins = User.query.filter_by(role='admin').all()
        print(f"\nAdministradores: {len(admins)}")
        
        # Buscar por email
        user_by_email = User.query.filter_by(email='maria@example.com').first()
        if user_by_email:
            print(f"\nUsuario encontrado por email: {user_by_email.username}")


def ejemplo_4_actualizar_usuario():
    """4. ACTUALIZAR INFORMACIÓN DEL USUARIO"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Actualizar datos del usuario")
    print("="*60)
    
    with app.app_context():
        user = User.query.filter_by(username='maria_garcia').first()
        
        if user:
            # Actualizar email
            user.email = 'maria.nueva@example.com'
            
            # Actualizar rol
            user.role = 'admin'
            
            # Cambiar contraseña
            user.set_password('nueva_contraseña_segura456')
            
            db.session.commit()
            print(f"✅ Usuario actualizado:")
            print(f"   Nuevo email: {user.email}")
            print(f"   Nuevo rol: {user.role}")
            print(f"   Contraseña actualizada ✓")


def ejemplo_5_eliminar_usuario():
    """5. ELIMINAR UN USUARIO"""
    print("\n" + "="*60)
    print("EJEMPLO 5: Eliminar un usuario")
    print("="*60)
    
    with app.app_context():
        user = User.query.filter_by(username='maria_garcia').first()
        
        if user:
            username = user.username
            db.session.delete(user)
            db.session.commit()
            print(f"✅ Usuario '{username}' eliminado de la base de datos")


def ejemplo_6_usar_en_rutas():
    """6. USAR EL MODELO EN RUTAS FLASK"""
    print("\n" + "="*60)
    print("EJEMPLO 6: Uso en rutas Flask")
    print("="*60)
    
    print("""
    # En tu archivo de autenticación (auth/routes.py):
    
    from flask import Blueprint, request, jsonify
    from app import db
    from app.models import User
    
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        '''Registrar nuevo usuario'''
        data = request.get_json()
        
        # Validar que no exista el usuario
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Usuario ya existe'}), 409
        
        # Crear usuario
        user = User(
            username=data['username'],
            email=data['email'],
            role='user'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuario creado exitosamente'}), 201
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        '''Iniciar sesión'''
        data = request.get_json()
        
        # Buscar usuario
        user = User.query.filter_by(username=data['username']).first()
        
        # Verificar contraseña
        if user and user.check_password(data['password']):
            # Login exitoso - usar Flask-Login
            login_user(user)
            return jsonify({'message': 'Login exitoso', 'user_id': user.id}), 200
        
        return jsonify({'error': 'Credenciales inválidas'}), 401
    """)


if __name__ == '__main__':
    print("\n🚀 EJEMPLOS DE USO DEL MODELO USER\n")
    
    # Descomentar los ejemplos que quieras ejecutar:
    
    # ejemplo_1_crear_usuario()
    # ejemplo_2_verificar_contraseña()
    # ejemplo_3_consultas()
    # ejemplo_4_actualizar_usuario()
    # ejemplo_5_eliminar_usuario()
    ejemplo_6_usar_en_rutas()
