import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("password")
# ADD SETTINGS TO SECTION
config_file.set("password", "password_count", "10")
config_file.set("password", "password_structure", "Big Small Digits Special")
config_file.set("password", "history", "3")
config_file.set("password", "word_bank", "admin ronaldo")
config_file.set("password", "login_tries", "3")

with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()