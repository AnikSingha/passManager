from passManager import PassManager
from authManager import AuthManager
from oauth import OAuth
from dbClient import client, key, oauth_key  
from flask import Flask, request, jsonify, make_response
import base64

pass_manager = PassManager(client, key)
auth_manager = AuthManager(client)
oauth_manager = OAuth(client, oauth_key)

app = Flask(__name__)

@app.route('/register', methods=["GET"])
def register():
    email = request.args.get('email')       # Must be changed to request.forms when code is sent to production
    password = request.args.get('password')

    result, message = auth_manager.add_user(email, password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@app.route('/login', methods=["GET"])
def login():
    email = request.args.get('email')
    password = request.args.get('password')

    result, message = auth_manager.login(email,  password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@app.route('/reset_password', methods=["GET"])
def reset_password():
    email = request.args.get('email')
    new_password = request.args.get('new_password')

    result, message = auth_manager.reset_password(email, new_password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)


if __name__ == "__main__":
    app.run()