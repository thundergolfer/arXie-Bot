import struct
from Crypto.Cipher import AES

from bot.settings import config

db_token = config.db_token


def pad16(ss):
    t = struct.pack('>I', len(ss)) + ss.encode('utf-8')
    return t + b'\x00' * ((16 - len(t) % 16) % 16)


def unpad16(s):
    n = struct.unpack('>I', s[:4])[0]
    return s[4:n + 4]


class Crypt(object):
    def __init__(self, password):
        password = pad16(password)
        self.cipher = AES.new(password, AES.MODE_ECB)

    def encrypt(self, s):
        s = pad16(s)
        return self.cipher.encrypt(s)

    def decrypt(self, s):
        t = self.cipher.decrypt(s)
        return unpad16(t)


def encrypt(s, p=db_token):
    c = Crypt(p)
    return c.encrypt(s)


def decrypt(s, p=db_token):
    crypt = Crypt(p)
    try:
        return crypt.decrypt(s).decode('utf-8')
    except UnicodeDecodeError:
        return ""
