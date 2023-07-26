from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from init import db, bcrypt
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, date
import functools
from models.users import User, user_schema

users_bp = Blueprint("users", __name__, url_prefix="/users")


def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        # get user by jwt_id
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return (
                jsonify(
                    message=f"User with email='{user.email}' not authorised to perform action"
                ),
                403,
            )

    return wrapper


@users_bp.route("/register", methods=["POST"])
def user_register():
    # try and create user, if an exception comes back it is due to not null or uniqueness
    try:
        body_data = request.get_json()
        # Create a new user based on POST information
        password = body_data.get("password")
        # checks if password exists and is longer than 6 characters < the length validation wasn't working as it was hashed.
        if password and len(password) >= 6:
            user = User(
                f_name=body_data.get("first_name"),
                l_name=body_data.get("last_name"),
                email=body_data.get("email"),
                password=bcrypt.generate_password_hash(
                    body_data.get("password")
                ).decode("utf-8"),
                date=date.today(),
            )
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 201
        else:
            return jsonify(message="Please enter a password of minimum length 6"), 400
    except IntegrityError as err:
        # if the user already exists
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return (
                jsonify(
                    message=f"User with email '{request.get_json().get('email')}' already exists"
                ),
                409,
            )
        # if the not null column is not filled
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return jsonify(message=f"The {err.orig.diag.column_name} is required"), 409


@users_bp.route("/login", methods=["POST"])
def user_login():
    body_data = request.get_json()
    # get user by body_data email
    user = db.session.scalar(db.select(User).filter_by(email=body_data.get("email")))
    # decrypt the password and login
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(
            identity=str(user.user_id), expires_delta=timedelta(days=1)
        )
        return jsonify(email=user.email, token=token, is_admin=user.is_admin)
    # failed login
    else:
        return jsonify(message="Username or password is incorrect"), 401


@users_bp.route("/update/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
def update_account(id):
    body_data = request.get_json()
    # get user by id
    user = db.session.scalar(db.select(User).filter_by(user_id=id))
    # try and create user, if an exception comes back it is due to not null or uniqueness
    try:
        if user:
            # the system requires one admin, otherwise no one can update categories, or update and delete users
            if user.is_admin and body_data.get("is_admin") == False:
                admin_count = db.session.query(User).filter_by(is_admin=True).count()
                if admin_count < 2:
                    return (
                        jsonify(
                            message="Unable to make change, system requires at least 1 admin"
                        ),
                        400,
                    )
            user.f_name = body_data.get("first_name") or user.f_name
            user.l_name = body_data.get("last_name") or user.l_name
            user.email = body_data.get("email") or user.email
            user.password = (
                bcrypt.generate_password_hash(body_data.get("password")).decode("utf-8")
                or user.password
            )
            # if statement to check if the boolean value exists, this is to avoid comparing true or false values
            user.is_admin = (
                body_data.get("is_admin") if "is_admin" in body_data else user.is_admin
            )
            db.session.commit()
            return user_schema.dump(user)
        else:
            return jsonify(message=f"User not found with id='{id}'"), 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return (
                jsonify(
                    message=f"User with email '{request.get_json().get('email')}' already exists"
                ),
                409,
            )
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return jsonify(message=f"The {err.orig.diag.column_name} is required"), 409


@users_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_user(id):
    # select user by id
    user = db.session.scalar(db.select(User).filter_by(user_id=id))
    # only delete user if not an admin, prevents accidental deletion of admins and makes sure there has to be 1 admin
    if not user.is_admin:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message=f"User with id='{id}' deleted'"), 200
    else:
        return jsonify(message=f"User not found with id='{id}'"), 404
