#!/usr/bin/env python

from google.appengine.ext import db

### Entities ###
class Run(db.Model):
  lastrundate = db.DateTimeProperty(auto_now=True)
  since = db.IntegerProperty()

class NexterlizerRequest(db.Model):
  tweetid = db.IntegerProperty()
  user = db.StringProperty()
  text = db.StringProperty()
  location = db.StringProperty()
  complete = db.BooleanProperty(default=False)
  index = db.StringProperty(default='All')
  
class NexterlizerResponse(db.Model):
  tweetid = db.IntegerProperty()
  user = db.StringProperty()
  title = db.StringProperty()
  url = db.LinkProperty()
  complete = db.BooleanProperty(default=False)

