from flask import Flask
import os
from init import db, ma, bcrypt, jwt 
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.list_controller import list_bp
from controllers.item_controller import item_bp
from controllers.list_item_controller import list_item_bp
from controllers.category_controller import category_bp

def create_app():
    app = Flask(__name__)

    app.json.sort_keys =  False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)

    app.register_blueprint(auth_bp)

    app.register_blueprint(list_bp)

    app.register_blueprint(item_bp)

    app.register_blueprint(list_item_bp)

    app.register_blueprint(category_bp)

    return app
