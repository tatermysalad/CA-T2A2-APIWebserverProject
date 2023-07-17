from init import db, ma
from marshmallow import fields


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


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
