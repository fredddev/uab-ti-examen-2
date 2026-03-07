from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Category

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/')
@login_required
def list_categories():
    """Lista todas las categorías del usuario."""
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return {'message': 'Categories list', 'data': [c.to_dict() for c in categories]}, 200


@categories_bp.route('/<int:category_id>')
@login_required
def get_category(category_id):
    """Obtiene una categoría específica."""
    category = Category.query.get_or_404(category_id)
    
    # Verificar que la categoría pertenece al usuario
    if category.user_id != current_user.id:
        return {'error': 'No tienes permiso para ver esta categoría'}, 403
    
    return {'message': f'Category {category_id}', 'data': category.to_dict()}, 200


@categories_bp.route('/create', methods=['POST'])
@login_required
def create_category():
    """Crea una nueva categoría."""
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return {'error': 'El nombre de la categoría es requerido'}, 400
    
    try:
        category = Category(
            name=name,
            user_id=current_user.id,
            description=data.get('description', '')
        )
        db.session.add(category)
        db.session.commit()
        return {'message': 'Category created', 'data': category.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500


@categories_bp.route('/<int:category_id>/update', methods=['PUT'])
@login_required
def update_category(category_id):
    """Actualiza una categoría."""
    category = Category.query.get_or_404(category_id)
    
    # Verificar que la categoría pertenece al usuario
    if category.user_id != current_user.id:
        return {'error': 'No tienes permiso para editar esta categoría'}, 403
    
    data = request.get_json()
    try:
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        db.session.commit()
        return {'message': f'Category {category_id} updated', 'data': category.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500


@categories_bp.route('/<int:category_id>/delete', methods=['DELETE'])
@login_required
def delete_category(category_id):
    """Elimina una categoría."""
    category = Category.query.get_or_404(category_id)
    
    # Verificar que la categoría pertenece al usuario
    if category.user_id != current_user.id:
        return {'error': 'No tienes permiso para eliminar esta categoría'}, 403
    
    try:
        db.session.delete(category)
        db.session.commit()
        return {'message': f'Category {category_id} deleted'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
