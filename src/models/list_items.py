from init import db, ma
from marshmallow import fields


class ListItem(db.Model):
    __tablename__ = "list_items"

    list_item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)

    list_id = db.Column(db.Integer, db.ForeignKey("lists.list_id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)

    list = db.relationship("List", back_populates="list_items")
    item = db.relationship("Item", back_populates="list_items")


class ListItemSchema(ma.Schema):
    list = fields.Nested("ListSchema", exclude=["list_item"])
    item = fields.Nested("ItemSchema", exclude=["list_item"])

    class Meta:
        ordered = True
        fields = ("list_item_id", "list", "item")


list_item_schema = ListItemSchema()
list_items_schema = ListItemSchema(many=True)
