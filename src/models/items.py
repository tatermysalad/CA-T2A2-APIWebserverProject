from flask_jwt_extended import get_jwt_identity
from init import db, ma
from marshmallow import fields
from models.users import User


class Item(db.Model):
    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    weight = db.Column(db.Float, default=0.0)
    date = db.Column(db.Date)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    category = db.relationship("Category", back_populates="items")
    user = db.relationship("User", back_populates="items")
    list_items = db.relationship(
        "ListItem", back_populates="item", cascade="all,delete"
    )


class ItemSchema(ma.Schema):
    category = fields.Nested("CategorySchema", only=['name'])
    user = fields.Nested("UserSchema", only=["email"])

    class Meta:
        ordered = True
        fields = (
            "item_id",
            "name",
            "description",
            "weight",
            "date",
            "category",
            "user",
        )

    # Custom method to filter items based on the user
    def filter_items(self, item):
        user_id = get_jwt_identity()
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))

        # Check if the user is an admin or the item belongs to the user
        if item.user_id == int(user_id) or user.is_admin:
            return item

        # Return None to exclude the item from the result if the condition is not met
        return None

    # Override the "item" field to apply the custom filter
    item = fields.Method("filter_items", data_key="item")

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
