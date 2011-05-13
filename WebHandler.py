#!/usr/bin/env python

import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import AmazonHelper

class WebHandler(webapp.RequestHandler):

  def get(self):
          
    # Render the template
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, None))


  def post(self):
    
    # posted variables
    last = self.request.get('last')
    country = self.request.get('country')
    index = self.request.get('index')
    itemIndex = self.request.get('itemIndex')
	
	# Increase the item index number
    if itemIndex == None:
        itemIndex = 0
    elif len(itemIndex) == 0:
        itemIndex = 0
    else:
        itemIndex = int(itemIndex) + 1

    logging.info('country %s' % country)

    # Amazon lookup
    status, title, url = AmazonHelper.AmazonSimilarLookup(last, country, index, itemIndex)

    # Set up template values
    template_values = {
      'last': last,
      'title': title,
      'url': url,
      'something_else' : title == 'something else',
      'index': index,
      'itemIndex': itemIndex
     }

    # Render the template
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

