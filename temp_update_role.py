"""Script temporal para cambiar el rol a admin."""
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    
    if user:
        print(f"Usuario encontrado: {user.username}")
        print(f"Rol actual: {user.role}")
        user.role = 'admin'
        db.session.commit()
        print(f"✓ Rol actualizado a: {user.role}")
    else:
        print("❌ Usuario 'admin' no encontrado")
