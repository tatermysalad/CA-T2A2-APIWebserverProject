from flask import Flask
import os
from init import db, ma, bcrypt, jwt 
from controllers.cli_controller import db_commands
from controllers.user_controller import users_bp
from controllers.list_controller import lists_bp
from controllers.item_controller import items_bp
from controllers.category_controller import categories_bp

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

    app.register_blueprint(users_bp)

    app.register_blueprint(lists_bp)

    app.register_blueprint(items_bp)

    app.register_blueprint(categories_bp)

    return app
