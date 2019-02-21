from flask import Flask, jsonify, request
import ast
from bson.json_util import dumps
from flask_pymongo import PyMongo

app = Flask(__name__)

## Configuring the local mongodb instance
#app.config["MONGO_URI"] = os.environ.get("REMOTE_DB") #Link to mlab url - provided in docker-compose file
app.config["MONGO_URI"] = "mongodb://mongodb:27017/kaiburr-task"
mongo = PyMongo(app)

## The first four routes specified in the documention
@app.route("/", methods=["GET", "PUT", "DELETE"])
def server():
    response = {}

    ### When GET / or GET /?server=<server_id> is executed
    if request.method == "GET":

        ## Fetching the server_id from the request url parameter "server"
        server_id = request.args.get("server")

        ## If a server_id is passed in the parameter - return that server's details
        if server_id:
            server_obj = dumps(mongo.db.Server.find_one({"id": server_id}))

            ## Checking whether the server object is found in the DB for the provided server_id
            try:
                if server_obj:
                    response = {
                        "success": True,
                        "message": "Server details fetched for the provided server id",
                        "server": ast.literal_eval(server_obj),
                        "code": 200
                    }
                else:
                    response = {
                        "success": False,
                        "message": "Server not found with provided Server ID",
                        "code": 404
                    }
            except:
                response = {
                    "success": False,
                    "message": "Server not found with provided Server ID",
                    "code": 404
                }
        ## Else, return all the servers
        else:
            query = mongo.db.Server.find({})
            server_objs = ast.literal_eval(dumps(query))
            ## Checking whether the database contains any server objects or not
            if server_objs and len(server_objs)>0:
                response = {
                    "success": True,
                    "message": "Server details fetched for all the server in the database",
                    "server": server_objs,
                    "code": 200
                }
            else:
                response = {
                    "success": False,
                    "message": "No server found in the Database. Please add some server objects in DB",
                    "code": 404
                }

    ## When PUT/ is executed
    elif request.method == "PUT":
        ## If the data is passed as application/json
        if request.is_json:
            content = request.get_json()
        ## If the data is passed as application/x-www-form-urlencoded
        else:
            content = request.form

        ## Fetching the request body parameters
        name = content["name"]
        server_id = content["id"]
        language = content["language"]
        framework = content["framework"]

        ## Checking whether any request body parameter is null or not
        if name and server_id and language and framework:
            server_obj = {
                "name": name,
                "id": server_id,
                "language": language,
                "framework": framework
            }
            mongo.db.Server.insert(server_obj)
            response = {
                "success": True,
                "message": "Added the object with server_id: {} to the Database".format(server_id),
                "code": 200
            }
        else:
            response = {
                "success": False,
                "message": "Please enter all the values in the request body",
                "code": 400
            }

    ## When DELETE /?server=<server_id> is executed
    elif request.method == "DELETE":
        ## Fetching the server_id from the request url parameter "server"
        server_id = request.args.get("server")

        ## Checking if the server id is provided in the request url as parameter or not
        if server_id:
            server_obj = mongo.db.Server.find_one({"id": server_id})
            if server_obj:
                mongo.db.Server.delete_one({"id": server_id})
                response = {
                    "success": True,
                    "message": "Server object corresponding to server_id: {} removed from the DB".format(server_id),
                    "code": 200
                }
            else:
                response = {
                    "success": False,
                    "message": "No server object found with the server_id: {}".format(server_id),
                    "code": 404
                }

    ## If any other request method is executed under the route /
    else:
        response = {
            "success": False,
            "message": "Wrong endpoint!",
            "code": 404
        }

    ## Finally, returning the response
    return jsonify(response), response["code"]


## GET/find?name=<name>
@app.route("/find", methods=["GET"])
def search_by_name():
    name = request.args.get("name")

    query = mongo.db.Server.find({})
    server_objs = ast.literal_eval(dumps(query))

    final_objs = []

    for obj in server_objs:
        if name in obj["name"]:
            final_objs.append(obj)

    response = {
        "success": True,
        "message": "Server details fetched for all the server in the database",
        "server": final_objs,
        "code": 200
    }

    return jsonify(response), response["code"]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")