#!/usr/bin/env python

import xml.etree.ElementTree as ET
import urllib
import urllib2
import logging
import hmac
import datetime
import hashlib
import base64
import AccessIds

from google.appengine.api import urlfetch

def GetUrl(associateId, countryUrl, urlString):

	# Keys and timestamp
	#AMAZON_ACCESS_KEY_ID = 'Insert'
	#AMAZON_SECRET_ACCESS_KEY = 'Insert'
	timestamp = urllib2.quote(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'))
	
	# Create the string to sign
	canonicalString = 'AWSAccessKeyId=' + AccessIds.AMAZON_ACCESS_KEY_ID + '&AssociateTag=' + associateId + urlString + '&Service=AWSECommerceService' + '&Timestamp=' + timestamp + '&Version=2009-07-01'
	#logging.debug(canonicalString)
	stringToSign = 'GET\necs.amazonaws.' + countryUrl + '\n/onca/xml\n' + canonicalString

	# Get the message signature
	digest_maker = hmac.new(AccessIds.AMAZON_SECRET_ACCESS_KEY, stringToSign, hashlib.sha256)
	rawsig = base64.encodestring(hmac.new(AccessIds.AMAZON_SECRET_ACCESS_KEY, stringToSign, hashlib.sha256).digest()).strip()
	#logging.debug(rawsig)
	signature = urllib.quote_plus(rawsig)
	
	# Create the full url
	awsurl = 'http://ecs.amazonaws.' + countryUrl + '/onca/xml?' + canonicalString + '&Signature=' + signature
	return awsurl


def AmazonSimilarLookup(last, country, index, itemIndex):
  
	# Did we specify an Amazon item index
	if (index == None):
		index = "All"

	# Did we sepcify an index of which similar item to get?
	if (itemIndex == None):
		itemIndex = 0

	# Return codes
	itemStatus = 0
	similarStatus = 200

	# Amazon namespace
	AMAZON_NS = 'http://webservices.amazon.com/AWSECommerceService/2009-07-01'

	# Get the root url given the country
	associateId = "bigdumbobject-20"
	countryUrl = "com"

	if (country == "GB" and index != "All" ):
		countryUrl = "co.uk"
		associateId = "jamesthebloom-20"

	# Construct an Amazon lookup url for lookup with similar item response group
	awsurl = GetUrl(associateId, countryUrl, '&Keywords=' + urllib2.quote(last) + '&Operation=ItemSearch' + '&ResponseGroup=Similarities&SearchIndex=' + index)

	#logging.debug(awsurl)

	title = "something else"
	url = "http://www.amazon.com/gp/redirect.html?ie=UTF8&location=http%3A%2F%2Fwww.amazon.com%2Fgp%2Fhomepage.html%3Fie%3DUTF8%26%252AVersion%252A%3D1%26%252Aentries%252A%3D0&tag=bigdumbobject-20&linkCode=ur2&camp=1789&creative=390957"
  
	# Call the Amazon web service to get similar items
	try:	
		result = urlfetch.fetch(awsurl, deadline=10)
		itemStatus = result.status_code
		#logging.debug(itemStatus)
		if result.status_code == 200:
			el = ET.fromstring(result.content)
			# TODO Needs a better xpath here as search returns multiple matches to the keywords
			# and each match has a similar items list, many of which are duplicates
			asinobj = el.findall('.//{%s}SimilarProduct/{%s}ASIN' % (AMAZON_NS,AMAZON_NS))
			#logging.debug(asinobj)

		# If there were no similar items leave similarStatus as 200 and return the generic search
		if asinobj != None:
			asin = asinobj[itemIndex].text
		
			# Now do an item lookup on the similar item ASIN
			asinurl = GetUrl(associateId, countryUrl, '&IdType=ASIN&ItemId=' + asin + '&Operation=ItemLookup')
			
			#logging.debug(asinurl)          
			result2 = urlfetch.fetch(asinurl, deadline=10)

			similarStatus = result2.status_code
			if result2.status_code == 200:
				el2 = ET.fromstring(result2.content)
				title = el2.find('.//{%s}Item/{%s}ItemAttributes/{%s}Title' % (AMAZON_NS,AMAZON_NS,AMAZON_NS)).text
				url = el2.find('.//{%s}Item/{%s}DetailPageURL' % (AMAZON_NS,AMAZON_NS)).text

	except:
		logging.error("URLFetch error")		
		  
	return (itemStatus == 200 and similarStatus == 200), title, url


