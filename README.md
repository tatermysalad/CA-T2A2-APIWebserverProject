# T2A2 API Webserver Project

## Links

[GitHub](https://github.com/tatermysalad/CA-T2A2-APIWebserverProject)
<br>

[Trello](https://trello.com/b/boyMDrFK/t2a2apiwebserver)
<br>

### Contents

[Installation Instructions](#installation)

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

[References](#references)

## Style guide

[Python Style Guide - Python Enhancement Proposal 8](https://peps.python.org/pep-0008/)

## Installation instructions <a name="installation"></a>

Installation instructions

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

## R1 - Identification of the problem you are trying to solve by building this particular app ]<a name="#req1"></a>

## R2 - Why is it a problem that needs solving ]<a name="#req2"></a>

## R3 - Why have you chosen this database system. What are the drawbacks compared to others ]<a name="#req3"></a>

## R4 - Identify and discuss the key functionalities and benefits of an ORM <a name="#req4"></a>

## R5 - Document all endpoints for your API <a name="#req5"></a>

## R6 - An ERD for your app <a name="#req6"></a>

## R7 - Detail any third party services that your app will use <a name="#req7"></a>

## R8 - Describe your projects models in terms of the relationships they have with each other <a name="#req8"></a>

## R9 - Discuss the database relations to be implemented in your application <a name="#req9"></a>

## R10* - Describe the way tasks are allocated and tracked in your project <a name="#req10"></a>
