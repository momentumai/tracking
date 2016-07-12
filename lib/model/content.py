from lib.model.db.content import Content
import uuid


def get_by_url(url, contex):
    return Content.get_or_insert(
        url,
        content_id=str(uuid.uuid4()),
        is_blacklisted=False,
        category_map=contex['category_map']
    )


def update_content(obj, contex):
    update = False
    if str(obj.category_map) != str(contex['category_map']):
        update = True
        obj.category_map = contex['category_map']

    if update:
        return obj.put_async()

    return None
