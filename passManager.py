from dbClient import client, key
from cryptography.fernet import Fernet
import bcrypt

class PassManager:
    def __init__(self, client):
        self.key = key
        self.cipher = Fernet(self.key)
        self.client = client
    
    def decodePasswords(self, passwords):
        for key, val in passwords.items():
            decrypted = self.cipher.decrypt(val).decode()
            passwords[key] = decrypted
        
        return passwords

    def getPasswords(self, userName):
        db = self.client["passManager"]

        try:
            user = db.passwords.find_one({"user" : userName})
        except Exception as e:
            print(e)
            return False

        return self.decodePasswords(user["accounts"])
    
    def addPassword(self, user, website, password):
        encryptedPass = self.cipher.encrypt(password.encode('utf-8'))

        try:
            db = self.client["passManager"]
            db.passwords.update_one({"user": user}, {"$set": {f"accounts.{website}": encryptedPass}})
        except Exception as e:
            print(e)
            return False

        return True


x = PassManager(client)


