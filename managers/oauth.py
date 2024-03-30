import pyotp 
import qrcode
from pymongo.mongo_client import MongoClient
from cryptography.fernet import Fernet
from io import BytesIO
from typing import Union

class OAuth:

    def __init__(self, client: MongoClient, key: bytes):
        """
        Initializes a OAuth object with the provided MongoDB client and encryption key

        Parameters:
            client (MongoClient): A MongoDB client object used for storing and retrieving password data.
            key (bytes): The encryption key used to encrypt the OAuth key used for OTP generation
        """
        self.cipher = Fernet(key)
        self.client = client

    def create_otp_key(self) -> bytes:
        """
        Generates and encrypts a key which will be used to generate one time codes
        """
        OTP_key = pyotp.random_base32()
        encrypyed = self.cipher.encrypt(OTP_key.encode('utf-8'))
        return encrypyed
    
    def upload_key(self, user: str) -> bool:
        """
        Generates and assigns a user a OTP key before uploading it to MongoDB

        Parameters:
            user (str): The username/email of the user

        Returns 
            bool: A boolean representing whether the database operation was succesful
        """
        otp_key = self.create_otp_key()
        operation = {"$set": {"OAuth_key": otp_key}}

        try:
            db = self.client["passManager"]

            if db.passwords.find_one({"user" : user}) == None: # Check if user exists
                return False
            
            db.passwords.update_one({"user": user}, operation)

        except Exception as e:
            print(e)
            return False
        
        return True
    
    def get_key(self, user: str) -> Union[str, bool]:
        """
        Retrieves and decryptes the OTP key

        parameters:
            user (str): The username/email of the user

        Returns:
            Union[str, bool]: The decrypted OTP key will be returned if the database fetch
                                was successful, otherwise False will be returned
        """
        try:
            db = self.client["passManager"]
            user = db.passwords.find_one({"user" : user})

            if not user:
                return False
            
            otp_key = self.cipher.decrypt(user["OAuth_key"])
            
            return otp_key.decode()
        
        except Exception as e:
            print(e)
            return False
    
    def verify_code(self, user: str, code: str) -> tuple[bool, str]:
        """
        Used to check if the user inputted code matches the 
        OTP generated by pyotp

        Parameters:
            user (str): The username/email of the user
            code (str): The user inputted code

        Returns:
            tuple[bool, str]: A boolean representing whether the user input code matches
                    the value of the OTP and a string with more detailed info 
        """
        try:
            otp_key = self.get_key(user)

            if not otp_key: 
                return False, "User does not exist"
            
            totp = pyotp.TOTP(otp_key)
            valid = totp.verify(code)

            if not valid:
                return False, "The code was incorrect"
            
            return True, "The code was correct"
        
        except Exception as e:
            return False, "Error: " + str(e)
        
    def gen_qrcode(self, user: str) -> tuple[bool, Union[BytesIO, str]]:
        """
        Generates a qr code which can be used by an authenticator app to
        display the generated OTP code

        Parameters:
            user (str): The username/email of the user

        Returns:
            tuple[bool, Union[BytesIO, str]]: A boolean representing whether the function succeeded is returned.
                                                The qr code is turned into a BytesIO so it can be sent over the web
                                                If the operation was unsuccesful then a string will be sent
        """
        try:
            key = self.get_key(user)

            uri = pyotp.totp.TOTP(key).provisioning_uri( 
                name=user, 
                issuer_name='PassManager') 
            
            qr_image = qrcode.make(uri)
            qr_bytes = BytesIO()
            qr_image.save(qr_bytes)
            qr_bytes.seek(0)

            return True, qr_bytes
        
        except Exception as e:
            return False, "Unable to generate qr code: " + str(e)
