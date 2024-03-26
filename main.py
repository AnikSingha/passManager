from dbClient import client, key   
from passManager import PassManager
from authManager import AuthManager

x = PassManager(client, key)
y = AuthManager(client)

print(x.add_password('dont', 'ani', '1'))