from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from datetime import date
from models.lists import List, list_schema, lists_schema
from models.items import Item
from models.users import User
from controllers.list_item_controller import list_items_bp

lists_bp = Blueprint("lists", __name__, url_prefix="/lists")
lists_bp.register_blueprint(list_items_bp)  # path is in list_items_controller.py


@lists_bp.route("/")
@jwt_required()
def get_all_lists():
    # if user admin display all lists, otherwise user specific
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    if user.is_admin:
        lists = db.session.scalars(db.select(List).order_by(List.date.desc()))
        return lists_schema.dump(lists)
    else:
        lists = db.session.scalars(db.select(List).filter_by(user_id=user_id))
        return lists_schema.dump(lists)


@lists_bp.route("/<int:id>")
@jwt_required()
def get_list(id):
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    # if user admin display, or check if user owns the list
    if list:
        if list.user_id == int(user_id) or user.is_admin:
            return list_schema.dump(list)
        else:
            return (
                jsonify(
                    message=f"List id='{id}' not found for user with email='{user.email}'"
                ),
                404,
            )
    else:
        return (
            jsonify(message=f"List id='{id}' not found"),
            404,
        )


@lists_bp.route("/", methods=["POST"])
@jwt_required()
def create_list():
    body_data = request.get_json()
    list = List(
        name=body_data.get("name"),
        description=body_data.get("description"),
        date=date.today(),
        user_id=get_jwt_identity(),
    )
    db.session.add(list)
    db.session.commit()
    return list_schema.dump(list), 201


@lists_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_list(id):
    body_data = request.get_json()
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    if list:
        if not (user.is_admin or list.user_id == int(user_id)):
            return jsonify(message=f"List with id='{id}' not found for user with email='{user.email}'"), 403
        list.name = body_data.get("name") or list.name
        list.description = body_data.get("description") or list.description
        db.session.commit()
        return list_schema.dump(list)
    else:
        return (
            jsonify(
                message=f"List with id='{id}' not found"
            ),
            404,
        )


@lists_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_list(id):
    user_id = get_jwt_identity()
    user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
    list = db.session.scalar(db.select(List).filter_by(list_id=id))
    if list:
        if not (user.is_admin or list.user_id == int(user_id)):
            return jsonify(message=f"Not authorised to delete list id='{id}'"), 403
        db.session.delete(list)
        db.session.commit()
        return jsonify(message=f"List with id='{id}' deleted'"), 200
    else:
        return jsonify(message=f"List not found with id='{id}'"), 404
