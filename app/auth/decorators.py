"""
Decorators personalizados para autenticación y autorización basada en roles.
"""

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def require_admin(f):
    """
    Decorator para restringir una vista solo a usuarios con rol 'admin'.
    
    Uso:
        @app.route('/admin')
        @require_admin
        def admin_dashboard():
            return render_template('admin_dashboard.html')
    
    Comportamiento:
        - Si el usuario no está autenticado: redirige a login
        - Si el usuario no es admin: redirige al dashboard principal con flash message
        - Si el usuario es admin: permite acceso a la vista
    
    Returns:
        function: Función decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el usuario está autenticado
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si el usuario tiene rol de admin
        if current_user.role != 'admin':
            flash('No tienes permisos para acceder a esta página. Se requiere rol de administrador.', 'danger')
            return redirect(url_for('tasks.list_tasks'))
        
        # Si el usuario es admin, permitir el acceso
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(required_role):
    """
    Decorator parametrizado para restringir una vista a un rol específico.
    
    Uso:
        @app.route('/moderador')
        @require_role('moderador')
        def moderator_panel():
            return render_template('moderator_panel.html')
    
    Args:
        required_role (str): Rol requerido para acceder a la vista
    
    Returns:
        function: Función decorada
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar si el usuario está autenticado
            if not current_user.is_authenticated:
                flash('Por favor inicia sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Verificar si el usuario tiene el rol requerido
            if current_user.role != required_role:
                flash(f'No tienes permisos para acceder a esta página. Se requiere rol de {required_role}.', 'danger')
                return redirect(url_for('tasks.list_tasks'))
            
            # Si el usuario tiene el rol correcto, permitir el acceso
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
