from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from datetime import date
import functools
from models.categories import Category, category_schema, categories_schema
from models.users import User

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return jsonify(message="Not authorised to perform action"), 403    
    return wrapper

@categories_bp.route('/')
@jwt_required()
def get_categories():
    categories = db.session.scalars(db.select(Category).order_by(Category.category_id.asc()))
    return categories_schema.dump(categories)

@categories_bp.route('/<int:id>')
@jwt_required()
def get_category(id):
    category = db.session.scalar(db.select(Category).filter_by(category_id=id))
    if category:
        # logic in categories.py to filter category items for user_id or all for admin
        return category_schema.dump(category)
    else:
        return jsonify(message=f"Category not found with id='{id}'"), 404

@categories_bp.route('/', methods=["POST"])
@jwt_required()
@authorise_as_admin
def create_category():
    body_data = request.get_json()
    category = Category(
        name = body_data.get("name"),
        description = body_data.get("description"),
        date = date.today(),
    )
    db.session.add(category)
    db.session.commit()
    return category_schema.dump(category), 201

@categories_bp.route('/<int:id>', methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
def update_category(id):
    body_data = request.get_json()
    category = db.session.scalar(db.select(Category).filter_by(category_id=id))
    if category:
        category.name = body_data.get("name") or category.name,
        category.description = body_data.get("description") or category.description
        db.session.commit()
        return category_schema.dump(category), 201
    else:
        return jsonify(message=f"Category not found with id='{id}'"), 404
    
@categories_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_category(id):
    category = db.session.scalar(db.select(Category).filter_by(category_id=id))
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify(message=f"Category with id='{id}' deleted"), 200
    else:
        return jsonify(message=f"Category not found with id='{id}'"), 404