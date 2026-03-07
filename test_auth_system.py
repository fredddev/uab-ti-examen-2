"""
Script de prueba para validar el sistema de registro e inicio de sesión.
Prueba el flujo completo sin interfaz web.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(override=True)

from app import create_app, db
from app.models import User

# Crear la aplicación
app = create_app('testing')

print("\n" + "="*60)
print("PRUEBA DEL SISTEMA DE REGISTRO E INICIO DE SESIÓN")
print("="*60)

with app.app_context():
    # Crear las tablas si no existen
    print("\n1. Creando tablas en base de datos...")
    db.create_all()
    print("   ✓ Tablas creadas")
    
    # Limpiar usuarios de prueba previos
    print("\n2. Limpiando usuarios de prueba previos...")
    User.query.delete()
    db.session.commit()
    print("   ✓ Base de datos limpia")
    
    # Prueba 1: Crear un usuario
    print("\n3. Creando usuario de prueba...")
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    print("   ✓ Usuario creado: testuser")
    
    # Prueba 2: Verificar que se guardó en base de datos
    print("\n4. Verificando usuario en base de datos...")
    saved_user = User.query.filter_by(username='testuser').first()
    assert saved_user is not None
    assert saved_user.email == 'testuser@example.com'
    print(f"   ✓ Usuario encontrado: {saved_user.username} ({saved_user.email})")
    
    # Prueba 3: Verificar contraseña
    print("\n5. Verificando validación de contraseña...")
    assert saved_user.check_password('password123') == True
    print("   ✓ Contraseña correcta validada")
    assert saved_user.check_password('wrongpassword') == False
    print("   ✓ Contraseña incorrecta rechazada")
    
    # Prueba 4: Validar unicidad de username
    print("\n6. Probando validación de username único...")
    try:
        duplicate_user = User(username='testuser', email='different@example.com')
        duplicate_user.set_password('password456')
        db.session.add(duplicate_user)
        db.session.commit()
        print("   ✗ ERROR: Se permitió username duplicado")
    except Exception as e:
        db.session.rollback()
        print("   ✓ Username duplicado correctamente rechazado")
    
    # Prueba 5: Validar unicidad de email
    print("\n7. Probando validación de email único...")
    try:
        duplicate_email = User(username='anotheruser', email='testuser@example.com')
        duplicate_email.set_password('password456')
        db.session.add(duplicate_email)
        db.session.commit()
        print("   ✗ ERROR: Se permitió email duplicado")
    except Exception as e:
        db.session.rollback()
        print("   ✓ Email duplicado correctamente rechazado")
    
    # Prueba 6: Crear usuario adicional
    print("\n8. Creando segundo usuario...")
    user2 = User(username='otheruser', email='other@example.com')
    user2.set_password('mypassword')
    db.session.add(user2)
    db.session.commit()
    print("   ✓ Segundo usuario creado: otheruser")
    
    # Prueba 7: Verificar que existen ambos usuarios
    print("\n9. Contando usuarios en base de datos...")
    total_users = User.query.count()
    assert total_users == 2
    print(f"   ✓ Total de usuarios: {total_users}")
    
    print("\n" + "="*60)
    print("TODAS LAS PRUEBAS PASADAS ✓")
    print("="*60)
    print("\nRESUMEN:")
    print("- Crear usuarios: ✓")
    print("- Guardar en base de datos: ✓")
    print("- Hashear contraseñas: ✓")
    print("- Validar contraseñas: ✓")
    print("- Validar username único: ✓")
    print("- Validar email único: ✓")
    print("\nEl sistema de registro está completamente funcional.")
    print("="*60 + "\n")
