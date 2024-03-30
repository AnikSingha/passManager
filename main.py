from flask import Flask
from blueprints.auth_bp import auth_bp
from blueprints.pass_bp import pass_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pass_bp, url_prefix="/password_management")


if __name__ == "__main__":
    app.run()