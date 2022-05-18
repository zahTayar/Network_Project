from src.main.network.application import mysql

class user_service:
    def __init__(self):
       cursor = mysql.connection.cursor()
       cursor.execute('''CREATE TABLE USERS(email,password)''')
       cursor.execute('''CREATE TABLE COUSTOMERS(email,password)''')

    def create_user(self, email, password):
        pass