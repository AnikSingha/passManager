from flask import Blueprint, request, jsonify, make_response
from managers.passManager import PassManager
from dbClient import client, key 

pass_bp = Blueprint('pass', __name__)

pass_manager = PassManager(client, key)

@pass_bp.route('/add_account', methods=["POST"])
def add_account():
    data = request.json
    email = data.get('email')    
    website = data.get('website')
    password = data.get('password')

    result, message = pass_manager.add_password(email, website, password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@pass_bp.route('get_accounts', methods=["POST"])
def get_accounts():
    data = request.json
    email = data.get('email')    

    result, message = pass_manager.get_passwords(email)
    
    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@pass_bp.route('update_password', methods=["PUT"])
def update_password():
    data = request.json
    email = data.get('email')    
    website = data.get('website')
    new_password = data.get('new_password')

    result, message = pass_manager.update_password(email, website, new_password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@pass_bp.route('delete_account', methods=["POST"])
def delete_account():
    data = request.json
    email = data.get('email')    
    website = data.get('website')

    result, message = pass_manager.delete_password(email, website)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)