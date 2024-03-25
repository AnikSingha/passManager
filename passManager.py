from dbClient import key
from cryptography.fernet import Fernet

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
    
    def addPassword(self, user, website, password):
        encryptedPass = self.cipher.encrypt(password.encode('utf-8'))
        operation = {"$set": {f"accounts.{website}": encryptedPass}}

        try:
            db = self.client["passManager"]
            db.passwords.update_one({"user": user}, operation)

        except Exception as e:
            print(e)
            return False

        return True
    
    def getPasswords(self, userName):
        try:
            db = self.client["passManager"]
            user = db.passwords.find_one({"user" : userName})

        except Exception as e:
            print(e)
            return False

        return self.decodePasswords(user["accounts"])


    def updatePassword(self, user, website, password):
        try:
            self.addPassword(user, website, password)

        except Exception as e:
            print(e)
            return False

        return True
    
    def deletePassword(self, user, website):
        operation = {"$unset" : {f"accounts.{website}" : ""}}

        try:
            db = self.client["passManager"]
            db.passwords.update_one({"user" : user}, operation)
        
        except Exception as e:
            print(e)
            return False
        
        return True