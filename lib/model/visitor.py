from lib.util.crypto import decrypt
from lib.model.db.visitor import Visitor, VisitorSession
from time import time


def decrypt_id(encrypted, config):
    try:
        return int(decrypt(str(encrypted), config['encryption_key_visitor']))
    except Exception:
        return 0


def init_session(visitor):

    if visitor is None or visitor.session.timeout <= int(time()):
        visitor_session = VisitorSession(
            is_new=True,
            timeout=int(time()) + 1800
        )
        visitor = Visitor(session=visitor_session)
    else:
        visitor.session.is_new = False
        visitor.session.timeout = int(time()) + 1800

    return visitor


def get_by_id(visitor_id):
    visitor = None
    visitor_id = int(visitor_id)

    if visitor_id != 0:
        visitor = Visitor.get_by_id(visitor_id)

    return init_session(visitor)
