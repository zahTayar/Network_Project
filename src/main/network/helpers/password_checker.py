from src.main.network.helpers.config import config
import re


class password_checker:
    def __init__(self):
        self.password_structure = []
        self.word_bank = []
        self.pull_from_config_file()

    def pull_from_config_file(self):
        self.password_count = config.password_count
        for item in config.password_structure.split(' '):
            self.password_structure.append(item)
        self.history = config.history
        for item in config.word_bank.split(' '):
            self.word_bank.append(item)
        self.login_tries = config.login_tries

    def check_password(self, password):
        if len(password) < self.password_count:
            raise Exception("password digits less than" + self.password_count)
        for item in self.password_structure:
            if not self.check_structure(item, password):
                raise Exception("missing requirments")
        for word in self.word_bank:
            if word == password:
                raise Exception("password in word bank")

    def check_structure(self, item, password):
        special_characters = "!@#$%^&*()-+?_=,<>/"
        if item == "Big":
            return any(ele.isupper() for ele in password)
        if item == "Small":
            return any(ele.islower() for ele in password)
        if item == "Digits":
            return any(ele.isdigit() for ele in password)
        if item == "Special":
            return any(c in special_characters for c in password)
        return False

