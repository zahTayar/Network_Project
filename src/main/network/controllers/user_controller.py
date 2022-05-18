import json
from flask import request

from flask import Blueprint, render_template, session, abort

app_file4 = Blueprint('app_file4', __name__)


@app_file4.route('/network/users/login/<user_email>', methods=["GET"])
def get_user_details(user_email) -> json:
    return {}


@app_file4.route('/network/users', methods=["POST"])
def create_new_user() -> json:
    return request.data


@app_file4.route('/network/users/<user_email>', methods=["PUT"])
def update_user_details() -> json:
    return request.data


#request to get yes or no user exist

#send code to email

#verify code entered against code send

#post customer with table of customers

#put request +verify old password