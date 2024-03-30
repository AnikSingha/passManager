from flask import Flask
from flask_cors import CORS
from blueprints.auth_bp import auth_bp
from blueprints.pass_bp import pass_bp
from blueprints.oauth_bp import oauth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pass_bp, url_prefix="/password_management")
app.register_blueprint(oauth_bp, url_prefix="/oauth")


if __name__ == "__main__":
    app.run()