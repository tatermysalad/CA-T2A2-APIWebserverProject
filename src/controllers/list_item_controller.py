from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from datetime import date
import functools
from models.list_items import ListItem, list_item_schema, list_items_schema
from models.lists import List
from models.items import Item
from models.users import User


list_items_bp = Blueprint("list_items", __name__, url_prefix="/<int:id>/items")
# a user can have the same item in a list so another bp is needed to make sure multiples aren't removed
list_items_delete_bp = Blueprint(
    "list_items_delete", __name__, url_prefix="/list_items/<int:id>/"
)


def authorise_as_user_or_admin(fn):
    @functools.wraps(fn)
    def wrapper(id, *args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))

        list_item_exists = db.session.scalar(
            db.select(ListItem).filter_by(list_item_id=id)
        )
        if list_item_exists:
            list_allowed = db.session.scalar(
                db.select(List).filter_by(list_id=list_item_exists.list_id)
            )
            item_allowed = db.session.scalar(
                db.select(Item).filter_by(item_id=list_item_exists.item_id)
            )
            if user.is_admin or (
                item_allowed.user_id == int(user_id)
                and list_allowed.user_id == int(user_id)
            ):
                return fn(id, *args, **kwargs)
            else:
                return (
                    jsonify(
                        message=f"User with email='{user.email}' not authorised to perform action on list_item with id='{list_item_exists.list_item_id}'"
                    ),
                    403,
                )
        else:
            return jsonify(message=f"List_Item not found with id='{id}"), 404

    return wrapper


@list_items_bp.route("/")
@jwt_required()
def get_list_items(id):
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    if list:
        if list.user_id == int(user_id) or user.is_admin:
            list_items = db.session.scalars(db.select(ListItem).filter_by(list_id=id))
            return list_items_schema.dump(list_items)
        else:   
            return (
            jsonify(
                message=f"List id='{id}' not found for user with email='{user.email}'"
            ),
            403,
        )
    else:
        return (
            jsonify(
                message=f"List id='{id}' not found"), 404,
        )


@list_items_bp.route("/", methods=["POST"])
@jwt_required()
def create_list_item(id):
    body_data = request.get_json()
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    item = db.session.scalar(
        db.select(Item).filter_by(item_id=body_data.get("item_id"))
    )
    if list and item:
        if user.is_admin or (
            item.user_id == int(user_id) and list.user_id == int(user_id)
        ):
            body_data = request.get_json()
            list_item = ListItem(
                quantity=body_data.get("quantity"),
                date=date.today(),
                list_id=list.list_id,
                item_id=item.item_id,
            )
            db.session.add(list_item)
            db.session.commit()
            return list_item_schema.dump(list_item), 201
        # if not allowed to create
        else:
            return (
                jsonify(
                    message=f"List or Item not found for user with email='{user.email}'"
                ),
                404,
            )
    # lets user know unable to find list with id
    elif not list:
        return (
            jsonify(message=f"List not found with id='{body_data.get('list_id')}"),
            404,
        )
    # lets user know unable to find item with id
    else:
        return (
            jsonify(message=f"Item not found with id='{body_data.get('item_id')}"),
            404,
        )


@list_items_delete_bp.route("", methods=["DELETE"])
@jwt_required()
@authorise_as_user_or_admin
def delete_list_item(id):
    list_item = db.session.scalar(db.select(ListItem).filter_by(list_item_id=id))
    if list_item:
        db.session.delete(list_item)
        db.session.commit()
        return jsonify(message=f"List Item with id='{id}' deleted"), 200
    else:
        return jsonify(message=f"List Item not found with id='{id}'"), 404
