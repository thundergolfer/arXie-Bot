import pytest

from bot.crypt import encrypt, decrypt

test_strings = [
    "hello my friend", "p@sswo0rd",
    "correct horse battery staple", "1233456659493228",
    "why god why god", "__________________3284_______",
    "what you want?", "a a a a b b b c c c c d d d de"
]

def test_encrypt():
    test_pw = "password"

    for s in test_strings:
        assert decrypt(encrypt(s, p=test_pw), p=test_pw) == s


def test_incorrect_pw():
    test_pw = "password"

    for s in test_strings:
        assert decrypt(encrypt(s, p=test_pw),p="wrong pw") != s
