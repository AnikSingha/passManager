from flask import Flask, make_response
from flask_cors import CORS
from blueprints.auth_bp import auth_bp
from blueprints.pass_bp import pass_bp
from blueprints.oauth_bp import oauth_bp

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pass_bp, url_prefix="/password_management")
app.register_blueprint(oauth_bp, url_prefix="/oauth")

@app.route('/')
def home():
    response = make_response("<h1>Testin</h1>")
    response.set_cookie('user', 'anik@gmail.com', samesite="None")
    return response

if __name__ == "__main__":
    app.run()