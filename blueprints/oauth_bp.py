from flask import Blueprint, request, jsonify, make_response
from managers.oauth import OAuth
from dbClient import client, oauth_key
import base64

oauth_bp = Blueprint('oauth', __name__)

oauth_manager = OAuth(client, oauth_key)

@oauth_bp.route('/verify_otp', methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get('email')    
    code = data.get('code')
    
    result, message = oauth_manager.verify_code(email, code)
    
    if result:
        response = {"success": True, "message": message}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)

@oauth_bp.route('/create_qr', methods=["POST"])
def create_qr():
    data = request.json
    email = data.get('email')    
    
    result, message = oauth_manager.gen_qrcode(email)

    if result:
        encoded_image = base64.b64encode(message.getvalue()).decode()
        response = {"success": True, "image_data": encoded_image}
        status_code = 200 
    else:
        response = {"success": False, "message": message}
        status_code = 400 

    return make_response(jsonify(response), status_code)
