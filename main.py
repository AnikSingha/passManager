from dbClient import client, key   
from passManager import PassManager
from authManager import AuthManager

x = PassManager(client, key)
y = AuthManager(client)


print(y.login("anik@gmail.com", "anik1"))
#print(y.reset_password("anik@gmail.com", "anik1"))