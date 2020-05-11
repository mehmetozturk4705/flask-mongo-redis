# Flask-Redis-MongoDB Sample Project
###### Mehmet Öztürk

This sample project uses microservices approach to flask applications which leverages **MongoDB** as persistence layer and **Redis** as caching layer.

You must install Docker and docker-compose packages prior to running this application.

You may use commands below in order to run the application.

    docker-compose build
    docker-compose up -d
   
In order to validate inputs [jsonchema](https://pypi.org/project/jsonschema/) has been used.

For password hashing [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/) library has been used

### Endpoints

There is one resource endpoint which makes crud operations. Due to the fact that case deliveries should have jsonschema validation support, endpoints accept only raw json inputs. 

Operations shown below are used in order to manipulate user data without authorization need.

* **GET** */user/*  (Lists users)
* **GET** */user/\<id>*  (Retrieve user from cache or mongodb)
* **POST** */user/* (Create new user)
* **PUT** */user/\<id>* (Update single user)
* **DELETE** */user/\<id>* (Delete user)
* **OPTIONS** */user/* (Show jsonschema)
* **OPTIONS** */user/\<id>* (Show detail jsonschema)

Operation below retrieves a JWT token for using change password endpoint.
* **POST** */login/* (Login endpoint)
* **OPTIONS** */login/* (Show login validation jsonschema)

In order to use changepassword operation you need a JWT token and push it as Bearer token to this endpoint.
* **POST** */changepassword/* (You can change password of user which is encrypted in JWT token)
* **OPTIONS** */changepassword/* (Show changepassword validation jsonschema.)

### Notes
***Redis*** *and* ***MongoDb*** services does not need password for authentication.


