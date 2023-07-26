from init import db, ma
from marshmallow import fields, post_dump

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
    list_items = fields.List(fields.Nested("ListItemSchema", only=["quantity", "item"]))

    # New field for total weight
    total_weight = fields.Float(dump_only=True)

    # Post dump method to calculate the total weight based on list_items
    @post_dump
    def calculate_total_weight(self, data, **kwargs):
        list_items = data.get('list_items', [])
        total_weight = [item.get('quantity', 1) * item["item"].get('weight', 0) for item in list_items]
        data['total_weight'] = sum(total_weight)
        return data
    class Meta:
        ordered = True
        fields = ("list_id", "name", "description", "date", "user", "list_items", "total_weight")

list_schema = ListSchema()
lists_schema = ListSchema(many=True)
