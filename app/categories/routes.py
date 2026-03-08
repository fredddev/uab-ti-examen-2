from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import CategoryForm
from app.models.category import Category
from app.categories.forms import EmptyForm
from app import db

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


# --- FORMULARIO HTML ---
@categories_bp.route("/create-form", methods=["GET", "POST"])
@login_required
def create_category_form_html():
    if current_user.role != "admin":
        flash("No tienes permisos para crear categorías.", "danger")
        return redirect(url_for("dashboard"))

    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash("Categoría creada exitosamente.", "success")
        return redirect(url_for("categories.list_categories_html"))  # temporal

    return render_template("categories/create.html", form=form)

# --- LISTADO HTML ---
@categories_bp.route("/", methods=["GET"])
@login_required
def list_categories_html():
    """Lista todas las categorías del usuario actual, con búsqueda opcional."""
    query = request.args.get("q", "").strip()
    form = EmptyForm()

    if query:
        # Filtrar categorías del usuario según la búsqueda en el nombre
        categories = Category.query.filter(
            Category.user_id == current_user.id,
            Category.name.ilike(f"%{query}%")
        ).all()
    else:
        # Mostrar todas las categorías si no hay búsqueda
        categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template("categories/list.html", categories=categories, form=form, query=query)


# --- FORMULARIO EDITAR ---
@categories_bp.route("/edit/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    """Editar una categoría existente (solo admin)."""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        flash("No tienes permisos para editar categorías.", "danger")
        return redirect(url_for("categories.list_categories_html"))

    # Buscar la categoría
    category = Category.query.get_or_404(category_id)

    form = CategoryForm(obj=category)  # Cargar datos actuales

    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        try:
            db.session.commit()
            flash("Categoría actualizada exitosamente.", "success")
            return redirect(url_for("categories.list_categories_html"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar la categoría: {str(e)}", "danger")

    return render_template("categories/edit.html", form=form, category=category)

# --- ELIMINAR ---
@categories_bp.route('/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category_html(category_id):
    """Elimina una categoría. Solo admins."""
    if current_user.role != "admin":
        flash("No tienes permisos para eliminar categorías.", "danger")
        return redirect(url_for('categories.list_categories_html'))

    category = Category.query.get_or_404(category_id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f"Categoría '{category.name}' eliminada exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error al eliminar la categoría: {str(e)}", "danger")

    return redirect(url_for('categories.list_categories_html'))