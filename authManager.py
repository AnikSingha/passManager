import bcrypt
from dbClient import client

class AuthManager:

    def __init__(self, client):
        self.client = client

    def hash_password(self, password):
        encoded = password.encode('utf-8')
        hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
        return hashed
    
    def check_password(self, password, hash):
        encoded = password.encode('utf-8')
        return bcrypt.checkpw(encoded, hash)
    
    def add_user(self, email, password):
        hashed_pass = self.hash_password(password)

        try:
            db = self.client["passManager"]

            accounts_collection = db["accounts"]
            password_collection = db["passwords"]

            accounts_collection.insert_one({email : hashed_pass})
            password_collection.insert_one()

        except Exception as e:
            pass


            

    