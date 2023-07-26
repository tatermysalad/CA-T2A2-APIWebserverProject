# Endpoints documentation
### Base URL

The base URL for using the below endpoints can be either localhost or 127.0.0.1 with the port 8080 or as determined by yourself when running `flask run`

[localhost:8080](http://localhost:8080)

[127.0.0.1:8080](http://127.0.0.1:8080)

For example a request to create a user would look like http://localhost:8080/users/register

## User Routes

### /users/register
* Description: create user
* Method: GET
* Authentication: None
* Permission level: Any 
* Request body:
    * Mandatory fields: email, password (minimum length 6)
```json
{
	"first_name" : "Bob",
	"last_name" : "Ross",
	"email" : "bob@ross.com",
	"password" : "123456"
}
```
* Possible responses: 
#### 201 Created
```json
{
	"user_id": 18,
	"f_name": "Bob",
	"l_name": "Ross",
	"email": "bob@ross.com",
	"is_admin": false

}
```
#### 400 Bad Request
```json
{
	"error": "Please enter a password of minimum length 6"
}
```
#### 409 Conflict
```json
{
	"error": "User with email 'bob@ross.com' already exists"
}
```

### /users/login
* Description: login user
* Method: POST
* Authentication: JWT Bearer Token
* Permission level: Any
* Request body:
    * Mandatory fields: email, password
```json
{
	"email" : "bob@ross.com",
	"password" : "123456"
}
```
* Possible responses: 
#### 200 OK
```json
{
	"email": "bob@ross.com",
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MDI2NTEzMSwianRpIjoiOGZlMzU5MmUtZGVkZC00OThhLWJmMDgtZGU3YjFhNTgyODI1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE4IiwibmJmIjoxNjkwMjY1MTMxLCJleHAiOjE2OTAzNTE1MzF9.DD8rC8pa6IAf594PlrANSWzZUzatj28MTbLARG8qV6o",
	"is_admin": false
}
```
#### 401 Unauthorized
```json
{
	"message": "Username or password is incorrect"
}
```

### /users/update/{id}
* Description: update user by ID
* Method: PUT, PATCH
* Authentication: JWT Bearer Token
* Permission level: Admin can update any user and grant admin privileges
* Request body:
    * Updatable fields: first_name, las_name, email, password, is_admin (admin permission required)
```json
{
	"first_name" : "Frida",
	"last_name" : "Kahlo",
	"email" : "Frida@Kahlo.com",
	"password" : "1234567",
	"is_admin" : true
}
```
* Possible responses: 
#### 200 OK
```json
{
	"user_id": 18,
	"f_name": "Frida",
	"l_name": "Kahlo",
	"email": "Frida@Kahlo.com",
	"is_admin": true
}
```
#### 400 Bad Request
```json
{
	"message": "Unable to make change, system requires at least 1 admin"
}
```
#### 403 Forbidden
```json
{
	"message": "User with email='jane@austen.com' not authorised to perform action"
}
```
#### 404 Not Found
```json
{
	"message": "User not found with id='100'"
}
```
#### 409 Conflict
```json
{
	"error": "User with email 'Frida@Kahlo.com' already exists"
}
```
### /users/delete/{id}
* Description: delete user by ID
* Method: DELETE
* Authentication: JWT Bearer Token
* Permission level: Admin
* Request body: None
* Possible responses: 
#### 200 OK
```json
{
	"message": "User with id='2' deleted'"
}
```
#### 403 Forbidden 
```json
{
	"message": "User with email='jane@austen.com' not authorised to perform action"
}
```
#### 404 Not Found
```json
{
	"message": "User not found with id='100'"
}
```

## List Routes

### /lists
* Description: Get users lists 
* Method: GET
* Authentication: None
* Permission level: Admin user will return all lists for every user
* Request body: None
* Possible responses: 
#### 200 OK
```json
[
	{
		"list_id": 1,
		"name": "Bag 1",
		"description": "This is my main bag",
		"date": "2023-07-25",
		"user": {
			"email": "john@tolkien.com"
		},
		"list_items": [
			{
				"list_item_id": 1,
				"quantity": 1,
				"date": "2023-07-25",
				"item": {
					"name": "Tent",
					"description": "X-Mid 2",
					"weight": 1098.0,
					"date": "2023-07-25",
					"category": {
						"name": "Sleeping"
					},
					"user": {
						"email": "john@tolkien.com"
					}
				}
			}
		],
		"total_weight": 1098.0
	},
	{
		"list_id": 2,
		"name": "Bag 2",
		"description": "This is my second bag",
		"date": "2023-07-25",
		"user": {
			"email": "john@tolkien.com"
		},
		"list_items": [
			{
				"list_item_id": 2,
				"quantity": 2,
				"date": "2023-07-25",
				"item": {
					"name": "Sleeping mat",
					"description": "Thermo X-lite",
					"weight": 504.0,
					"date": "2023-07-25",
					"category": {
						"name": "Sleeping"
					},
					"user": {
						"email": "john@tolkien.com"
					}
				}
			}
		],
		"total_weight": 1008.0
	}
]
```

### /lists/{id}
* Description: Get list by ID
* Method: GET
* Authentication: JWT Bearer Token
* Permission level: Admin can retrieve any list
* Request body: None
* Possible responses: 
#### 200 OK
```json
{
	"list_id": 2,
	"name": "Bag 2",
	"description": "This is my second bag",
	"date": "2023-07-25",
	"user": {
		"email": "john@tolkien.com"
	},
	"list_items": [
		{
			"list_item_id": 2,
			"quantity": 2,
			"date": "2023-07-25",
			"item": {
				"name": "Sleeping mat",
				"description": "Thermo X-lite",
				"weight": 504.0,
				"date": "2023-07-25",
				"category": {
					"name": "Sleeping"
				},
				"user": {
					"email": "john@tolkien.com"
				}
			}
		}
	],
	"total_weight": 1008.0
}
```
#### 404 Not Found
```json
{
	"message": "List with id='3' not found for user with email='john@tolkien.com'"
}
```

### /lists
* Description: create list for logged in user
* Method: POST
* Authentication: JWT Bearer Token
* Permission level: Admin
* Request body:
```json
{
	"name" : "Weekend warm weather ultralight bag",
	"description" : "Ultralight bag, without warm weather gear"
}
```
* Possible responses: 
#### 201 OK
```json
{
	"list_id": 4,
	"name": "Weekend warm weather ultralight bag",
	"description": "Ultralight bag, without warm weather gear",
	"date": "2023-07-25",
	"user": {
		"email": "john@tolkien.com"
	},
	"list_items": [],
	"total_weight": 0
}
```

### /lists/{id}
* Description: update list by ID
* Method: PUT, PATCH
* Authentication: JWT Bearer Token
* Permission level: Admin user can update any list
* Request body:
    * Updatable fields: name, description
```json
{
	"name" : "Weekend cold weather ultralight bag",
	"description" : "Ultralight bag, with cold weather gear"
}
```
* Possible responses: 
#### 200 OK
```json
{
	"list_id": 4,
	"name": "Weekend cold weather ultralight bag",
	"description": "Ultralight bag, with cold weather gear",
	"date": "2023-07-25",
	"user": {
		"email": "john@tolkien.com"
	},
	"list_items": [],
	"total_weight": 0
}
```
#### 403 Forbidden 
```json
{
	"error": "Not authorised to edit list id='3'"
}
```
#### 404 Not Found
```json
{
	"message": "List with id='8' not found for user with email='john@tolkien.com'"
}
```
### /lists/{id}
* Description: delete list by ID
* Method: DELETE
* Authentication: JWT Bearer Token
* Permission level: Admin can delete any list
* Request body: None
* Possible responses: 
#### 200 OK
```json
{
	"message": "List with id='4' deleted'"
}
```
#### 403 Forbidden 
```json
{
	"error": "Not authorised to delete list id='3'"
}
```
#### 404 Not Found
```json
{
	"message": "List not found with id='5'"
}
```

## Items Routes

### /items
* Description: List all items
* Method: GET
* Authentication: None
* Permission level: Admin user will return all items regardless of user
* Request body: None
* Possible responses: 
#### 200 OK
```json
[
	{
		"item_id": 2,
		"name": "Tent",
		"description": "X-Mid 2 Pro",
		"weight": 608.0,
		"date": "2023-07-25",
		"category": {
			"name": "Sleeping"
		},
		"user": {
			"email": "jane@austen.com"
		}
	},
    {
		"item_id": 4,
		"name": "Sleeping mat",
		"description": "S2S Pad",
		"weight": 705.0,
		"date": "2023-07-25",
		"category": {
			"name": "Sleeping"
		},
		"user": {
			"email": "jane@austen.com"
		}
	}
]
```

### /items/{id}
* Description: Get item by ID
* Method: GET
* Authentication: JWT Bearer Token
* Permission level: Admin can retrieve any item
* Request body: None
* Possible responses: 
#### 200 OK
```json
[
	{
		"item_id": 2,
		"name": "Tent",
		"description": "X-Mid 2 Pro",
		"weight": 608.0,
		"date": "2023-07-25",
		"category": {
			"name": "Sleeping"
		},
		"user": {
			"email": "jane@austen.com"
		}
	}
]
```
#### 403 Forbidden
```json
{
	"message": "Item with id='1' not found for user with email='jane@austen.com'"
}
```
#### 404 Not Found
```json
{
	"message": "Item with id='1' not found"
}
```

### /items
* Description: create item for logged in user
* Method: POST
* Authentication: JWT Bearer Token
* Permission level: Any
* Request body:
    * Mandatory fields: None
```json
{        
    "name" : "Filter",
    "description" : "water filter",
    "category_id" : 1,
    "weight" : 100
}
```
* Possible responses: 
#### 201 OK
```json
{
	"item_id": 6,
	"name": "Filter",
	"description": "water filter",
	"weight": 100.0,
	"date": "2023-07-26",
	"category": {
		"name": "Sleeping"
	},
	"user": {
		"email": "jane@austen.com"
	}
}
```

### /lists/{id}
* Description: update item by ID
* Method: PUT, PATCH
* Authentication: JWT Bearer Token
* Permission level: Admin user can update any item
* Request body:
    * Updatable fields: name, description, category_id, weight
```json
{        
    "category_id" : 2,
	"weight" : 50
}
```
* Possible responses: 
#### 200 OK
```json
{
	"item_id": 6,
	"name": "Filter",
	"description": "water filter",
	"weight": 50.0,
	"date": "2023-07-26",
	"category": {
		"name": "Hygiene"
	},
	"user": {
		"email": "jane@austen.com"
	}
}
```
#### 403 Forbidden 
```json
{
	"message": "Item with id='1' not found for user with email='jane@austen.com'"
}
```
#### 404 Not Found
```json
{
	"message": "Item with id='11' not found"
}
```
### /lists/{id}
* Description: delete item by ID
* Method: DELETE
* Authentication: JWT Bearer Token
* Permission level: Admin can delete any item
* Request body: None
* Possible responses: 
#### 200 OK
```json
{
	"message": "Item with id='7' deleted'"
}
```
#### 403 Forbidden 
```json
{
	"error": "Not authorised to delete item id='1'"
}
```
#### 404 Not Found
```json
{
	"message": "Item not found with id='11'"
}
```
## List Items Routes

### /lists/{list_id}/items/
* Description: Get all items in a list
* Method: GET
* Authentication: None
* Permission level: User can only retrieve their lists and items. Admin can retrieve any list
* Request body: None
* Possible responses: 
#### 200 OK
```json
[
	{
		"list_item_id": 2,
		"quantity": 1,
		"date": "2023-07-25",
		"list": {
			"name": "Ultralight 1",
			"description": "Ultralight Hiking",
			"date": "2023-07-25",
			"user": {
				"email": "jane@austen.com"
			},
			"total_weight": 0
		},
		"item": {
			"name": "Tent",
			"description": "X-Mid 2 Pro",
			"weight": 608.0,
			"date": "2023-07-25",
			"category": {
				"name": "Sleeping"
			},
			"user": {
				"email": "jane@austen.com"
			}
		}
	},
	{
		"list_item_id": 4,
		"quantity": 1,
		"date": "2023-07-25",
		"list": {
			"name": "Ultralight 1",
			"description": "Ultralight Hiking",
			"date": "2023-07-25",
			"user": {
				"email": "jane@austen.com"
			},
			"total_weight": 0
		},
		"item": {
			"name": "Sleeping mat",
			"description": "S2S Pad",
			"weight": 705.0,
			"date": "2023-07-25",
			"category": {
				"name": "Sleeping"
			},
			"user": {
				"email": "jane@austen.com"
			}
		}
	}
]
```
#### 404 Not Found
```json
{
	"message": "List id='2' not found for user with email='jane@austen.com'"
}
```

### /lists/{list_id}/items
* Description: Add item to a list for logged in user
* Method: POST
* Authentication: JWT Bearer Token
* Permission level: The Item and List must belong to User. Admin can assign any item to any list.
* Request body:
```json
{        
    "quantity" : 4,
    "item_id" : 2
}
```
* Possible responses: 
#### 201 Created
```json
{
	"list_item_id": 5,
	"quantity": 4,
	"date": "2023-07-25",
	"list": {
		"name": "Ultralight 1",
		"description": "Ultralight Hiking",
		"date": "2023-07-25",
		"user": {
			"email": "jane@austen.com"
		},
		"total_weight": 0
	},
	"item": {
		"name": "Tent",
		"description": "X-Mid 2 Pro",
		"weight": 608.0,
		"date": "2023-07-25",
		"category": {
			"name": "Sleeping"
		},
		"user": {
			"email": "jane@austen.com"
		}
	}
}
```
#### 404 Not Found
```json
{
	"message": "List or Item not found for user with email='jane@austen.com'"
}
```

### /list_items/{list_item_id}
* Description: delete list_item by ID
* Method: DELETE
* Authentication: JWT Bearer Token
* Permission level: User can only delete their associations. Admin can delete any list item
* Request body: None
* Possible responses: 
#### 200 OK
```json
{
	"message": "List Item with id='5' deleted"
}
```
#### 403 Forbidden 
```json
{
	"message": "User with email='jane@austen.com' not authorised to perform action on list_item with id='4'"
}
```
#### 404 Not Found
```json
{
	"message": "List_Item not found with id='9"
}
```

## Category Routes

### /categories
* Description: Get all categories
* Method: GET
* Authentication: None
* Permission level: Any
* Request body: None
* Possible responses: 
#### 200 OK
```json
[
	{
		"category_id": 1,
		"name": "Sleeping",
		"description": "For all your sleeping items, tent, sleeping mat, pillow, etc."
	},
	{
		"category_id": 2,
		"name": "Hygiene",
		"description": "For all your hygiene items, like toothbrush, toothpaste, and any medications."
	}
]
```

### /categories/{category_id}
* Description: Get category and items in that category
* Method: GET
* Authentication: JWT Bearer Token
* Permission level: Admin will retrieve all items in the category
* Request body: None
* Possible responses: 
#### 200 OK
```json
{
	"category_id": 1,
	"name": "Sleeping",
	"description": "For all your sleeping items, tent, sleeping mat, pillow, etc.",
	"items": [
		{
			"item_id": 3,
			"name": "Sleeping mat",
			"description": "Thermo X-lite",
			"weight": 504.0,
			"date": "2023-07-25",
			"user": {
				"email": "john@tolkien.com"
			}
		}
	]
}
```
#### 404 Not Found
```json
{
	"message": "Category not found with id='3'"
}
```

### /categories
* Description: Create category
* Method: POST
* Authentication: JWT Bearer Token
* Permission level: Admin only
* Request body:
```json
{        
    "name" : "Clothing",
    "description" : "items of clothing, shirts, shoes, socks, etc."
}
```
* Possible responses: 
#### 201 Created
```json
{
	"category_id": 3,
	"name": "Clothing",
	"description": "items of clothing, shirts, shoes, socks, etc.",
	"items": []
}
```
#### 403 Forbidden
```json
{
	"message": "Not authorised to perform action"
}
```

### /categories/{category_id}
* Description: update category by ID
* Method: PUT, PATCH
* Authentication: JWT Bearer Token
* Permission level: Admin only
* Request body:
    * Updatable fields: name, description
```json
{        
    "name" : "Clothing",
    "description" : "Clothes to be used"
}
```
* Possible responses: 
#### 200 OK
```json
{
	"category_id": 3,
	"name": "Clothing",
	"description": "Clothes to be used",
	"items": []
}
```
#### 403 Forbidden
```json
{
	"message": "Not authorised to perform action"
}
```
#### 404 Not Found
```json
{
	"message": "Category not found with id='9"
}
```
### /categories/{category_id}
* Description: delete category by ID
* Method: DELETE
* Authentication: JWT Bearer Token
* Permission level: Admin only
* Request body: None
* Possible responses: 
#### 200 OK
```json
{
	"message": "Category with id='5' deleted"
}
```
#### 403 Forbidden
```json
{
	"message": "Not authorised to perform action"
}
```
#### 404 Not Found
```json
{
	"message": "Category not found with id='9"
}
```

