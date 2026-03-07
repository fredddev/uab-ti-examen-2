#!/usr/bin/env python
"""
Script de prueba para validar la configuración de MySQL y Flask
"""

from app import create_app, db
import os

try:
    # Crear la aplicación
    app = create_app()
    
    print("\n" + "="*60)
    print("✅ APLICACIÓN FLASK CREADA EXITOSAMENTE")
    print("="*60)
    
    print("\n📋 CONFIGURACIÓN:")
    print(f"   Entorno: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"   Debug: {app.debug}")
    print(f"   Host: {os.environ.get('FLASK_HOST', '127.0.0.1')}")
    print(f"   Puerto: {os.environ.get('FLASK_PORT', '5001')}")
    
    print("\n🗄️  BASE DE DATOS:")
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    # Ocultar contraseña por seguridad
    db_uri_masked = db_uri.replace(
        f"{os.environ.get('DB_PASSWORD', 'password')}",
        "***"
    )
    print(f"   URI: {db_uri_masked}")
    
    print("\n✨ CONFIGURACIÓN LISTA PARA:")
    print("   - Crear migraciones: flask db init")
    print("   - Generar migración: flask db migrate -m 'descripción'")
    print("   - Aplicar migración: flask db upgrade")
    print("   - Ejecutar app: python run.py")
    
    print("\n" + "="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
