#### Task 1:

---------

##### Base URL - http://0.0.0.0:5000

##### Routes
- **GET /** -> fetches all the server objects from the DB
- **GET /?server=<server_id>** -> fetches the server object corresponding to server_id
- **PUT /** => *Body ("name", "id", "language", "framework")* -> Adds an object to the DB with the provided details
- **DELETE /?server=<server_id>** -> Removes the server object corresponding to server_id from the DB
- **GET /find?name=<name>** -> Find the server whose names contain this "name"

---------

##### Description

Python version used while development: 3.5.4
Software used for testing: POSTman

For running the app, follow one of the below snippets:
 - ```pip install -r requirements.txt```<br>
    ```mongod```<br>
    ```python script.py```
 -  ```docker-compose up --build```
 
The first time docker execution takes some amount of time because downloads the ubuntu and mongo image from docker hub.

Application Details: <br>
 - IP on which app runs: 0.0.0.0
 - Port on which app runs: 5000

------

##### Screenshots of POSTman depicting the testing of different routes with their respective responses are in the "screenshots" folder

-------