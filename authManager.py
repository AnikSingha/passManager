from pymongo.mongo_client import MongoClient
import bcrypt

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
    
    def add_user(self, email: str, password: str) -> bool:
        """
        Creates a new user and adds an entry for them in the database

        Parameters:
            email (str): An email which will be used for logging in
            password (str): The user's desired password

        Returns:
            bool: Returns True if the user was succesfully added to the database and False otherwise
        """
        hashed_pass = self.hash_password(password)
        operation = {"user" : email, "password" : hashed_pass, "accounts" : {}}

        try:
            db = self.client["passManager"]
            password_collection = db["passwords"]

            if password_collection.find_one({"user" : email}) != None: # Check if this user already exists
                return False
            
            password_collection.insert_one(operation)

        except Exception as e:
            print(e)
            return False
        
        return True    
    
    def login(self, email: str, password: str) -> bool:
        """
        Determines whether we should allow a user to login

        Parameters:
            email (str): The user's email
            password (str): The user's password, will be matched against a hash

        Returns:
            bool: A boolean determining whether the user was allowed to login
        """
        try:
            db = self.client["passManager"]
            hash = db.passwords.find_one({"user" : email}, {"password" : 1, "_id" : 0})

            if hash == None: # Trips when the user doesn't exist
                return False
            
            return self.check_password(password, hash["password"])
        
        except Exception as e:
            print(e)
            return False
        
    def reset_password(self, email: str, password: str) -> bool:
        """
        Resets a user's password 

        Parameters:
            email (str): The user's email
            password (str): THe user's new desired password

        Returns:
            bool: Returns True if the database update was succesful and False otherwise
        """
        hashed_password = self.hash_password(password)

        try:
            db = self.client["passManager"]
            password_collection = db["passwords"]
            
            if password_collection.find_one({"user" : email}) == None: # Check if this user doesn't exist
                return False
            
            password_collection.update_one({"user" : email}, {"$set": {"password": hashed_password}})
            
            return True

        except Exception as e:
            print(e)
            return False