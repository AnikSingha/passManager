from flask import Blueprint, request, jsonify, make_response
from authManager import AuthManager
from dbClient import client

auth_bp = Blueprint('auth', __name__)

auth_manager = AuthManager(client)

@auth_bp.route('/register', methods=["GET"])
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

@auth_bp.route('/login', methods=["GET"])
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

@auth_bp.route('/reset_password', methods=["GET"])
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