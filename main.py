from dbClient import client, key   
from passManager import PassManager
from authManager import AuthManager

x = PassManager(client, key)
a = AuthManager(client)
