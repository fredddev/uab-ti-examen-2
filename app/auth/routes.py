"""
Rutas de autenticación (login, registro, logout).
"""

from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.decorators import require_admin


# Crear el blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Ruta para el registro de nuevos usuarios.
    
    GET: Muestra el formulario de registro
    POST: Procesa el formulario y crea el usuario
    """
    # Si el usuario ya está logueado, redirige al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('tasks.list_tasks'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Crear nuevo usuario
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            # Hashear y asignar contraseña
            user.set_password(form.password.data)
            
            # Guardar en base de datos
            db.session.add(user)
            db.session.commit()
            
            flash(f'¡Bienvenido, {form.username.data}! Tu cuenta ha sido creada exitosamente.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. Por favor intenta de nuevo.', 'danger')
            print(f'Error en registro: {str(e)}')
    
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para el login de usuarios.
    
    GET: Muestra el formulario de login
    POST: Procesa el formulario y autentica al usuario
    """
    # Si el usuario ya está logueado, redirige al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('tasks.list_tasks'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=False)
            
            # Redirige a la página siguiente si existe, sino al dashboard de tareas
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('tasks.list_tasks'))
        
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Ruta para logout del usuario."""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/admin')
@require_admin
def admin_panel():
    """
    Panel de administración - solo accesible para usuarios con rol 'admin'.
    
    Esta ruta demuestra cómo usar el decorator @require_admin para proteger vistas.
    """
    # Obtener estadísticas de usuarios
    total_users = User.query.count()
    admin_users = User.query.filter_by(role='admin').count()
    regular_users = User.query.filter_by(role='user').count()
    
    users_list = User.query.all()
    
    return render_template(
        'admin_panel.html',
        total_users=total_users,
        admin_users=admin_users,
        regular_users=regular_users,
        users_list=users_list
    )
