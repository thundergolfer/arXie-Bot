import json
import os
from bot.crypt import encrypt, decrypt

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

def update_with_user(team, slack_user, username, pw):
    logins = load_db()
    if team not in logins:
        logins[team] = {}
    if slack_user not in logins:
        logins[team][slack_user] = {}
        logins[team][slack_user]['username'] = encrypt(pw)
        logins[team][slack_user]['password'] = pw
        with open(LOGIN_DB, 'w') as fp:
            json.dump(logins, fp)


def add_user(team, slack_user, username, pw):
    logins = load_db()
    if team not in logins:
        logins[team] = {}
    logins[team][slack_user]['username'] = username
    logins[team][slack_user]['password'] = encrypt(pw)
    with open(LOGIN_DB, 'w') as fp:
        json.dump(logins, fp)

def get_user(team, slack_user):
    logins = load_db()
    if team in logins and slack_user in logins[team]:
        user = logins[team][slack_user]['username']
        pw = decrypt(logins[team][slack_user]['password'])
        return user, pw

    return None, None

def delete_user(slack_user):
    logins = load_db()
    del logins[slack_user]
    with open(LOGIN_DB, 'w') as fp:
        json.dump(logins, fp)
