from cryptography.fernet import Fernet
from pymongo.mongo_client import MongoClient
from typing import Union

class PassManager:

    def __init__(self, client: MongoClient, key: bytes):
        """
        Initializes a PassManager object with the provided MongoDB client and encryption key.

        Parameters:
            client (MongoClient): A MongoDB client object used for storing and retrieving password data.
            key (bytes): The encryption key used for encrypting the data. It should be a 32-byte Fernet key
                            generated using Fernet.generate_key().
        """
        self.client = client
        self.cipher = Fernet(key) # used for encryption and decryption
    
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
    
    def add_password(self, user: str, website: str, password: str) -> tuple[bool, str]:
        """
        Encrypts a password and then stores it in the MongoDB passwords collection.

        Parameters:
            user (str): The username of the user.
            website (str): The name of the website.
            password (str): The unencrypted password we will encrypt and place into the database.

        Returns:
            tuple[bool, str] : A boolean representing whether the function succeeded or failed in updating the database
                                and a string with a detailed message
        """
        encrypted_pass = self.cipher.encrypt(password.encode('utf-8'))
        website = website.replace('.', '|')
        operation = {"$set": {f"accounts.{website}": encrypted_pass}}

        try:
            db = self.client["passManager"]

            if db.passwords.find_one({"user" : user}) == None: # Check if user exists
                return False, "User doesn't exist"
            
            db.passwords.update_one({"user": user}, operation)

        except Exception as e:
            return False, "Failed: " + str(e)

        return True, "Account successfully added"
    
    def get_passwords(self, userName: str) -> tuple[bool, Union[dict, str]]:
        """
        Returns a dictionary containing decrypted passwords for a specific user.

        Parameters:
            userName (str): The username of the user whose passwords we want to retrieve.

        Returns:
            tuple[bool, Union[str, dict]] : The first item returned is a boolean representing whether the 
                database operation succeeded or not. If it succeeded then a dictionary with all the account
                credentials will be returned, otherwise a string detailing what went werong will be returned.
        """
        try:
            db = self.client["passManager"]
            user = db.passwords.find_one({"user" : userName})

            if user == None:
                return False, "User doesn't exist"

        except Exception as e:
            return False, "Unsuccesful: " + str(e)

        return True, self.decode_passwords(user["accounts"]) # decodes the passwords before returning them


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