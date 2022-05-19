from flask import Flask
from flask_mysqldb import MySQL
import json
from flask import request

app = Flask(__name__)

# MYSQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'network_project'

mysql = MySQL(app)

class user_service():
    def __init__(self):
        self.cursor = mysql.connection.cursor()
    def get_cursor(self):
        return self.cursor

@app.route('/network/users/login/<user_email>/<user_pass>', methods=["GET"])
def login(user_email, user_pass) -> json:

    return {}  # succes/not

@app.route('/network/users', methods=["POST"])
def register() -> json:
    service = user_service()
    service.get_cursor().execute('''select *  from users where email LIKE "zahtayil.com" ;''')
    dic =service.get_cursor().fetchall()
    service.get_cursor().execute('''Insert into users(email,password) values("zahtayil.com","zahtayar123");''')
    mysql.connection.commit()
    return request.data  # succes/not

@app.route('/network/users/<user_email>', methods=["PUT"])
def update_password(user_email) -> json:
    return request.data  # succes/not


@app.route('/network/users/send_code/<user_email>', methods=["GET"])
def send_code_to_mail(user_email) -> json:
    return request.data  # code


@app.route('/network/users/verify_code/<user_email>', methods=["POST"])
def verify_code_entered(user_email) -> json:
    return request.data  # yes/not


@app.route('/network/clients', methods=["POST"])
def create_new_client() -> json:
    return request.data  # created user

if __name__ == '__main__':
    app.run(port=5500)
