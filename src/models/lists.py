from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length


class List(db.Model):
    __tablename__ = "lists"

    list_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    user = db.relationship("User", back_populates="lists")
    list_items = db.relationship(
        "ListItem", back_populates="list", cascade="all,delete"
    )


class ListSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["email"])
    list_items = fields.List(fields.Nested("ListItemSchema", exclude=["list"]))
    category = fields.Nested("CategorySchema", only=['name'])

    class Meta:
        ordered = True
        fields = ("list_id", "name", "description", "date", "user", "category", "list_items")


list_schema = ListSchema()
lists_schema = ListSchema(many=True)
