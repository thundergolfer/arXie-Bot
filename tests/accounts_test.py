from mock import patch, ANY
import base64
import copy
import pytest

from bot.crypt import encrypt
from bot.accounts import LocalAccountManager

MOCK_LOGINS = {
    "ONETEAM": {
        "user1": {"username": "thundergolfer", "password": 'WPGEN/xy0flaCqe4QuiGVg==\n'},
        "user2": {"username": "another", "password": 'UDV62flhLW/kOXUzUv2zuQ==\n'}
    },
    "TWOTEAM": {
        "user3": {"username": "friend", "password": '7eoLolBe/2Le7jx1Jl8Ckw==\n'}
    }
}

account_manager = LocalAccountManager()


@pytest.yield_fixture
def refresh():
    account_manager.create_db()
    yield
    account_manager.create_db()


@patch('bot.accounts.json.load', return_value={"this": "was loaded"})
def test_load_db(mock_load, refresh):
    assert account_manager.load_db() == {"this": "was loaded"}
    mock_load.assert_called_once_with(ANY)


@patch.object(LocalAccountManager, 'create_db')
@patch('bot.accounts.json.load', side_effect=IOError)
def test_load_db_not_exists(mock_load, mock_create):
    assert account_manager.load_db() == {}
    mock_create.assert_called_with()


@patch('bot.accounts.json.dump', return_value={"this": "was loaded"})
def test_create_db(mock_dump):
    account_manager.create_db()
    mock_dump.assert_called_once_with({}, ANY)


@patch('bot.accounts.json.dump')
@patch.object(LocalAccountManager, 'load_db', lambda self: MOCK_LOGINS)
def test_update_with_user_new_user_new_team(mock_json):
    account_manager.update_with_user("NEWTEAM", "newuser", "NEWUSERNAME", "NEWPASSWORD")
    new_logins = copy.deepcopy(MOCK_LOGINS)
    new_logins["NEWTEAM"] = {
        "newuser": {
            "username": "NEWUSERNAME",
            "password": base64.encodestring(encrypt("NEWPASSWORD")).decode('utf-8')
        }
    }

    mock_json.assert_called_once_with(new_logins, ANY)


@patch('bot.accounts.json.dump')
@patch.object(LocalAccountManager, 'load_db', lambda self: MOCK_LOGINS)
def test_update_with_user_new_user_existing_team(mock_json):
    account_manager.update_with_user("ONETEAM", "newuser", "NEWUSERNAME", "NEWPASSWORD")
    new_logins = copy.deepcopy(MOCK_LOGINS)
    new_logins["ONETEAM"]["newuser"] = {
        "username": "NEWUSERNAME",
        "password": base64.encodestring(encrypt("NEWPASSWORD")).decode('utf-8')
    }

    mock_json.assert_called_once_with(new_logins, ANY)


@patch('bot.accounts.json.dump')
@patch.object(LocalAccountManager, 'load_db', lambda self: MOCK_LOGINS)
def test_update_with_user_existing_user_existing_team(mock_json):
    account_manager.update_with_user("ONETEAM", "user1", "NEWUSERNAME", "NEWPASSWORD")

    assert not mock_json.called


@patch.object(LocalAccountManager, 'load_db', lambda self: MOCK_LOGINS)
def test_get_user_where_user_exists_in_team():
    assert account_manager.get_user("ONETEAM", "user1") == ("thundergolfer", "blah")


@patch.object(LocalAccountManager, 'load_db', lambda self: MOCK_LOGINS)
def test_get_user_where_user_not_exists_in_team():
    assert account_manager.get_user("NOTATEAM", "user1") == (None, None)


@patch.object(LocalAccountManager, 'load_db', lambda self: MOCK_LOGINS)
def test_get_user_where_user_not_exists():
    assert account_manager.get_user("NOTATEAM", "thisuserdoesntexistindb") == (None, None)


@patch('bot.accounts.json.dump')
@patch.object(LocalAccountManager, 'load_db', lambda self: MOCK_LOGINS)
def test_delete_user(mock_json):
    new_logins = copy.deepcopy(MOCK_LOGINS)
    team, user = "ONETEAM", "user1"
    del new_logins[team][user]
    account_manager.delete_user(team, user)

    mock_json.assert_called_once_with(new_logins, ANY)
