from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from datetime import date
from models.items import Item, item_schema, items_schema
from models.users import User

items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/')
@jwt_required()
def get_item():
    # if user admin display all lists, otherwise user specific
    user = get_jwt_identity()
    # determine if selected user is an admin, true or false
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    if user_admin:
        # select all items
        items = db.session.scalars(db.select(Item).order_by(Item.date.desc()))
        return items_schema.dump(items)
    else:
        # select items by user_id
        items = db.session.scalars(db.select(Item).filter_by(user_id=user))
        return items_schema.dump(items)

@items_bp.route('/<int:id>')
@jwt_required()
def get_list(id):
    user_id = get_jwt_identity()
    # get user by id
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    # get item by id
    item = db.session.scalar(db.select(Item).filter_by(item_id=id))
    # if user admin display, or check if user owns the list
    if item:
        # if the item belongs to the user or is an admin then proceed, otherwise throw 403
        if item.user_id != int(user_id) and not user.is_admin:
            return jsonify(message=f"Item with id='{id}' not found for user with email='{user.email}'"), 403
        return item_schema.dump(item)
    else:
        return jsonify(message=f"Item with id='{id}' not found"), 404
    
@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    body_data = request.get_json()
    # Create item by class
    item = Item(
        name=body_data.get('name'),
        description=body_data.get('description'),
        date=date.today(),
        user_id=get_jwt_identity(),
        category_id=body_data.get('category_id'),
        weight=body_data.get('weight')
    )
    db.session.add(item)
    db.session.commit()
    return item_schema.dump(item), 201

@items_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_item(id):
    body_data = request.get_json()
    user_id = get_jwt_identity()
    # get user by id
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    # get item by id
    item = db.session.scalar(db.select(Item).filter_by(item_id=id))
    if item:
        # if the item belongs to the user or an admin proceed, otherwise 403
        if item.user_id != int(user_id) and not user.is_admin:
            return jsonify(message=f"Item with id='{id}' not found for user with email='{user.email}'"), 403
        item.name = body_data.get('name') or item.name
        item.description = body_data.get('description') or item.description
        item.category_id = body_data.get('category_id') or item.category_id
        item.weight = body_data.get('weight') or item.weight
        db.session.commit()
        return item_schema.dump(item)
    else:
        return jsonify(message=f"Item with id='{id}' not found"), 404

@items_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    user_id = get_jwt_identity()
    # get user by id
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    # get item by id
    item = db.session.scalar(db.select(Item).filter_by(item_id=id))
    if item:
        # if the item belongs to the user or an admin proceed, otherwise 403
        if item.user_id != int(user_id) and not user.is_admin:
            return jsonify(error=f"Not authorised to delete item id='{id}'"), 403
        db.session.delete(item)
        db.session.commit()
        return jsonify(message=f"Item with id='{id}' deleted'"), 200
    else:
        return jsonify(message=f"Item not found with id='{id}'"), 404
