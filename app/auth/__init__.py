from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login')
def login():
    """Ruta de login."""
    return {'message': 'Login page'}, 200


@auth_bp.route('/register')
def register():
    """Ruta de registro."""
    return {'message': 'Register page'}, 200


@auth_bp.route('/logout')
def logout():
    """Ruta de logout."""
    return {'message': 'Logout'}, 200
