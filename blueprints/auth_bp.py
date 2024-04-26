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
    res.set_cookie('user', email, secure=True, expires=expiration_date, domain='.aniksingha.com', samesite='None')
    res.set_cookie('session_id', session_id, httponly=True, secure=True, expires=expiration_date, domain='.aniksingha.com', samesite='None')

    
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

    res.set_cookie('user', email, httponly=True, secure=True, expires=expiration_date, domain='.aniksingha.com', samesite='None')
    res.set_cookie('session_id', session_id, httponly=True, secure=True, expires=expiration_date, domain='.aniksingha.com', samesite='None')

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

@auth_bp.route('/verify_session', methods=["POST"])
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
        response = {"success": False, "message": "session id was incorrect"}
        status_code = 401

    res = make_response(jsonify(response), status_code)

    if res.status_code == 401:
        res.delete_cookie('user')
        res.delete_cookie('session_id')

    return res

@auth_bp.route('/get_cookies', methods=["GET"])
def get_cookies():
    user = request.cookies.get('user')
    session_id = request.cookies.get('session_id')

    if not user or not session_id:
        response = {"success": False, "message": "User or session didn't exist"}
        status_code = 401
    else:
        response = {"success": True, "message": "Success","user": user, "session_id": session_id}
        status_code = 200

    return make_response(jsonify(response), status_code)

@auth_bp.route('/delete_cookies', methods=["DELETE"])
def delete_cookies():
    response = make_response(jsonify({"success": True, "message": "Cookies deleted"}))

    response.delete_cookie('user', secure=True, domain='.aniksingha.com', samesite='None')
    response.delete_cookie('session_id', secure=True, domain='.aniksingha.com', samesite='None')

    return response