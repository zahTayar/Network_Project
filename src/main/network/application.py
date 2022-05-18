from flask import Flask
from flask_mysqldb import MySQL
import json
from flask import request
from src.main.network.controllers.admin_controller import app_file1
from src.main.network.controllers.item_controller import app_file2
from src.main.network.controllers.operation_controller import app_file3
# from src.main.network.controllers.user_controller import app_file4

app = Flask(__name__)

# MYSQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'network_project'

mysql = MySQL(app)

app.register_blueprint(app_file1)
app.register_blueprint(app_file2)
app.register_blueprint(app_file3)
# app.register_blueprint(app_file4)

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
    service.get_cursor().execute('''Insert into users(email,password) values("zahtayar1993@gmail.com","zahtayar123");''')
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
