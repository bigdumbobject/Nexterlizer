#!/usr/bin/env python

import wsgiref.handlers
import logging

from google.appengine.ext import webapp

import sys

import WebHandler

## main ##

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/', WebHandler.WebHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
