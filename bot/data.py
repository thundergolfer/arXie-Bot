import json
import os

LOGIN_DB_FILENAME = "logins.json"
LOGIN_DB = os.path.join(os.path.dirname(__file__), LOGIN_DB_FILENAME)

def load_db():
    logins = {}
    try:
        with open(LOGIN_DB, 'r') as fp:
            logins = json.load(fp)
    except IOError:
        create_db()

    return logins

def create_db():
    with open(LOGIN_DB, 'w') as fp:
        json.dump({}, fp)

def erase_db():
    with open(LOGIN_DB, 'w'): pass

def update_with_user(slack_user, username, pw):
    logins = load_db()
    if slack_user not in logins:
        logins[slack_user]['username'] = username
        logins[slack_user]['password'] = pw
        with open(LOGIN_DB, 'w') as fp:
            json.dump(logins, fp)


def add_user(slack_user, username, pw):
    logins = load_db()
    logins[slack_user]['username'] = username
    logins[slack_user]['password'] = pw
    with open(LOGIN_DB, 'w') as fp:
        json.dump(logins, fp)

def get_user(slack_user):
    logins = load_db()
    if slack_user in logins:
        user = logins[slack_user]['username']
        pw = logins[slack_user]['password']
        return user, pw

    return None, None

def delete_user(slack_user):
    logins = load_db()
    del logins[slack_user]
    with open(LOGIN_DB, 'w') as fp:
        json.dump(logins, fp)
