from google.appengine.ext import ndb


class VisitorSession(ndb.Model):
    timeout = ndb.IntegerProperty(required=True, indexed=False)
    is_new = ndb.BooleanProperty(required=True, indexed=False)
    visited_contents = ndb.StringProperty(repeated=True, indexed=False)
    visited_cat1_contents = ndb.StringProperty(repeated=True, indexed=False)
    visited_cat2_contents = ndb.StringProperty(repeated=True, indexed=False)
    visited_cat3_contents = ndb.StringProperty(repeated=True, indexed=False)


class Visitor(ndb.Model):
    session = ndb.LocalStructuredProperty(VisitorSession, required=True, indexed=False)
