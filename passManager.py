from cryptography.fernet import Fernet
from pymongo.mongo_client import MongoClient
from typing import Union

class PassManager:

    def __init__(self, client: MongoClient, key: bytes):
        """
        Initializes a PassManager object with the provided MongoDB client.

        Parameters:
            client (MongoClient): A MongoDB client object used for storing and retrieving password data.
            key (bytes): The encryption key used for encrypting the data. It should be a 32-byte Fernet key
                         generated using Fernet.generate_key().
        """
        self.client = client
        self.key = key
        self.cipher = Fernet(self.key) # used for encryption and decryption
    
    def decode_passwords(self, passwords: str) -> dict:
        """
        Decrypts the encrypted passwords stored in the given dictionary.

        Parameters:
            passwords (dict): A dictionary where the keys represent website names and the values are encrypted passwords.

        Returns:
            dict: An updated passwords dictionary where the values are now decrypted.
        """
        decPasswords = {}

        for key, val in passwords.items():
            decrypted = self.cipher.decrypt(val).decode() # the decrypted password 
            decPasswords[key.replace('|', '.')] = decrypted
        
        return decPasswords
    
    def add_password(self, user: str, website: str, password: str) -> bool:
        """
        Encrypts a password and then stores it in the MongoDB passwords collection.

        Parameters:
            user (str): The username of the user.
            website (str): The name of the website.
            password (str): The unencrypted password we will encrypt and place into the database.

        Returns:
            bool: A boolean representing whether the function succeeded or failed in updating the database.

        Notes:
            If there is an existing entry for the website then the password is updated
        """
        encrypted_pass = self.cipher.encrypt(password.encode('utf-8'))
        website = website.replace('.', '|')
        operation = {"$set": {f"accounts.{website}": encrypted_pass}}

        try:
            db = self.client["passManager"]

            if db.passwords.find_one({"user" : user}) == None: # Check if user exists
                return False
            
            db.passwords.update_one({"user": user}, operation)

        except Exception as e:
            print(e)
            return False

        return True
    
    def get_passwords(self, userName: str) -> Union[dict, None]:
        """
        Returns a dictionary containing decrypted passwords for a specific user.

        Parameters:
            userName (str): The username of the user whose passwords we want to retrieve.

        Returns:
            Union[dict, None]: A dictionary where the keys are the names of websites and the values are the decrypted passwords,
            or None if there was an error retrieving the passwords.
        """
        try:
            db = self.client["passManager"]
            user = db.passwords.find_one({"user" : userName})

            if user == None:
                return False

        except Exception as e:
            print(e)
            return False

        return self.decode_passwords(user["accounts"]) # decodes the passwords before returning them


    def update_password(self, user: str, website: str, password: str) -> bool:
        """
        Updates the password for an existing website in the database

        Parameters:
            user (str): The username of the user.
            website (str): The name of the website.
            password (str): The unencrypted password we will encrypt and place into the database.

        Returns:
            bool: A boolean representing whether the function succeeded or failed in updating the database.
        """
        encrypted_pass = self.cipher.encrypt(password.encode('utf-8'))
        website = website.replace('.', '|')
        operation = {"$set": {f"accounts.{website}": encrypted_pass}}

        try:
            db = self.client["passManager"]

            if db.passwords.find_one({"user" : user}) == None: # Check if user exists
                return False
            
            db.passwords.update_one({"user": user}, operation)


        except Exception as e:
            print(e)
            return False

        return True
    
    def delete_password(self, user: str, website: str) -> bool:
        """
        Deletes the credentials for a specific website from the database

        Parameters:
            user (str): The username of the user.
            website (str): The name of the website.

        Returns:
            bool: A boolean representing whether the function succeeded or failed in updating the database.
        """
        website = website.replace('.', '|')
        operation = {"$unset" : {f"accounts.{website}" : ""}}

        try:
            db = self.client["passManager"]

            if db.passwords.find_one({"user" : user}) == None: # Check if user exists
                return False
            
            db.passwords.update_one({"user" : user}, operation)
        
        except Exception as e:
            print(e)
            return False
        
        return True