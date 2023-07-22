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

The problem being solved by this API web server is to help the travel, ultralight, and hiking community to be more conscious of the weight they carry on their trips and provide a way to track and manage the weight effectively. This application is essential and needs solving for the following reasons:

1. Weight Awareness: Travelers, ultralight enthusiasts, and hikers often face the challenge of carrying limited weight during their journeys. Being conscious of the weight they carry is crucial for their safety, comfort, and overall enjoyment of the trip. Exceeding weight limits can lead to physical strain, fatigue, and increased risk of injuries, particularly during long hikes or demanding travel conditions.
2. Optimised Packing: By offering weight tracking and management capabilities, this API enables users to make informed decisions about what to pack and what to leave behind. It encourages them to pack only the essentials and prioritise lightweight gear, leading to a more efficient and optimised packing process.
3. Environmental Impact: The hiking and travel community is increasingly focused on reducing its environmental footprint. Carrying excessive weight can lead to higher fuel consumption and increased waste generation when items are discarded along the way. This application can contribute to a more sustainable approach by encouraging users to pack thoughtfully and minimize unnecessary items.
4. User Safety: For hikers and adventurers embarking on challenging terrains, managing weight can have a significant impact on their safety. Reducing unnecessary weight can improve balance and stability, reducing the risk of accidents and falls.
5. Improved Experience: Carrying less weight can enhance the overall travel or hiking experience. Lighter loads mean less fatigue, more enjoyment of the surroundings, and the ability to cover longer distances comfortably.
6. Data-Driven Decisions: The API can store historical weight data, enabling users to analyze their packing habits over time. This data-driven approach empowers travelers to identify patterns, make adjustments, and continuously improve their packing strategies for future trips.
7. Community Support: The travel, ultralight, and hiking communities thrive on sharing experiences and knowledge. By providing an API that facilitates weight management and tracking, the application can foster a supportive community where users can exchange tips, recommendations, and insights on how to travel responsibly and efficiently.

## **R3** - Database system

## **R4** - ORM (key functionalities and benefits)

## **R5** - Endpoints documentation

### Base URL

The base URL for using the below endpoints can be either localhost or 127.0.0.1 with the port 8080 or as determined by yourself when running `flask run`

[http://localhost:8080](http://localhost:8080)

[http://127.0.0.1:8080](http://127.0.0.1:8080)

### Authentication

| Endpoint         | Method | Description | Request Body (if applicable) | Response Body (if applicable) |
| ---------------- | ------ | ----------- | ---------------------------- | ----------------------------- |
| '/auth/register' | POST   |             |                              |                               |
| '/auth/login'    | POST   |             |                              |                               |

### Lists

| Endpoint     | Method       | Description         | Request Body (if applicable)                                                             | Response Body (if applicable)                                                                                                                                                                                                                                                                                                                                         |
| ------------ | ------------ | ------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| '/list'      | GET          | Get all lists       |                                                                                          | **200 OK** <br>`{`<br>`  "list_id": 3,`<br>`  "name": "Ultralight 1",`<br>`  "description": "Ultralight Hiking",`<br>`  "date": "2023-07-18",`<br>`  "user": {`<br>`    "email": "jane@austen.com"`<br>`  },`<br>`  "list_items": []`<br>`}`                                                                                                                          |
| '/list/{id}' | GET          | Get a list by ID    |                                                                                          | **200 OK** <br>`{`<br>`  "list_id": 3,`<br>`  "name": "Ultralight 1",`<br>`  "description": "Ultralight Hiking",`<br>`  "date": "2023-07-18",`<br>`  "user": {`<br>`    "email": "jane@austen.com"`<br>`  },`<br>`  "list_items": []`<br>`}`<br>**404 Not Found** <br>`{`<br>`  "message": "List with id='1' not found for user with email='jane@austen.com'"`<br>`}` |
| '/list'      | POST         | Create a new list   | `{`<br>`  "name" : "5+ night bag",`<br>`  "description" : "Bag for longer trips"`<br>`}` | **200 OK** <br>`{`<br>`  "list_id": 5,`<br>`  "name": "5+ night bag",`<br>`  "description": "Bag for longer trips",`<br>`  "date": "2023-07-17",`<br>`  "user": {`<br>`    "f_name": "John",`<br>`    "l_name": "Tolkien",`<br>`    "email": "john@tolkien.com"`<br>`  }`<br>`}`                                                                                      |
| '/list/{id}' | PUT<br>PATCH | Update a list by ID | `{`<br>`  "name" : "Cart",`<br>`  "description" : "Card 5 desc"`<br>`}`                  |                                                                                                                                                                                                                                                                                                                                                                       |
| '/list/{id}' | DELETE       | Delete a list by ID |                                                                                          |                                                                                                                                                                                                                                                                                                                                                                       |

## **R6** - ERD of the app

![Gear Cache API ERD](/docs/GearCacheERD.png)

## **R7** - Detail any third party services in the app

## **R8** - Describe project models

## **R9** - Discuss the database relations

## **R10** - Planning and tracking of tasks
