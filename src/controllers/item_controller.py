from flask import Blueprint, request, jsonify
from init import db
from models.items import Item, item_schema, items_schema
from models.list_items import ListItem, list_item_schema, list_items_schema
from models.lists import List, list_schema, lists_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/')
@jwt_required()
def get_item():
    # if user admin display all lists, otherwise user specific
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    if user_admin:
        items = db.session.scalars(db.select(Item).order_by(Item.date.desc()))
        return items_schema.dump(items)
    else:
        items = db.session.scalars(db.select(Item).filter_by(user_id=user))
        return items_schema.dump(items)
    
@items_bp.route('/<int:id>')
@jwt_required()
def get_list(id):
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    item = db.session.scalar(db.select(Item).filter_by(item_id=id))
    # if user admin display, or check if user owns the list
    if item and (user_admin or item.user_id == int(user)):
        return item_schema.dump(item)
    else:
        return jsonify(message=f"Item with id='{id}' not found for user id='{user}'"), 404
    
@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    body_data = request.get_json()

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
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    item = db.session.scalar(db.select(Item).filter_by(item_id=id))
    if item:
        if not(user_admin or item.user_id == int(user)):
            return jsonify(error=f"Not authorised to edit item id='{id}'")
        item.name = body_data.get('name') or item.name
        item.description = body_data.get('description') or item.description
        item.category_id = body_data.get('category_id') or item.category_id
        item.weight = body_data.get('weight') or item.weight
        db.session.commit()
        return item_schema.dump(item)
    else:
        return jsonify(message=f"List with id='{id}' not found for user id='{user}'"), 404

@items_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    item = db.session.scalar(db.select(Item).filter_by(item_id=id))
    if item:
        if not(user_admin or item.user_id == int(user)):
            return jsonify(error=f"Not authorised to delete item id='{id}'")
        db.session.delete(item)
        db.session.commit()
        return jsonify(message=f"Item with id='{id}' deleted'"), 200
    else:
        return jsonify(message=f"Item not found with id='{id}'"), 404
