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


def authorise_as_user_or_admin(fn):
    @functools.wraps(fn)
    def wrapper(id, item_id, *args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
        list_item = db.session.scalar(
            db.select(ListItem).filter_by(list_id=id, item_id=item_id)
        )
        if list_item:
            list_allowed = db.session.scalar(
                db.select(List).filter_by(list_id=list_item.list_id)
            )
            item_allowed = db.session.scalar(
                db.select(Item).filter_by(item_id=list_item.item_id)
            )
            if user.is_admin or (
                item_allowed.user_id == int(user_id)
                and list_allowed.user_id == int(user_id)
            ):
                return fn(id, item_id, *args, **kwargs)
            else:
                return (
                    jsonify(
                        message=f"User with email='{user.email}' not authorised to perform action on item with id='{item_id}' in list with id='{id}'"
                    ),
                    403,
                )
        else:
            return (
                jsonify(
                    message=f"Item with id='{item_id}' not found in list with id='{id}'"
                ),
                404,
            )

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
            jsonify(message=f"List id='{id}' not found"),
            404,
        )


@list_items_bp.route("/", methods=["POST"])
@jwt_required()
def create_list_item(id):
    body_data = request.get_json()
    item_id = body_data.get("item_id")
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    list_item = db.session.scalar(
        db.select(ListItem).filter_by(list_id=id, item_id=item_id)
    )
    if list_item:
        list_item.quantity = body_data.get("quantity") or list_item.quantity
        db.session.commit()
        return (
            jsonify(
                message=f"This item id='{item_id}' is already in list='{id}'",
                item_quantity=list_item.quantity,
            ),
            404,
        )
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
            jsonify(message=f"List not found with id='{id}"),
            404,
        )
    # lets user know unable to find item with id
    else:
        return (
            jsonify(message=f"Item not found with id='{body_data.get('item_id')}"),
            404,
        )


@list_items_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_user_or_admin
def delete_list_item(id, item_id):
    list_item = db.session.scalar(
        db.select(ListItem).filter_by(list_id=id, item_id=item_id)
    )
    if list_item:
        db.session.delete(list_item)
        db.session.commit()
        return (
            jsonify(
                message=f"Item with id='{item_id}' deleted from list with id='{id}'"
            ),
            200,
        )
    else:
        return (
            jsonify(
                message=f"Item with id='{item_id}' not found in list with id='{id}'"
            ),
            404,
        )
