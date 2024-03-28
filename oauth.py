import pyotp 
import qrcode
from pymongo.mongo_client import MongoClient
from cryptography.fernet import Fernet
from io import BytesIO
from flask import Response
from typing import Union

class OAuth:

    def __init__(self, key: bytes, client: MongoClient):
        self.cipher = Fernet(key)
        self.client = client

    def create_otp_key(self) -> bytes:
        OTP_key = pyotp.random_base32()
        encrypyed = self.cipher.encrypt(OTP_key.encode('utf-8'))
        return encrypyed
    
    def upload_key(self, user: str) -> bytes:
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
    
    def verify_code(self, user: str, code: str) -> bool:

        try:
            otp_key = self.get_key(user)

            if not otp_key: 
                return False
            
            totp = pyotp.TOTP(otp_key)

            return totp.verify(code)
        
        except Exception as e:
            print(e)
            return False
        
    def gen_qrcode(self, user: str):
        try:
            key = self.get_key(user)

            uri = pyotp.totp.TOTP(key).provisioning_uri( 
                name=user, 
                issuer_name='PassManager') 
            
            qr_image = qrcode.make(uri)
            qr_bytes = BytesIO()
            qr_image.save(qr_bytes)
            qr_bytes.seek(0)

            return qr_bytes
        
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None


    # Create function that verifies OTP Code

