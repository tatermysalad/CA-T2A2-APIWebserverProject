from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.users import User
from models.lists import List
from models.list_items import ListItem
from models.items import Item
from models.categories import Category

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all() # create tables based on models
    print("Tables created")


@db_commands.cli.command("seed")
def seed_db():
    categories = [
        Category(
            name="Sleeping",
            description="For all your sleeping items, tent, sleeping mat, pillow, etc.",
            date=date.today(),
        ),
        Category(
            name="Hygiene",
            description="For all your hygiene items, like toothbrush, toothpaste, and any medications.",
            date=date.today(),
        ),
    ]
    db.session.add_all(categories) # add categories to table using class
    users = [
        User(
            email="admin@admin.com",
            password=bcrypt.generate_password_hash("adminadmin").decode("utf-8"),
            is_admin=True,
            date=date.today(),
        ),
        User(
            f_name="John",
            l_name="Tolkien",
            email="john@tolkien.com",
            password=bcrypt.generate_password_hash("johntolkien").decode("utf-8"),
            date=date.today(),
        ),
        User(
            f_name="Jane",
            l_name="Austen",
            email="jane@austen.com",
            password=bcrypt.generate_password_hash("janeausten").decode("utf-8"),
            date=date.today(),
        ),
    ]
    db.session.add_all(users) # add users to table using class
    lists = [
        List(
            name="Bag 1",
            description="This is my main bag",
            date=date.today(),
            user=users[1],
        ),
        List(
            name="Bag 2",
            description="This is my second bag",
            date=date.today(),
            user=users[1],
        ),
        List(
            name="Ultralight 1",
            description="Ultralight Hiking",
            date=date.today(),
            user=users[2],
        ),
    ]
    db.session.add_all(lists) # add lists to table using class
    items = [
        Item(
            name="Tent",
            description="X-Mid 2",
            weight="1098.0",
            date=date.today(),
            user=users[1],
            category=categories[0],
        ),
        Item(
            name="Tent",
            description="X-Mid 2 Pro",
            weight="608.0",
            date=date.today(),
            user=users[2],
            category=categories[0],
        ),
        Item(
            name="Sleeping mat",
            description="Thermo X-lite",
            weight="504.0",
            date=date.today(),
            user=users[1],
            category=categories[0],
        ),
        Item(
            name="Sleeping mat",
            description="S2S Pad",
            weight="705.0",
            date=date.today(),
            user=users[2],
            category=categories[0],
        ),
        Item(
            name="Toothbrush",
            description="without handle to save weight",
            weight="20.0",
            date=date.today(),
            user=users[2],
            category=categories[1],
        ),
    ]
    db.session.add_all(items) # add items to table using class
    list_items = [
        ListItem(
            list=lists[0],
            item=items[0],
            quantity=1,
            date=date.today(),
        ),
        ListItem(
            list=lists[2],
            item=items[1],
            quantity=1,
            date=date.today(),
        ),
        ListItem(
            list=lists[1],
            item=items[2],
            quantity=2,
            date=date.today(),
        ),
        ListItem(
            list=lists[2],
            item=items[3],
            quantity=1,
            date=date.today(),
        ),
    ]
    db.session.add_all(list_items) # add list_items to table using class
    db.session.commit() # commit the changes to the database
    print("Tables seeded")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all() # delete tables, but leave the database
    print("Tables dropped")
