from passManager import PassManager
from authManager import AuthManager
from dbClient import client, key   
from flask import Flask, request

x = PassManager(client, key)
y = AuthManager(client)

app = Flask(__name__)

@app.route('/register', methods=["GET"])
def register():
    #email = request.args.get('email')
    #password = request.form.get('password')
    #print(email, password)
    return "Hello"
    
app.run()