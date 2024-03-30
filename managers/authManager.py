import bcrypt
from pymongo.mongo_client import MongoClient
from dbClient import oauth_key
from managers.oauth import OAuth
import re

class AuthManager:

    def __init__(self, client: MongoClient):
        """
        Initializes an AuthManager object with the provided MongoDB Client

        Parameters:
            client (MongoClient): A MongoDB client object used for storing and retrieving password data.
        """
        self.client = client

    def hash_password(self, password: str) -> bytes:
        """
        Creates a secure hash for the provided password

        Parameters:
            password (str): A password which will be used to login

        Returns:
            bytes: The hash is stored as a bytes object
        """
        encoded = password.encode('utf-8')
        hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
        return hashed
    
    def check_password(self, password: str, hash: bytes) -> bool:
        """
        Checks the password against the hash to see if it matches

        Parameters:
            password (str): A user inputted value which is meant to be their password
            hash (bytes): A hash which can be used to verify the validity of the password

        Returns:
            bool: Represents whether the password matched the hash
        """
        encoded = password.encode('utf-8')
        return bcrypt.checkpw(encoded, hash)
    
    def add_user(self, email: str, password: str) -> tuple[bool, str]:
        """
        Creates a new user and adds an entry for them in the database

        Parameters:
            email (str): An email which will be used for logging in
            password (str): The user's desired password

        Returns:
            tuple[bool, str]: Returns a boolean indicating whether the database operation was successful
                                or not and a string with more detailed information
        """
        o_auth = OAuth(self.client, oauth_key)
        hashed_pass = self.hash_password(password)
        operation = {"user" : email, "password" : hashed_pass, "OAuth_key" : o_auth.create_otp_key(), "accounts" : {}}

        pattern = "^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$"
        valid = re.match(pattern, email) # input validaiton on the email

        if not valid:
            return False, "Email is invalid or contains mistakes"

        try:
            db = self.client["passManager"]
            password_collection = db["passwords"]

            if password_collection.find_one({"user" : email}) != None: # Check if this user already exists
                return False, "User already exists"
            
            password_collection.insert_one(operation)

        except Exception as e:
            return False, "User registration failed: " + str(e)
        
        return True, "Use successfully created"
    
    def login(self, email: str, password: str) -> tuple[bool, str]:
        """
        Attempts to log a user in
        Compares the provided password to the hash stores in the database

        Parameters:
            email (str): The user's email
            password (str): The user's password, will be matched against a hash

        Returns:
            tuple[bool, str]: A boolean determining whether the user was succesfully able to log in
                                and a string with more detailed information
        """
        try:
            db = self.client["passManager"]
            hashed_pass = db.passwords.find_one({"user" : email}, {"password" : 1, "_id" : 0})

            if hashed_pass == None: # Trips when the user doesn't exist
                return False, "User doesn't exist"
            
            valid = self.check_password(password, hashed_pass["password"])

            if not valid:
                return False, "Login failed: The password was incorrect"
            
            return True, "Login Successful"
        
        except Exception as e:
            return False, "Login failed: " + str(e)
    
    def reset_password(self, email: str, password: str) -> tuple[bool, str]:
        """
        Resets a user's password 

        Parameters:
            email (str): The user's email
            password (str): THe user's new desired password

        Returns:
            tuple[bool, str]: Returns True if the database update was succesful and False otherwise
                                A string containing more detailed information is also provided
        """
        hashed_password = self.hash_password(password)
        operation = {"$set": {"password": hashed_password}}

        try:
            db = self.client["passManager"]
            password_collection = db["passwords"]
            
            if password_collection.find_one({"user" : email}) == None: # Check if this user doesn't exist
                return False, "User doesn't exist"
            
            password_collection.update_one({"user" : email}, operation)
            
            return True, "Password was succesfully reset"

        except Exception as e:
            return False, "Unsuccesful operation: " + str(e)