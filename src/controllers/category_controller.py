from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import functools
from init import db
from models.categories import Category, category_schema, categories_schema
from models.users import User

category_bp = Blueprint("category", __name__, url_prefix="/category")

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return jsonify(error="Not authorised to perform action"), 403    
    return wrapper

@category_bp.route('/')
@jwt_required()
@authorise_as_admin
def get_categories():
    categories = db.session.scalars(db.select(Category).order_by(Category.category_id.asc()))
    return categories_schema.dump(categories)

@category_bp.route('/<int:id>')
@jwt_required()
@authorise_as_admin
def get_category(id):
    category = db.session.scalar(db.select(Category).filter_by(category_id=id))
    return category_schema.dump(category)