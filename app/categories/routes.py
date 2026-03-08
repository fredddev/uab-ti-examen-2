from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import CategoryForm
from app.models.category import Category
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
        return redirect(url_for("dashboard"))  # temporal

    return render_template("categories/create.html", form=form)


# --- API JSON (POST, PUT, DELETE) ---
@categories_bp.route("/create", methods=["POST"])
@login_required
def create_category_api():
    data = request.get_json()
    if not data or not data.get("name"):
        return {"error": "El nombre de la categoría es requerido"}, 400
    try:
        category = Category(
            name=data.get("name"),
            description=data.get("description", ""),
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        return {"message": "Category created", "data": category.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500