from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/')
@login_required
def list_users():
    """Lista todos los usuarios."""
    return {'message': 'Users list'}, 200


@users_bp.route('/<int:user_id>')
@login_required
def get_user(user_id):
    """Obtiene un usuario específico."""
    return {'message': f'User {user_id}'}, 200


@users_bp.route('/<int:user_id>/profile')
@login_required
def user_profile(user_id):
    """Obtiene el perfil de un usuario."""
    user = User.query.get_or_404(user_id)
    return {'message': f'User {user_id} profile'}, 200
