from flask import Blueprint, request, jsonify
from init import db, brcypt
from models.users import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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
                    password = bcrypt.generate_password_hash(body_data.get('password').decode('UTF-8'))
            )
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify(error='User with email already exists'), 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return jsonify(error=f'The {err.orig.diag.column_name} is required'), 409