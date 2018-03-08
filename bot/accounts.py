import json
import os
import base64
from bot.crypt import encrypt, decrypt

from google.cloud import datastore

LOGIN_DB_FILENAME = "logins.json"
LOGIN_DB = os.path.join(os.path.dirname(__file__), LOGIN_DB_FILENAME)


def newAccountManager(dev_env):
    return LocalAccountManager() if dev_env else CloudDatastoreAccountManager()


class CloudDatastoreAccountManager():
    def __init__(self):
        self.project_id = os.environ['PROJECT_ID']

    def update_with_user(self, team, slack_user, username, pw):
        client = datastore.Client(self.project_id, namespace=team)

        complete_key = client.key('Login', slack_user)

        task = datastore.Entity(key=complete_key)

        task.update({
            'username': username,
            'password': pw,
        })

        client.put(task)

    def get_user(self, team, slack_user):
        client = datastore.Client(self.project_id, namespace=team)
        key = client.key('Login', slack_user)
        user_details = client.get(key)

        return user_details['username'], user_details['password']


class LocalAccountManager():
    def load_db(self):
        logins = {}
        try:
            with open(LOGIN_DB, 'r') as fp:
                logins = json.load(fp)
        except (IOError, ValueError):
            create_db()

        return logins

    def create_db(self):
        with open(LOGIN_DB, 'w') as fp:
            json.dump({}, fp)

    def erase_db(self):
        create_db()

    def update_with_user(self, team, slack_user, username, pw):
        logins = load_db()
        if team not in logins:
            logins[team] = {}
        if slack_user not in logins[team]:
            logins[team][slack_user] = {}
            logins[team][slack_user]['username'] = username
            pw = base64.encodestring(encrypt(pw)).decode('utf-8')
            logins[team][slack_user]['password'] = pw
            with open(LOGIN_DB, 'w') as fp:
                json.dump(logins, fp)

    def add_user(self, team, slack_user, username, pw):
        logins = load_db()
        if team not in logins:
            logins[team] = {}
        logins[team][slack_user]['username'] = username
        logins[team][slack_user]['password'] = base64.encodestring(encrypt(pw))
        with open(LOGIN_DB, 'w') as fp:
            json.dump(logins, fp)

    def get_user(self, team, slack_user):
        logins = load_db()
        if team in logins and slack_user in logins[team]:
            user = logins[team][slack_user]['username']
            encrypted_pw = logins[team][slack_user]['password'].encode('utf-8')
            pw = decrypt(base64.decodestring(encrypted_pw))

            return user, pw

        return None, None

    def delete_user(self, team, slack_user):
        logins = load_db()
        del logins[team][slack_user]
        with open(LOGIN_DB, 'w') as fp:
            json.dump(logins, fp)
