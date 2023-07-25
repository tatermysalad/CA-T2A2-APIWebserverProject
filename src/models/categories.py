from init import db, ma
from marshmallow import fields


class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    date = db.Column(db.Date)

    items = db.relationship("Item", back_populates="category")


class CategorySchema(ma.Schema):
    items = fields.List(fields.Nested("ItemSchema", exclude=["category"]))
    class Meta:
        ordered = True
        fields = ("category_id", "name", "description", "items")
class CategoriesSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("category_id", "name", "description")


category_schema = CategorySchema()
categories_schema = CategoriesSchema(many=True)