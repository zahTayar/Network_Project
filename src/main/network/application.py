import smtplib
import random
from flask import Flask
from flask_mysqldb import MySQL
import json
from flask import request

from src.main.network.helpers.config import config
from src.main.network.helpers.password_checker import password_checker

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

    def check_last_three(self, password_str,password_from_db):
        lis = password_from_db.split('|')
        counter = 0
        for i in reversed(lis):
            if i == password_str :
                return False
            counter+=1
            if counter == 3:
                return True
        return True


    def send_email_with_update(self,email):
        email_address = 'fma.finalproject2022@yahoo.com'
        subject = 'Subject: Code for verify you own this account!\n\n'
        passcode = 'zkykgdjwieuikyrf'
        random_code = random.randint(1000,9999)
        content = 'Hello, \nThe code for change the password is \n\n.' + str(random_code)
        footer = "Thank you."
        global conn
        try:
            conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
            conn.ehlo()
            conn.login(email_address, passcode)
        except smtplib.SMTPException as e:
            Exception(e)
        if email is None:
            Exception("There are no users in the system")
            return

        try:
            conn.sendmail(email_address,
                              email,
                              subject + content + footer)
        except smtplib.SMTPException as e:
                Exception(e)
                conn.quit()
        conn.quit()
        return str(random_code)

@app.route('/network/users/login/<user_email>/<user_pass>', methods=["GET"])
def login(user_email, user_pass) -> json:
    service = user_service()
    service.get_cursor().execute('''select email,password from users where email LIKE '%s' LIMIT 1;''' % user_email)
    result = service.get_cursor().fetchone()
    if len(result) == 0:
        return {"status":"200ok","result":False}
    if result[1] != user_pass:
        config.login_tries-=1
        if config.login_tries == 0:
            raise Exception("You have tried more then three times to login.")
        raise Exception("Wrong password entered.")
    config.login_tries = 3
    return {"status":"200ok","result":True,"message":"login succussfuly"}  # succes/not

@app.route('/network/users', methods=["POST"])
def register() -> json:
    service = user_service()
    service.get_cursor().execute('''select email,password from users where email LIKE '%s' LIMIT 1;''' % request.get_json()["email"])
    dic = service.get_cursor().fetchall()
    if len(dic) > 0:
        raise Exception("User already exist, please try again :)")
    helper = password_checker()
    helper.check_password(request.get_json()["password"])
    service.get_cursor().execute('''Insert into passwords(email,password_str) values('%s','%s');''' % (request.get_json()["email"] , str(request.get_json()["password"])))
    service.get_cursor().execute('''Insert into users(email,password) values('%s','%s');''' % (request.get_json()["email"] , request.get_json()["password"]))
    mysql.connection.commit()
    return {"status":"200ok","result":True ,"message":"user created successfully"}  # succes/not

@app.route('/network/users/<user_email>', methods=["PUT"])
def update_password(user_email) -> json:
    service = user_service()
    service.get_cursor().execute('''select email,password from users where email LIKE '%s' LIMIT 1;''' % user_email)
    result = service.get_cursor().fetchone()
    if len(result) > 0:
        helper = password_checker()
        helper.check_password(request.get_json()["password"])
        service.get_cursor().execute('''select password_str from passwords where email LIKE '%s' ''' % user_email)
        result_password = service.get_cursor().fetchone()
        result_password = ','.join(result_password)
        if not service.check_last_three(str(request.get_json()["password"]),result_password):
            raise Exception("You cant use password that you have used in the last three updates")
        result_str = str(result_password)
        result_str += "|" + request.get_json()["password"]
        service.get_cursor().execute('''UPDATE USERS 
                                        SET password=%s 
                                        WHERE email LIKE %s
                                        ''' , (request.get_json()["password"],user_email))
        service.get_cursor().execute('''UPDATE passwords.
                                        SET (password_str=%s) 
                                        WHERE (email LIKE %s) ''' , (result_str, user_email))
        mysql.connection.commit()
    else:
        raise Exception("user not exist")
    return {"status":"200ok","result":True ,"message":"password updated successfully"}  # succes/not


@app.route('/network/users/send_code/<user_email>', methods=["GET"])
def send_code_to_mail(user_email) -> json:
    service = user_service()
    if service.get_cursor().execute('''select email from users where email LIKE '%s' LIMIT 1;''' % user_email) ==0:
        raise  Exception("User not exist in our systems.")
    code = service.send_email_with_update(user_email)
    if service.get_cursor().execute('''select email from codes where email LIKE '%s' ''' % user_email) == 0 :
        service.get_cursor().execute('''Insert into codes(email,code) values('%s', '%s')'''%(user_email,code))
    else:
        service.get_cursor().execute('''UPDATE CODES SET code = '%s' ''' % code)
    mysql.connection.commit()
    return  {"status":"200ok","result":True ,"message":"code sent via email."} # code


@app.route('/network/users/verify_code/<user_email>', methods=["POST"])
def verify_code_entered(user_email) -> json:
    service = user_service()
    service.get_cursor().execute('''select code from codes where email LIKE '%s' ''' % user_email)
    code_from_db = service.get_cursor().fetchone()

    if not code_from_db[0] == request.get_json()['code']:
        raise Exception('Code not fit. \n Please try again.')
    return {"status":"200ok","result":True ,"message":"code entered succussfully"}  # yes/not


@app.route('/network/clients', methods=["POST"])
def create_new_client() -> json:
    service =user_service()
    service.get_cursor().execute('''Insert into customers(f_name,l_name) values('%s','%s');''' % (request.get_json()["f_name"] , request.get_json()["l_name"]))
    mysql.connection.commit()
    return {"status":"200ok","result":True ,"message":"customer created succussfully"} # created user

if __name__ == '__main__':
    app.run(port=5500)
