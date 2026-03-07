from flask import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/')
def list_users():
    """Lista todos los usuarios."""
    return {'message': 'Users list'}, 200


@users_bp.route('/<int:user_id>')
def get_user(user_id):
    """Obtiene un usuario específico."""
    return {'message': f'User {user_id}'}, 200


@users_bp.route('/<int:user_id>/profile')
def user_profile(user_id):
    """Obtiene el perfil de un usuario."""
    return {'message': f'User {user_id} profile'}, 200
