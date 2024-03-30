from flask import Blueprint, request, jsonify, make_response
from oauth import OAuth
from dbClient import client, oauth_key

oauth_bp = Blueprint('oauth', __name__)

oauth_manager = OAuth(client, oauth_key)

@oauth_bp.route('verify_otp', methods=["GET"])
def verify_otp(email, code):
    email = request.args.get("email")
    code = request.args.get("code")

    result, message = oauth_manager.verify_code(email, code)

    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)
    

