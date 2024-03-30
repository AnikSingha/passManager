from flask import Blueprint, request, jsonify, make_response
from passManager import PassManager
from dbClient import client, key 

pass_bp = Blueprint('pass', __name__)

pass_manager = PassManager(client, key)

@pass_bp.route('/add_account', methods=["GET"])
def add_account():
    email = request.args.get('email')
    website = request.args.get('website')
    password = request.args.get('password')

    result, message = pass_manager.add_password(email, website, password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@pass_bp.route('get_accounts', methods=["GET"])
def get_accounts():
    email = request.args.get('email')

    result, message = pass_manager.get_passwords(email)
    
    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@pass_bp.route('update_password', methods=["GET"])
def update_password():
    email = request.args.get('email')
    website = request.args.get('website')
    new_password = request.args.get('new_password')

    result, message = pass_manager.update_password(email, website, new_password)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@pass_bp.route('delete_account', methods=["GET"])
def delete_account():
    email = request.args.get('email')
    website = request.args.get('website')

    result, message = pass_manager.delete_password(email, website)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)