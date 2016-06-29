from lib.model.db.content import Content
import uuid


def get_by_url(url):
    return Content.get_or_insert(
        url,
        content_id=str(uuid.uuid4()),
        is_blacklisted=False
    )