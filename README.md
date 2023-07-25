## T2A2 API Webserver Project

### Links

[GitHub](https://github.com/tatermysalad/CA-T2A2-APIWebserverProject)
<br>

[Trello](https://trello.com/b/boyMDrFK/t2a2apiwebserver)
<br>

### Contents

[Installation Instructions](#installation-instructions)

[**R1** - The problem](#r1---the-problem)

[**R2** - Why does the problem need solving](#r2---why-does-the-problem-need-solving)

[**R3** - Database system](#r3---database-system)

[**R4** - ORM (key functionalities and benefits)](#r4---orm-key-functionalities-and-benefits)

[**R5** - Endpoints documentation](#r5---endpoints-documentation)

[**R6** - ERD of the app](#r6---erd-of-the-app)

[**R7** - Detail any third party services in the app](#r7---detail-any-third-party-services-in-the-app)

[**R8** - Describe project models](#r8---describe-project-models)

[**R9** - Discuss the database relations](#r9---discuss-the-database-relations)

[**R10** - Planning and tracking of tasks](#r10---planning-and-tracking-of-tasks)

## Installation instructions

Clone or download the repository from Github.

Ensure that Python 3 and PostgreSQL is installed. Open command line/terminal and run the following commands:

`psql`

Create a user and set a password:

`CREATE USER gear_dev WITH PASSWORD '123456';`

Create the database by typing:

`CREATE DATABASE gear_cache_db WITH OWNER=gear_dev;`

Grant the user all privileges:

`GRANT ALL PRIVILEGES ON DATABASE gear_cache_db TO gear_dev;`

Connect to the database:

`\c gear_cache_db;`

Open another command line/terminal and run the following commands:

`python3 -m venv .venv`

`source .venv/bin/activate`

Install dependencies:

`pip install -r requirements.txt`

In the /src folder, rename the .envexample file to .env and set the database connection and JWT secret key

`DATABASE_URL="postgresql+psycopg2://gear_dev:123456@localhost:5432/gear_cache_db"`

`SECRET_KEY="example secret key"`

Create, drop and seed the database with the corresponding flask functions. In the console type:

`flask db create`

`flask db seed`

`flask db drop`

Note: The seed command will create some mock records amongst other mock user information.

Run the application:

`flask run`

You should be able to use the application in your browser with the URL prefix 127.0.0.1:5000/, localhost:5000/, or through setup with Insomnia or Postman.

## **R1** - The problem

Every person needs a reliable and efficient system to manage their gear for their travel or everyday needs. The purpose of this API application is to provide all-in-one management solution to a person who is interested in maintaining not only a list of what gear they have, but to combine these into lists to manage the weight for a range of trips, be that hiking, ultralight hiking, or travel.

With this application, users interact with the database using user-friendly RESTful API calls. Problems that can be solved by this application are:
- Users can Create accounts, lists, items (associated with a list), and place items within categories moderated by admin users.
- Users can Read multiple lists via API query to compare weight.
- Users can Update items, and associated these with lists and categories.
- Users can Delete lists, and items.
- Admin user can Update, and Delete Users and their associated list, and items.
## **R2** - Why does the problem need solving

The problem being solved by this API web server is to help the travel, ultralight, and hiking community to be more conscious of the weight they carry on their trips, providing a way to track and manage gear effectively. This application addresses the following:

1. **Weight Awareness:** Travelers, ultralight enthusiasts, and hikers often face the challenge of carrying limited weight during their journeys. Being conscious of the weight they carry is crucial for their safety, comfort, and overall enjoyment of the trip. Exceeding weight limits can lead to physical strain, fatigue, and increased risk of injuries, particularly during long hikes or demanding travel conditions.
2. **Optimised Packing:** By offering weight tracking and management capabilities, this API enables users to make informed decisions about what to pack and what to leave behind. It encourages them to pack only the essentials and prioritise lightweight gear, leading to a more efficient and optimised packing process.
3. **Environmental Impact:** The hiking and travel community is increasingly focused on reducing its environmental footprint. Carrying excessive weight can lead to higher fuel consumption and increased waste generation when items are discarded along the way. This application can contribute to a more sustainable approach by encouraging users to pack thoughtfully and minimize unnecessary items.
4. **User Safety:** For hikers and adventurers embarking on challenging terrains, managing weight can have a significant impact on their safety. Reducing unnecessary weight can improve balance and stability, reducing the risk of accidents and falls.
5. **Improved Experience:** Carrying less weight can enhance the overall travel or hiking experience. Lighter loads mean less fatigue, more enjoyment of the surroundings, and the ability to cover longer distances comfortably.
6. **Data-Driven Decisions:** The API can store historical weight data, enabling users to analyze their packing habits over time. This data-driven approach empowers travelers to identify patterns, make adjustments, and continuously improve their packing strategies for future trips.
7. **Community Support:** The travel, ultralight, and hiking communities thrive on sharing experiences and knowledge. By providing an API that facilitates weight management and tracking, the application can foster a supportive community where users can exchange tips, recommendations, and insights on how to travel responsibly and efficiently.

## **R3** - Database system

The Database system chosen for this application is PostgreSQL due to the following advantages:

1. **Data Integrity and Reliability:** PostgreSQL's support for constraints, triggers, and foreign key relationships ensures that the data in the database remains consistent and reliable. This is crucial for maintaining data quality and preventing data corruption.

2. **ACID Compliance:** The ACID properties provided by PostgreSQL guarantee that transactions are executed reliably and that the database remains in a consistent state even in the face of system failures or concurrent access.

3. **Flexibility and Extensibility:** PostgreSQL's support for user-defined functions, procedural languages, and extensions allows us to tailor the database to meet our application's specific requirements. This level of customization enables us to handle complex data structures and operations efficiently.

4. **Scalability:** PostgreSQL's ability to scale horizontally with replication and sharding capabilities allows us to handle growing amounts of data and increasing user demands as our application's user base expands.

5. **JSON Support:** The native support for JSON data in PostgreSQL allows us to store and query semi-structured data, providing us with the flexibility of a NoSQL database within the context of a robust relational database system.

6. **Open Source and Active Community:** Choosing an open-source database like PostgreSQL ensures that we have access to a vast community of developers continuously improving the software. We benefit from regular updates, bug fixes, and security patches, ensuring the database remains up-to-date and secure.

7. **Maturity and Stability:** PostgreSQL's long history and proven track record of stability make it a reliable choice for our application. We can be confident that it can handle our data with efficiency and minimal risk of data loss.

8. **Cross-Platform Support:** PostgreSQL's compatibility with various operating systems ensures that we can deploy our application on different platforms without major changes to the database setup.

9. **Security Features:** PostgreSQL's built-in security features, such as SSL encryption, user authentication mechanisms, and fine-grained access controls, help us protect our data from unauthorized access and ensure data privacy.

10. **Community Support and Resources:** The active PostgreSQL community provides us with access to a wealth of resources, documentation, forums, and expert advice, making it easier to troubleshoot issues, optimize performance, and learn best practices.

By leveraging PostgreSQL's strengths, we can build a robust, scalable, and efficient application that meets the demands of our users while ensuring the integrity and reliability of our data.


While PostgreSQL is a powerful and versatile database management system, like any technology, it has its limitations compared to other database systems. Here are some drawbacks of PostgreSQL when compared to other databases:

1. **Performance:** In certain scenarios, other databases may outperform PostgreSQL, especially for specific use cases with massive write-heavy workloads. Some NoSQL databases, for example, may handle high write throughput more efficiently.

2. **Learning Curve:** PostgreSQL's advanced features and capabilities may come with a steeper learning curve for developers who are less familiar with relational databases or who have primarily worked with NoSQL databases.

3. **No Built-in Replication for Sharding:** Unlike some other databases designed specifically for sharding, PostgreSQL's built-in replication doesn't handle automatic sharding. Sharding in PostgreSQL requires custom solutions, which can be complex to set up and maintain.

4. **Memory Usage and Tuning:** PostgreSQL's memory management and configuration require careful tuning to optimize performance. This process can be challenging, and misconfigurations may lead to suboptimal performance.

5. **Limited Native Support for NoSQL:** While PostgreSQL does support JSON data and some NoSQL-like features, it may not be as performant or intuitive as dedicated NoSQL databases for certain types of unstructured or semi-structured data.

6. **Backup and Restore Times:** PostgreSQL's backup and restore times can be slower compared to some other databases, especially when dealing with large volumes of data.

7. **Limited GUI Tools:** While there are some GUI tools available for PostgreSQL, they might not be as feature-rich or user-friendly as those available for more popular database systems.

8. **Less Prevalent in Some Ecosystems:** In certain ecosystems or industries, other databases might be more widely used and have better integration with other tools and frameworks.

9. **Spatial Data Handling:** While PostgreSQL has some support for spatial data and Geographic Information System (GIS) functionality, it may not be as comprehensive as specialized spatial databases.

10. **Community and Third-Party Ecosystem:** While PostgreSQL has an active community, it may not have as extensive a third-party ecosystem and plugin support as some other databases, leading to potentially fewer pre-built integrations or extensions.

## **R4** - ORM (key functionalities and benefits)

ORM stands for Object Relational Mapper, which supports the interactions between an application and its database.  

This application uses SQLAlchemy for this task as it is highly compatible with Flask and Python, as well as being database-agnostic

Key functionalities of SQLAlchemy: 
- Tables in Python are determined with classes which extend the ORM's model class (db.Model), and they behave as such in Python i.e. a database 'record' is an object, or an instance of the class. For example

```py
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String)
    l_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.Date)
```

#### A record is declared just like an object 

```py
    user = User(
            f_name="Jane",
            l_name="Austen",
            email="jane@austen.com",
            password="janeausten",
            date=date.today()
    )
```
#### With the declaration through the ORM, columns within the database become attributes of the class. This can use data types which are similar to python, and added .

```py
password = db.Column(db.String)
```


#### Foreign keys can be declared using the tables defined class

```py
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
```

#### Relationships between tables are represented by relationship method

```py
    user = db.relationship("User")

```

- Functions are converted to SQL by ORM

Python function:
```py
    def select_user():
        user = db.session.scalar(db.select(User).filter_by(user_id=1))
        return user.name
```
The SQL equivalent of it is:
```SQL
    select name from users where id = 1;
```

- SQLalchemy supports actions like select, query, commit, delete, add, update, which correlate to actions made in a SQL database.

```py
    user = db.session.scalar(db.select(User).filter_by(user_id=2))
    db.session.delete(user)
    db.session.commit()
```

Key benefits of an ORM are:
- It allows querying and manipulation of a database using a programming language, therefore, it reduces the length and complexity of code compared to embedded SQL.
- It makes the development process easier because developers do not need to switch between their coding language and SQL.
- It has great support for tasks such as connections, seeds and migrations. As a result, implementation is straightforward. 
- It protects data from direct SQL injections because does not take explicit SQL queries and requires all interactions performed on OOP objects instead of database tables.
- It is database-agnostic which makes switching from one database (for development) to another one (for deployment) seamless whilst keeping the code base consistent. 


## **R5** - Endpoints documentation

[Click here for the Endpoint documentation](/docs/endpoints.md)

## **R6** - ERD of the app

![Gear Cache API ERD](/docs/GearCacheERD.png)

## **R7** - Detail any third party services in the app

1. Web framework: Flask, which is a microframework used to develop web applications in Python. It comes with a built-in development server and has a fast debugger. Flask 2.2.2 is used in this application.

2. Object Relational Mapper: SQLAlchemy - facilitates the communication between Python programs and the database (PostgreSQL in this case). It translates database tables into Python objects, and converts function calls into SQL statements. In the app, Flask - SQLAlchemy is used, because it is specifically designed to work with Flask, making SQLAlchemy compatible with a Flask app. The version of SQLAlchemy is 1.4.42 and Flask-SQLAlchemy in the app is 3.0.2.

3. Serialization and deserialization library: Marshmallow - it is framework-agnostic, and it helps convert complex datatypes into native Python datatypes. Marshmallow version in the app is 3.18.0. In this app, Flask - Marshmallow is used because it comes with additional features to make Marshmallow fully compatible with a Flask app, and marshmallow-sqlalchemy is another package that integrates SQLAlchemy and Marshmallow. The version of Flask-Marshmallow is 0.14.0, and marshmallow-sqlalchemy is 0.28.1

4. PostgreSQL and Python adapter: psycopg2, its functions are to match Python data types with PostgreSQL datatypes. It also comes with thread safety feature which is desireable in heavily multi-threaded applications that make a large number of concurrent "INSERT"s or "UPDATE"s. The version of psycopg2 used in the app is 2.9.4

5. Hashing utility: Bcrypt - its special feature is slow hashing, which prevents brute force attacks on sensitive data such as passwords. In the app, Flask-Bcrypt is used because it comes fully compatible with a Flask app. The version of Flask-Bcrypt is 1.0.1. 

6. Authorization: JSON Web Token (JWT), provides a secure and compact tool for user authentication. Once logged in, a token will be generated and it will be included in all subsequent requests made by the client, and allows them access to routes, services and resources that are permitted with that token. In the app, the secret key method of signing is used, and Flask-JWT-Extended is required extension, its version is 4.4.4


## **R8** - Describe project models

There are 5 models used in this application - Users, Lists, Items, List Items, and Categories.

1. User Model:

#### Model declaration:
```py
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
```
Relationship to List and Item model is the same. 
One and only one to zero or many ie. one user can have zero or many lists and items.
When a user is deleted so is their associated lists and items.

'user_id' is the primary key of the Users table, and is therefore the foreign key used in the corresponding List and Item tables.

#### Schema declaration:
```py
class UserSchema(ma.Schema):
    lists = fields.List(fields.Nested("ListSchema", exclude=["user"]))
    items = fields.List(fields.Nested("ItemSchema", exclude=["user"]))

    class Meta:
        ordered = True
        fields = ("user_id", "f_name", "l_name", "email", "password", "is_admin")

    password = ma.String(validate=Length(min=6))


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
```
In the UserSchema, when called the users corresponding lists and items are nested, and as there can be multiple these are also listed, which gives more value to the response. 

In both of these cases we remove the 'user' field as it will create a loop. 

When used as 'user_schema' or 'users_schema' we exclude the password from visibility.



## **R9** - Discuss the database relations

## **R10** - Planning and tracking of tasks
