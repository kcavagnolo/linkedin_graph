#!/usr/bin/env python

import os
import oauth2 as oauth
import urlparse
import hashlib
import webbrowser
import urllib
import urllib2
import ast

consumer_key = str(os.environ['LINKEDIN_API_KEY'])
consumer_secret = str(os.environ['LINKEDIN_API_SECRET'])
redirect_uri = 'http%3A%2F%2Flocalhost%3A8080%2Fcode'

random_data = os.urandom(128)
state_key = hashlib.md5(random_data).hexdigest()[:16]

request_token_url = 'https://www.linkedin.com/uas/oauth2/authorization?'
access_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken?'

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)
params = '&'.join(
    ["response_type=code",
     "client_id="+consumer_key,
     "redirect_uri="+redirect_uri,
     "state="+state_key,
     "scope=r_basicprofile"])
resp, content = client.request(request_token_url+params, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])
authorize_url = resp['content-location']

webbrowser.open(authorize_url,new=2)
key = raw_input('Paste the code here: ')
state = key.split('&')[1].split('=')[1]
if state != state_key:
   raise Exception("State key error. Being attacked?")
oauth_verifier = key.split('&')[0].split('=')[1]

params = '&'.join(
    ["grant_type=authorization_code",
     "code="+oauth_verifier,
     "redirect_uri="+redirect_uri,
     "client_id="+consumer_key,
     "client_secret="+consumer_secret])

resp = urllib2.urlopen(urllib2.Request(access_token_url, params))
content = resp.read()
token = ast.literal_eval(content)['access_token']
print "run >>> setenv LINKEDIN_API_TOKEN \'%s\'" % oauth_verifier
print "run >>> setenv LINKEDIN_API_TOKEN_SECRET \'%s\'" % token
