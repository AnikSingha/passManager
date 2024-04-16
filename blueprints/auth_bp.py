from flask import Blueprint, request, jsonify, make_response
from managers.authManager import AuthManager
from dbClient import client
import datetime

auth_bp = Blueprint('auth', __name__)

auth_manager = AuthManager(client)

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.json
    email = data.get('email')    
    password = data.get('password')

    result, message, session_id = auth_manager.add_user(email, password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    expiration_date = datetime.datetime.now() + datetime.timedelta(days=3)

    res = make_response(jsonify(response), status_code)
    res.set_cookie('user', email, samesite=True, secure=True, expires=expiration_date)
    res.set_cookie('session_id', session_id, httponly=True, samesite=True, secure=True, expires=expiration_date)

    
    return res

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    result, message = auth_manager.login(email,  password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    _ , session_id = auth_manager.new_session(email)

    res = make_response(jsonify(response), status_code)
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=3)

    res.set_cookie('user', email, samesite=True, secure=True, expires=expiration_date)
    res.set_cookie('session_id', session_id, httponly=True, samesite=True, secure=True, expires=expiration_date)

    return res

@auth_bp.route('/reset_password', methods=["PUT"])
def reset_password():
    data = request.json
    email = data.get('email')    
    new_password = data.get('new_password')

    result, message = auth_manager.reset_password(email, new_password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@auth_bp.route('/verify_session', methods=["GET"])
def verify_session():
    user = request.cookies.get('user')
    session_id = request.cookies.get('session_id')

    if not user or not session_id:
        response = {"success": False, "message": "User or session ID missing"}
        return make_response(jsonify(response), 400)  # Bad request
    
    result = auth_manager.verify_session(session_id, user)

    if result:
        response = {"success": True, "message": "session id was correct"}
        status_code = 200
    else:
        response = {"success": True, "message": "session id was incorrect"}
        status_code = 401

    res = make_response(jsonify(response), status_code)

    if res.status_code == 401:
        res.set_cookie("session_id", "", expires=0)

    return res