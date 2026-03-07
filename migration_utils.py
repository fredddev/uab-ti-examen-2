"""
Utilidades para gestionar migraciones de Flask-Migrate desde Python

Usar este archivo para ejecutar comandos de migración dentro de la aplicación Flask
o para automatizar tareas relacionadas con la base de datos.
"""

import os
from flask.cli import FlaskGroup
from app import create_app, db


def create_app_for_cli(info=None):
    """Función para crear app en contexto CLI."""
    return create_app(os.environ.get('FLASK_ENV', 'development'))


@click.group(cls=FlaskGroup, create_app=create_app_for_cli)
def cli():
    """Herramientas de migración de base de datos."""
    pass


# Importar otros comandos CLI si los necesitas
if __name__ == '__main__':
    cli()


"""
ALTERNATIVA: Comandos Básicos desde Terminal
=============================================

# Ver estado actual
flask db current

# Ver todas las migraciones
flask db history

# Crear nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir última migración
flask db downgrade

# Revertir a versión específica
flask db downgrade <revision_id>

# Ver información de revisión
flask db show <revision_id>


MANEJO DE CONFLICTOS EN EQUIPO
==============================

Cuando hay migraciones en conflicto (deux personas crean migraciones simultáneamente):

1. Identificar las ramas divergentes:
   flask db branches

2. Ver el árbol de versiones:
   flask db history

3. Fusionar manualmente (si es necesario):
   flask db merge <revision1> <revision2> -m "Merge migraciones"

4. Resolver conflictos en el archivo generado
5. Aplicar:
   flask db upgrade


CÓMO TRABAJAR EN EQUIPO
======================

1. Compañero A modifica modelos y ejecuta:
   flask db migrate -m "Feature A changes"
   git add migrations/
   git commit -m "Migration for feature A"
   git push

2. Compañero B recibe cambios:
   git pull
   flask db upgrade  # Aplica migraciones de A

3. Compañero B modifica modelos y ejecuta:
   flask db migrate -m "Feature B changes"
   git add migrations/
   git commit -m "Migration for feature B"
   git push

4. Si hay conflictos, resolver con flask db merge


TESTING CON MIGRACIONES
=======================

Para tests, puedes:

1. Usar base de datos en memoria:
   SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

2. O usar una BD de prueba:
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/test_db'

3. Ejecutar migraciones en tests:
   flask db upgrade

4. Limpiar después:
   flask db downgrade  # O eliminar la BD de prueba


BACKUP RECOMENDADO ANTES DE UPGRADE EN PRODUCCIÓN
=================================================

# 1. Backup de BD
mysqldump -u root -p flask_app > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Ver cambios de migración
flask db show head

# 3. Ejecutar upgrade
flask db upgrade

# 4. Verificar que todo funciona
flask run

# 5. Si falla, restaurar
mysql -u root -p flask_app < backup_*.sql
flask db downgrade
"""
