## T2A2 API Webserver Project

### Links

[GitHub](https://github.com/tatermysalad/CA-T2A2-APIWebserverProject)
<br>

[Trello](https://trello.com/b/boyMDrFK/t2a2apiwebserver)
<br>

### Contents

[Installation Instructions](#installation-instructions-)

[**R1** - The problem](#req1)

[**R2** - Why do the problems need solving](#req2)

[**R3** - Database system](#req3)

[**R4** - ORM (key functionalities and benefits)](#req4)

[**R5** - Endpoints documentation](#req5)

[**R6** - ERD of the app](#req6)

[**R7** - Detail any third party services in the app](#req7)

[**R8** - Describe project models](#req8)

[**R9** - Discuss the database relations](#req9)

[**R10** - Planning and tracking of tasks](#req10)

## Installation instructions <a name="installation"></a>

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

## **R1** - The problem <a name="#req1"></a>

## **R2** - Why do the problems need solving <a name="#req2"></a>

## **R3** - Database system <a name="#req3"></a>

## **R4** - ORM (key functionalities and benefits <a name="(#req4"></a>

## **R5** - Endpoints documentation <a name="#req5"></a>

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


## **R6** - ERD of the app <a name="#req6"></a>

![Gear Cache API ERD](/docs/GearCacheERD.png)
## **R7** - Detail any third party services in the app <a name="#req7"></a>

## **R8** - Describe project models <a name="#req8"></a>

## **R9** - Discuss the database relations <a name="#req9"></a>

## **R10** - Planning and tracking of tasks <a name="#req10"></a>