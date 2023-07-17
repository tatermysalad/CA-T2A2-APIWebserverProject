from flask import Blueprint, request, jsonify
from init import db
from datetime import date
from models.list_items import ListItem, list_item_schema, list_items_schema
from models.lists import List, list_schema, lists_schema
from models.items import Item, item_schema, items_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

list_items_bp = Blueprint('list_items', __name__, url_prefix='/list_items')

@list_items_bp.route('/')
@jwt_required()
def get_list_items():
    listitems = db.session.scalars(db.select(ListItem).order_by(ListItem.date.desc()))
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