from passManager import PassManager
from authManager import AuthManager
from dbClient import client, key   
from flask import Flask, request

pass_manager = PassManager(client, key)
auth_manager = AuthManager(client)

app = Flask(__name__)

@app.route('/register', methods=["GET"])
def register():
    #email = request.args.get('email')
    #password = request.form.get('password')
    #print(email, password)
    return "Hello"
    
if __name__ == "__main__":
    app.run()
