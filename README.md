## T2A2 API Webserver Project

### Links

[GitHub](https://github.com/tatermysalad/CA-T2A2-APIWebserverProject)
<br>

[Trello](https://trello.com/b/boyMDrFK/t2a2apiwebserver)
<br>

### Contents

[Installation Instructions](#installation-instructions)

[**R1** - The problem](#r1---the-problem)

[**R2** - Why do the problems need solving](#r2---why-do-the-problems-need-solving)

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

```psql```

Create a user and set a password:

```CREATE USER gear_dev WITH PASSWORD '123456';```

Create the database by typing:

```CREATE DATABASE gear_cache_db WITH OWNER=gear_dev;```

Grant the user all privileges:

```GRANT ALL PRIVILEGES ON DATABASE gear_cache_db TO gear_dev;```

Connect to the database:

```\c gear_cache_db;```

Open another command line/terminal and run the following commands:

```python3 -m venv .venv```

```source .venv/bin/activate```

Install dependencies:

```pip install -r requirements.txt```

In the /src folder, rename the .envexample file to .env and set the database connection and JWT secret key

```DATABASE_URL="postgresql+psycopg2://gear_dev:123456@localhost:5432/gear_cache_db"```

```SECRET_KEY="example secret key"```

Create, drop and seed the database with the corresponding flask functions. In the console type:

```flask db create```

```flask db seed```

```flask db drop```

Note: The seed command will create some mock records amongst other mock user information.

Run the application:

```flask run```

You should be able to use the application in your browser with the URL prefix 127.0.0.1:5000/, localhost:5000/, or through setup with Insomnia or Postman.

## **R1** - The problem 

## **R2** - Why do the problems need solving 

## **R3** - Database system 

## **R4** - ORM (key functionalities and benefits 

## **R5** - Endpoints documentation 

### Authentication
| Endpoint    | Method | Description | Request Body (if applicable) | Response Body (if applicable) |
|---------|-----|--------|--------|--------|
| '/auth/register'| POST | | | |
| '/auth/login'   | POST | | | |
### Lists
| Endpoint    | Method | Description | Request Body (if applicable) | Response Body (if applicable) |
|---------|-----|--------------------|--------|--------|
| '/list' | GET | | | |
| '/list/{id}' | GET | | | |
| '/list' | POST | | {"name" : "Cart", "description" : "Card 5 desc"}| |
| '/list/{id}' | POST | | {<br>     "name" : "Cart", <br>       "description" : "Card 5 desc"<br>}| |


## **R6** - ERD of the app 

![Gear Cache API ERD](/docs/GearCacheERD.png)
## **R7** - Detail any third party services in the app 

## **R8** - Describe project models 

## **R9** - Discuss the database relations 

## **R10** - Planning and tracking of tasks 