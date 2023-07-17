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
def get_one_list_item():
    pass

@list_items_bp.route('/', methods=['POST'])
@jwt_required()
def create_list_item():
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
    # need to make sure only user and admin can do this