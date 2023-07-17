from flask import Blueprint, request, jsonify
from init import db
from models.lists import List, list_schema, lists_schema
from models.list_items import ListItem, list_item_schema, list_items_schema
from models.items import Item, item_schema, items_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
import functools

list_bp = Blueprint('list', __name__, url_prefix='/list')

@list_bp.route('/')
@jwt_required()
def get_all_lists():
    # if user admin display all lists, otherwise user specific
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    if user_admin:
        lists = db.session.scalars(db.select(List).order_by(List.date.desc()))
        return lists_schema.dump(lists)
    else:
        lists = db.session.scalars(db.select(List).filter_by(user_id=user))
        return lists_schema.dump(lists)

@list_bp.route('/<int:id>')
@jwt_required()
def get_list(id):
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    # if user admin display, or check if user owns the list
    if list and (user_admin or list.user_id == int(user)):
        return list_schema.dump(list)
    else:
        return jsonify(message=f"List with id='{id}' not found for user id='{user}'"), 404
    
@list_bp.route('/', methods=['POST'])
@jwt_required()
def create_list():
    body_data = request.get_json()
    list = List(
        name=body_data.get('name'),
        description=body_data.get('description'),
        date=date.today(),
        user_id=get_jwt_identity()
    )
    db.session.add(list)
    db.session.commit()
    return list_schema.dump(list), 201

@list_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(id):
    body_data = request.get_json()
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    if list:
        if not(user_admin or list.user_id == int(user)):
            return jsonify(error=f"Not authorised to edit list id='{id}'")
        list.name = body_data.get('name') or list.name
        list.description = body_data.get('description') or list.description
        db.session.commit()
        return list_schema.dump(list)
    else:
        return jsonify(message=f"List with id='{id}' not found for user id='{user}'"), 404

@list_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_list(id):
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    if list:
        if not(user_admin or list.user_id == int(user)):
            return jsonify(error=f"Not authorised to delete list id='{id}'")
        db.session.delete(list)
        db.session.commit()
        return jsonify(message=f"List with id='{id}' deleted'"), 200
    else:
        return jsonify(message=f"List not found with id='{id}'"), 404