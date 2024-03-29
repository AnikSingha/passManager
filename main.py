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

@app.route('/register', methods=["POST"])
def register():
    email = request.args.get('email')
    password = request.args.get('password')

    result = auth_manager.add_user(email, password)

    if result:
        response = {
            "success": True,
            "message": "User registered successfully"
        }
        status_code = 200  # OK
    else:
        response = {
            "success": False,
            "message": "User registration failed"
        }
        status_code = 400  # Bad Request

    return make_response(jsonify(response), status_code)

'''
@app.route('/qr', methods={"GET"})
def testQR():
    email = request.args.get('email')
    print(email)
    qr_bytes = oauth_manager.gen_qrcode(email)

    if qr_bytes:
        qr_base64 = base64.b64encode(qr_bytes.getvalue()).decode('utf-8')
        html_content = f"<img src='data:image/png;base64,{qr_base64}' />"
        return render_template_string(html_content)
    else:
        return "Error generating QR code", 500
'''

if __name__ == "__main__":
    app.run()