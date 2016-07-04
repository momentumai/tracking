from google.appengine.ext import ndb


class Category(ndb.Model):
    created_at = ndb.DateTimeProperty(indexed=False, auto_now_add=True)
