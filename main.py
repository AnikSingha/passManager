from dbClient import client, key   
from passManager import PassManager
from authManager import AuthManager

x = PassManager(client, key)
y = AuthManager(client)

#y.add_user("anik@gmail.com", "Anik")

print(y.login("anik@gmail.com", "Anik"))