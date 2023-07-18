from flask import Blueprint, request, jsonify
from init import db
from datetime import date
from models.list_items import ListItem, list_item_schema, list_items_schema
from models.lists import List, list_schema, lists_schema
from models.items import Item, item_schema, items_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity

list_items_bp = Blueprint('list_items', __name__, url_prefix='/list_items')

@list_items_bp.route('/')
@jwt_required()
def get_list_items():
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    if user_admin:
        listitems = db.session.query(ListItem).join(Item, ListItem.item_id==Item.item_id).all()
    else:
        listitems = db.session.query(ListItem).join(Item, ListItem.item_id==Item.item_id).filter(Item.user_id==int(user))
    return list_items_schema.dump(listitems)
 
@list_items_bp.route('/<int:id>')
@jwt_required()
def get_one_list_item(id):
    user = get_jwt_identity()
    list_item_exists = db.session.scalar(db.select(ListItem).filter_by(list_item_id=id))
    if list_item_exists:
        user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
        list_allowed = db.session.scalar(db.select(List).filter_by(list_id=list_item_exists.list_id))
        item_allowed = db.session.scalar(db.select(Item).filter_by(item_id=list_item_exists.item_id))
        if list_allowed and item_allowed:
            if user_admin or (item_allowed.user_id==int(user) and list_allowed.user_id==int(user)):
                return list_item_schema.dump(list_item_exists), 201
            # if not allowed to create
            else:
                return jsonify(message=f"List or Item not found for user with id='{user}'"), 404
        # lets user know unable to find list with id
        elif not list_allowed:
            return jsonify(message=f"List not found with id='{list_item_exists.list_id}"), 404
        # lets user know unable to find item with id
        else:
            return jsonify(message=f"Item not found with id='{list_item_exists.item_id}"), 404
    else:
        return jsonify(message=f"List_item not found with id='{id}")

@list_items_bp.route('/', methods=['POST'])
@jwt_required()
def create_list_item():
    body_data = request.get_json()
    user = get_jwt_identity()
    user_admin = db.session.scalar(db.select(User).filter_by(user_id=user)).is_admin
    list_allowed = db.session.scalar(db.select(List).filter_by(list_id=body_data.get('list_id')))
    item_allowed = db.session.scalar(db.select(Item).filter_by(item_id=body_data.get('item_id')))
    if list_allowed and item_allowed:
        if user_admin or (item_allowed.user_id==int(user) and list_allowed.user_id==int(user)):
            body_data = request.get_json()
            listitem = ListItem(
                quantity=body_data.get('quantity'),
                date=date.today(),
                list_id=body_data.get('list_id'),
                item_id=body_data.get('item_id'),
            )
            db.session.add(listitem)
            db.session.commit()
            return list_item_schema.dump(listitem), 201
        # if not allowed to create
        else:
            return jsonify(message=f"List or Item not found for user with id='{user}'"), 404
    # lets user know unable to find list with id
    elif not list_allowed:
        return jsonify(message=f"List not found with id='{body_data.get('list_id')}"), 404
    # lets user know unable to find item with id
    else:
        return jsonify(message=f"Item not found with id='{body_data.get('item_id')}"), 404