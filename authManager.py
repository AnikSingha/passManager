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
        operation = {"user" : email, "password" : hashed_pass, "accounts" : []}

        try:
            db = self.client["passManager"]
            password_collection = db["passwords"]

            if password_collection.find_one({"user" : email}) != None:
                return False
            
            password_collection.insert_one(operation)

        except Exception as e:
            print(e)
            return False
        
        return True

x = AuthManager(client)

x.add_user("test@gmail.com", "Anik123")

            

    