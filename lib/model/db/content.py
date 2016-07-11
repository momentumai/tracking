from google.appengine.ext import ndb


class Content(ndb.Model):
    content_id = ndb.StringProperty(required=True, indexed=True)
    is_blacklisted = ndb.BooleanProperty(indexed=False)
    category_map = ndb.StringProperty(indexed=False)
