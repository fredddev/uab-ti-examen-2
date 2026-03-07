#!/usr/bin/env python
"""
Script para actualizar las tablas de la base de datos
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno PRIMERO
load_dotenv()

from app import create_app, db
from app.models import User, Category, Task

# Crear contexto de la aplicación
app = create_app(os.environ.get('FLASK_ENV', 'development'))

with app.app_context():
    print("🔧 Actualizando estructura de la base de datos...")
    print("=" * 60)
    
    # Crear todas las tablas
    db.create_all()
    
    print("✅ Tablas creadas/actualizadas exitosamente")
    print("\nTablas en la base de datos:")
    print("  - user")
    print("  - category")
    print("  - task")
    print("=" * 60)
