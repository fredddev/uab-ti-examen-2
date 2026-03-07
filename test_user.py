#!/usr/bin/env python
"""
Test: Crear un usuario de prueba
"""
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models import User

app = create_app(os.environ.get('FLASK_ENV', 'development'))

with app.app_context():
    # Eliminar usuario si existe
    User.query.filter_by(username='test_user').delete()
    db.session.commit()
    
    # Crear usuario de prueba
    user = User(
        username='test_user',
        email='test@example.com',
        role='user'
    )
    user.set_password('test123')
    
    db.session.add(user)
    db.session.commit()
    
    print("\n✅ Usuario creado exitosamente:")
    print(f"   ID: {user.id}")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Role: {user.role}")
    print(f"   Password hasheada: {user.password_hash[:20]}...")
    
    # Verificar contraseña
    if user.check_password('test123'):
        print("   ✓ Contraseña verificada exitosamente")
    else:
        print("   ✗ Error en verificación de contraseña")
    
    print()
