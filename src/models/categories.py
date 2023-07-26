from init import db, ma
from marshmallow import fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.items import ItemSchema
from models.users import User


class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    date = db.Column(db.Date)

    items = db.relationship("Item", back_populates="category")


class CategorySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("category_id", "name", "description", "items")

    # Custom method to filter items in category based on the user
    def filter_items(self, category):
        user_id = get_jwt_identity()
        # get user by jwt_id
        user = db.session.scalar(db.select(User).filter_by(user_id=user_id))
        # Filter items to include only those that belong to the current user or all if admin
        filtered_items = [item for item in category.items if item.user_id == int(user_id) or user.is_admin]

        item_schema = ItemSchema(exclude=["category"]) 
        items = item_schema.dump(filtered_items, many=True)
        return items
    
    items = fields.Method("filter_items")
class CategoriesSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("category_id", "name", "description")


category_schema = CategorySchema()
categories_schema = CategoriesSchema(many=True)