import json
import os

LOGIN_DB_FILENAME = "logins.json"
LOGIN_DB = os.path.join(os.path.dirname(__file__), LOGIN_DB_FILENAME)

def load_db():
    with open(LOGIN_DB, 'r') as fp:
        logins = json.load(fp)

    return logins

def create_db():
    raise NotImplementedError

def erase_db():
    raise NotImplementedError

def add_user(user, pw):
    raise NotImplementedError

def get_user(slack_user):
    logins = load_db()
    if slack_user in logins:
        user = logins[slack_user]['username']
        pw = logins[slack_user]['password']
        return user, pw

    return None, None

def delete_user(slack_user):
    raise NotImplementedError
