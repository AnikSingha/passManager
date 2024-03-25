import bcrypt
from dbClient import client

class AuthManager:

    def __init__(self, client):
        self.client = client

    def addUser(self, email, password):
        
        try:
            db = self.client["accounts"]
        except:
            pass
            

    