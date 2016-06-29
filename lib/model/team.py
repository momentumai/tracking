from lib.util.unsafecrypto import decrypt


def decrypt_id(encrypted, config):
    try:
        return int(decrypt(str(encrypted), config['encryption_key_team']))
    except Exception:
        return 0
