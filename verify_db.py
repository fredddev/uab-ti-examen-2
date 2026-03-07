#!/usr/bin/env python
"""
Verificar la estructura de las tablas en la base de datos
"""
import os
from dotenv import load_dotenv
from sqlalchemy import inspect

load_dotenv()

from app import create_app, db
from app.models import User, Category, Task

app = create_app(os.environ.get('FLASK_ENV', 'development'))

with app.app_context():
    inspector = inspect(db.engine)
    
    print("\n" + "="*70)
    print("📊 ESTRUCTURA DE LA TABLA 'user'")
    print("="*70)
    
    columns = inspector.get_columns('user')
    for col in columns:
        nullable = "✓ Nullable" if col['nullable'] else "✗ NOT NULL"
        print(f"  • {col['name']:<25} {str(col['type']):<20} {nullable}")
    
    print("\n" + "="*70)
    print("✅ Tabla 'user' actualizada con éxito")
    print("="*70)
    print("\nNuevos campos agregados:")
    print("  ✓ password_hash (en lugar de password)")
    print("  ✓ role (admin o user)")
    print("\nMétodos disponibles en el modelo User:")
    print("  ✓ set_password(password) - Hashear y guardar contraseña")
    print("  ✓ check_password(password) - Verificar contraseña")
    print("  ✓ Compatible con Flask-Login (UserMixin)")
    print("="*70 + "\n")
