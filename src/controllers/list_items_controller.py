from flask import Blueprint, request, jsonify
from init import db
from datetime import date
from models.list_items import ListItem, list_item_schema, list_items_schema
from models.lists import List, list_schema, lists_schema
from models.items import Item, item_schema, items_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity
import functools

list_items_bp = Blueprint("list_items", __name__, url_prefix="/list_items")


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
                        message=f"User with email='{user.email}' not authorised to perform action"
                    ),
                    403,
                )
        else:
            return jsonify(message=f"List Item not found with id='{id}"), 404

    return wrapper


@list_items_bp.route("/")
@jwt_required()
def get_list_items():
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    if user.is_admin:
        list_items = (
            db.session.query(ListItem)
            .join(Item, ListItem.item_id == Item.item_id)
            .all()
        )
    else:
        list_items = (
            db.session.query(ListItem)
            .join(Item, ListItem.item_id == Item.item_id)
            .filter(Item.user_id == int(user))
        )
    return list_items_schema.dump(list_items)


@list_items_bp.route("/<int:id>")
@jwt_required()
@authorise_as_user_or_admin
def get_one_list_item(id):
    list_item = db.session.scalar(db.select(ListItem).filter_by(list_item_id=id))
    return list_item_schema.dump(list_item)


@list_items_bp.route("/", methods=["POST"])
@jwt_required()
def create_list_item():
    body_data = request.get_json()
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    list_allowed = db.session.scalar(
        db.select(List).filter_by(list_id=body_data.get("list_id"))
    )
    item_allowed = db.session.scalar(
        db.select(Item).filter_by(item_id=body_data.get("item_id"))
    )
    if list_allowed and item_allowed:
        if user.is_admin or (
            item_allowed.user_id == int(user) and list_allowed.user_id == int(user)
        ):
            body_data = request.get_json()
            list_item = ListItem(
                quantity=body_data.get("quantity"),
                date=date.today(),
                list_id=body_data.get("list_id"),
                item_id=body_data.get("item_id"),
            )
            db.session.add(list_item)
            db.session.commit()
            return list_item_schema.dump(list_item), 201
        # if not allowed to create
        else:
            return (
                jsonify(message=f"List or Item not found for user with email='{user.email}'"),
                404,
            )
    # lets user know unable to find list with id
    elif not list_allowed:
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


@list_items_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_user_or_admin
def update_one_list_item(id):
    body_data = request.get_json()
    list_item = db.session.scalar(db.select(ListItem).filter_by(list_item_id=id))
    if list_item:
        new_list_allowed = db.session.scalar(
            db.select(List).filter_by(list_id=body_data.get("list_id"))
        )
        new_item_allowed = db.session.scalar(
            db.select(Item).filter_by(item_id=body_data.get("item_id"))
        )
        user_id = get_jwt_identity()
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
        if user.is_admin or (new_item_allowed and new_list_allowed):
            list_item.quantity = (body_data.get("quantity") or list_item.quantity,)
            list_item.list_id = (body_data.get("list_id") or list_item.list_id,)
            list_item.item_id = (body_data.get("item_id") or list_item.item_id,)
            db.session.commit()
            return list_item_schema.dump(list_item)
        else:
            return (
                jsonify(message=f"List with id='{body_data.get('list_id')}' or Item with id='{body_data.get('item_id')}' not found for user with email='{user.email}'"),
                403,
            )

    else:
        return jsonify(message=f"Not found {id}"), 404


@list_items_bp.route("/<int:id>", methods=["DELETE"])
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