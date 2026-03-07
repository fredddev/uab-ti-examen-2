from flask import Blueprint

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/')
def list_categories():
    """Lista todas las categorías del usuario."""
    return {'message': 'Categories list'}, 200


@categories_bp.route('/<int:category_id>')
def get_category(category_id):
    """Obtiene una categoría específica."""
    return {'message': f'Category {category_id}'}, 200


@categories_bp.route('/create', methods=['POST'])
def create_category():
    """Crea una nueva categoría."""
    return {'message': 'Category created'}, 201


@categories_bp.route('/<int:category_id>/update', methods=['PUT'])
def update_category(category_id):
    """Actualiza una categoría."""
    return {'message': f'Category {category_id} updated'}, 200


@categories_bp.route('/<int:category_id>/delete', methods=['DELETE'])
def delete_category(category_id):
    """Elimina una categoría."""
    return {'message': f'Category {category_id} deleted'}, 200
