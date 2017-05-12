from mock import patch, ANY
import base64
import copy

from bot.crypt import encrypt
from bot.accounts import (LOGIN_DB,
                          load_db,
                          create_db,
                          erase_db,
                          update_with_user,
                          add_user,
                          get_user,
                          delete_user)

MOCK_LOGINS = {
    "ONETEAM": {
        "user1": {"username": "thundergolfer", "password": 'WPGEN/xy0flaCqe4QuiGVg==\n'},
        "user2": {"username": "another", "password": 'UDV62flhLW/kOXUzUv2zuQ==\n'}
    },
    "TWOTEAM": {
        "user3": {"username": "friend", "password": '7eoLolBe/2Le7jx1Jl8Ckw==\n'}
    }
}

@patch('bot.accounts.json.load', return_value={"this": "was loaded"})
def test_load_db(mock_load):
    assert load_db() == {"this": "was loaded"}
    mock_load.assert_called_once_with(ANY)


@patch('bot.accounts.create_db')
@patch('bot.accounts.json.load', side_effect=IOError)
def test_load_db_not_exists(mock_load, mock_create):
    assert load_db() == {}
    mock_create.assert_called_with()


@patch('bot.accounts.json.dump', return_value={"this": "was loaded"})
def test_create_db(mock_dump):
    create_db()
    mock_dump.assert_called_once_with({}, ANY)


@patch("builtins.open")
def test_erase_db(mock_open):
    erase_db()
    mock_open.assert_called_once_with(LOGIN_DB, 'w')


@patch('bot.accounts.json.dump')
@patch('bot.accounts.load_db', return_value=MOCK_LOGINS)
def test_update_with_user_new_user_new_team(mock_load_db, mock_json):
    update_with_user("NEWTEAM", "newuser", "NEWUSERNAME", "NEWPASSWORD")
    new_logins = copy.deepcopy(MOCK_LOGINS)
    new_logins["NEWTEAM"] = {"newuser": {"username": "NEWUSERNAME",
                                         "password": base64.encodestring(encrypt("NEWPASSWORD")).decode('utf-8')}}

    mock_json.assert_called_once_with(new_logins, ANY)


@patch('bot.accounts.json.dump')
@patch('bot.accounts.load_db', return_value=MOCK_LOGINS)
def test_update_with_user_new_user_existing_team(mock_load_db, mock_json):
    update_with_user("ONETEAM", "newuser", "NEWUSERNAME", "NEWPASSWORD")
    new_logins = copy.deepcopy(MOCK_LOGINS)
    new_logins["ONETEAM"]["newuser"] = {"username": "NEWUSERNAME",
                                        "password": base64.encodestring(encrypt("NEWPASSWORD")).decode('utf-8')}

    mock_json.assert_called_once_with(new_logins, ANY)


@patch('bot.accounts.json.dump')
@patch('bot.accounts.load_db', return_value=MOCK_LOGINS)
def test_update_with_user_existing_user_existing_team(mock_load_db, mock_json):
    update_with_user("ONETEAM", "user1", "NEWUSERNAME", "NEWPASSWORD")

    assert not mock_json.called


@patch('bot.accounts.load_db', return_value=MOCK_LOGINS)
def test_get_user_where_user_exists_in_team(mock_load_db):
    assert get_user("ONETEAM", "user1") == ("thundergolfer", "blah")


@patch('bot.accounts.load_db', return_value=MOCK_LOGINS)
def test_get_user_where_user_not_exists_in_team(mock_load_db):
    assert get_user("NOTATEAM", "user1") == (None, None)


@patch('bot.accounts.load_db', return_value=MOCK_LOGINS)
def test_get_user_where_user_not_exists(mock_load_db):
    assert get_user("NOTATEAM", "thisuserdoesntexistindb") == (None, None)


@patch('bot.accounts.json.dump')
@patch('bot.accounts.load_db', return_value=MOCK_LOGINS)
def test_delete_user(mock_load_db, mock_json):
    new_logins = copy.deepcopy(MOCK_LOGINS)
    team, user = "ONETEAM", "user1"
    del new_logins[team][user]
    delete_user(team, user)

    mock_json.assert_called_once_with(new_logins, ANY)
