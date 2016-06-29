from base64 import urlsafe_b64decode, urlsafe_b64encode
from Crypto.Cipher import AES
import string
import random


def _pad(data):
    size = 16 - len(data) % 16
    return data + size * chr(size)


def _unpad(padded):
    size = ord(padded[-1])
    return padded[:-size]


def decrypt(text, key):
    text = urlsafe_b64decode(text)
    iv = text[:16]
    text = text[16:]
    dec = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    return _unpad(dec.decrypt(text))


def encrypt(text, key):
    text = str(text)
    iv = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    dec = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    return urlsafe_b64encode(iv + dec.encrypt(_pad(text)))
