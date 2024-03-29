from passManager import PassManager
from authManager import AuthManager
from oauth import OAuth
from dbClient import client, key, oauth_key  
from flask import Flask, request, render_template_string
import base64

pass_manager = PassManager(client, key)
auth_manager = AuthManager(client)
oauth_manager = OAuth(oauth_key, client)


app = Flask(__name__)

@app.route('/register', methods=["GET"])
def register():
    #email = request.args.get('email')
    #password = request.form.get('password')
    #print(email, password)
    return "Hello"

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
    
if __name__ == "__main__":
    app.run()
