import json
from flask import request

from flask import Blueprint, render_template, session, abort

app_file4 = Blueprint('app_file4', __name__)


@app_file4.route('/network/users/login/<user_email>/<user_pass>', methods=["GET"])
def login(user_email, user_pass) -> json:
    return {}  # succes/not


@app_file4.route('/network/users', methods=["POST"])
def register() -> json:
    return request.data  # succes/not


@app_file4.route('/network/users/<user_email>', methods=["PUT"])
def update_password(user_email) -> json:
    return request.data  # succes/not


@app_file4.route('/network/users/send_code/<user_email>', methods=["GET"])
def send_code_to_mail(user_email) -> json:
    return request.data  # code


@app_file4.route('/network/users/verify_code/<user_email>', methods=["POST"])
def verify_code_entered(user_email) -> json:
    return request.data  # yes/not


@app_file4.route('/network/clients', methods=["POST"])
def create_new_client() -> json:
    return request.data  # created user
