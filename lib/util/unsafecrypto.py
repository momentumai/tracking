from Crypto.Cipher import AES
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import md5

def _pad(data):
    size = 16 - len(data) % 16
    return data + size * chr(size)


def _unpad(padded):
    size = ord(padded[-1])
    return padded[:-size]


def encrypt(data, password):
    m = md5()
    m.update(password)
    key = m.hexdigest()

    m = md5()
    m.update(password + key)
    iv = m.hexdigest()

    data = _pad(data)

    aes = AES.new(key, AES.MODE_CBC, iv[:16])

    encrypted = aes.encrypt(data)
    return urlsafe_b64encode(encrypted)


def decrypt(data, password):
    data = urlsafe_b64decode(str(data))

    m = md5()
    m.update(password)
    key = m.hexdigest()

    m = md5()
    m.update(password + key)
    iv = m.hexdigest()

    aes = AES.new(key, AES.MODE_CBC, iv[:16])
    return _unpad(aes.decrypt(data))

