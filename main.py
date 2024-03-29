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
    email = request.args.get('email')
    password = request.args.get('password')

    result, message = auth_manager.add_user(email, password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200  # OK
    else:
        response = {"success": False, "message": message}
        status_code = 400  # Bad Request

    return make_response(jsonify(response), status_code)


if __name__ == "__main__":
    app.run()