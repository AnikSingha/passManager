import time 
import pyotp 
import qrcode
from pymongo.mongo_client import MongoClient
from cryptography.fernet import Fernet
from dbClient import key

class OAuth:

    def __init__(self, user: str, password: str, key: bytes, client: MongoClient):
        self.user = user
        self.password = password
        self.cipher = Fernet(key)
        self.client = client

    def create_otp_key(self) -> bytes:
        OTP_key = pyotp.random_base32()
        encrypyed = self.cipher.encrypt(OTP_key.encode('utf-8'))
        return encrypyed