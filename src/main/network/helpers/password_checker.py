import configparser


class password_checker:
    def __init__(self):
        self.password_structure = []
        self.word_bank = []
        self.pull_from_config_file()

    def pull_from_config_file(self):
        config = configparser.ConfigParser()
        password_requirments = config.read('configurations.ini')['password']
        self.password_count = password_requirments['password_count']
        for item in password_requirments['password_count'].split(' '):
            self.password_structure.append(item)
        self.history = password_requirments['history']
        for item in password_requirments['word_bank'].split(' '):
            self.word_bank.append(item)
        self.login_tries = password_requirments['login_tries']

    def check_password(self):
        pass
