
### Base URL

The base URL for using the below endpoints can be either localhost or 127.0.0.1 with the port 8080 or as determined by yourself when running `flask run`

[localhost:8080](http://localhost:8080)

[127.0.0.1:8080](http://127.0.0.1:8080)
### Authentication
| Endpoint | Method | Description | Authorization | Request Body (if applicable) | Response Body |
|---|---|---|---|---|---|
| '/auth/register'| POST | Create User Account | Not required | | |
| '/auth/login'   | POST | | Bearer Token | | |
| '/auth/update/{id} | PUT, PATCH || Bearer Token | | |
### Lists
| Endpoint | Method | Description | Authorization | Request Body | Response Body (if applicable) |
|---|---|---|---|---|---|
| '/list' | GET | Get all lists | Token Required | | **200 OK** <br>`{`<br>`  "list_id": 3,`<br>`  "name": "Ultralight 1",`<br>`  "description": "Ultralight Hiking",`<br>`  "date": "2023-07-18",`<br>`  "user": {`<br>`    "email": "jane@austen.com"`<br>`  },`<br>`  "list_items": []`<br>`}` |
| '/list/{id}' | GET | Get a list by ID | | **200 OK** <br>`{`<br>`  "list_id": 3,`<br>`  "name": "Ultralight 1",`<br>`  "description": "Ultralight Hiking",`<br>`  "date": "2023-07-18",`<br>`  "user": {`<br>`    "email": "jane@austen.com"`<br>`  },`<br>`  "list_items": []`<br>`}`<br>**404 Not Found** <br>`{`<br>`  "message": "List with id='1' not found for user with email='jane@austen.com'"`<br>`}`|
| '/list' | POST | Create a new list | `{`<br>`  "name" : "5+ night bag",`<br>`  "description" : "Bag for longer trips"`<br>`}` | **200 OK** <br>`{`<br>`  "list_id": 5,`<br>`  "name": "5+ night bag",`<br>`  "description": "Bag for longer trips",`<br>`  "date": "2023-07-17",`<br>`  "user": {`<br>`    "f_name": "John",`<br>`    "l_name": "Tolkien",`<br>`    "email": "john@tolkien.com"`<br>`  }`<br>`}` |
| '/list/{id}' | PUT, PATCH | Update a list by ID | `{`<br>`  "name" : "Cart",`<br>`  "description" : "Card 5 desc"`<br>`}` | |
| '/list/{id}' | DELETE | Delete a list by ID | | |

