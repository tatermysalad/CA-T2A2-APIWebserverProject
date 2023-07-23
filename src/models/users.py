from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String)
    l_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.Date)

    lists = db.relationship("List", back_populates="user", cascade="all, delete")
    items = db.relationship("Item", back_populates="user", cascade="all,delete")


class UserSchema(ma.Schema):
    lists = fields.List(fields.Nested("ListSchema", exclude=["user"]))
    items = fields.List(fields.Nested("ItemSchema", exclude=["user"]))

    class Meta:
        ordered = True
        fields = ("user_id", "f_name", "l_name", "email", "password", "is_admin")

    password = ma.String(validate=Length(min=6))


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
