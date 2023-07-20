from flask import Blueprint, request, jsonify
from init import db, bcrypt
from models.users import User, user_schema, users_schema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return jsonify(message=f"User with email='{user.email}' not authorised to perform action"),403
    return wrapper


@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        body_data = request.get_json()
        # Create a new user based on POST information
        if body_data.get('password'):
            user = User(
                    f_name = body_data.get('first_name'),
                    l_name = body_data.get('last_name'),
                    email = body_data.get('email'),
                    password = bcrypt.generate_password_hash(body_data.get('password')).decode('UTF-8')
            )
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify(error=f"User with email '{request.get_json().get('email')}' already exists"), 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return jsonify(error=f'The {err.orig.diag.column_name} is required'), 409
        
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    user = db.session.scalar(db.select(User).filter_by(email=body_data.get('email')))
    if user and bcrypt.check_password_hash(user.password,body_data.get('password')):
        token = create_access_token(identity=str(user.user_id),expires_delta=timedelta(days=1))
        return jsonify(email=user.email, token=token, is_admin=user.is_admin)
    else:
        return jsonify(message="Username or password is incorrect or doesn't exist"), 401
    
@auth_bp.route('/<int:id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_account():
    pass

@auth_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_user(id):
    user = db.session.scalar(db.select(User).filter_by(user_id=id))
    if not user.is_admin:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message=f"User with id='{id}' deleted'"), 200
    else:
        return jsonify(message=f"User not found with id='{id}'"), 404