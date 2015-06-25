#!/usr/bin/env python

import os
import oauth2 as oauth
import urlparse
import simplejson
import codecs
import requests

consumer_key = str(os.environ['LINKEDIN_API_KEY'])
consumer_secret = str(os.environ['LINKEDIN_API_SECRET'])
api_token = str(os.environ['LINKEDIN_API_TOKEN'])
OUTPUT = "linked.csv"

response = requests.get(
    'https://api.linkedin.com/v1/people/~?format=json',
    headers={'Authorization': api_token})
print response.content
exit()


def linkedin_connections():

    # Use your credentials to build the oauth client
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(key=api_token, secret=api_token_secret)
    print token
    client = oauth.Client(consumer, token)


    # Fetch first degree connections
    resp, content = client.request('http://api.linkedin.com/v1/people/~/connections?format=json')
    results = simplejson.loads(content)    
    print results

    # File that will store the results
    output = codecs.open(OUTPUT, 'w', 'utf-8')

    # Loop thru the 1st degree connection and see how they connect to each other
    for result in results["values"]:
        con = "%s %s" % (result["firstName"].replace(",", " "), result["lastName"].replace(",", " "))
        print >>output, "%s,%s" % ("Ken Cavagnolo",  con)

        # This is the trick, use the search API to get related connections
        u = "https://api.linkedin.com/v1/people/%s:(relation-to-viewer:(related-connections))?format=json" % result["id"]
        resp, content = client.request(u)
        rels = simplejson.loads(content)
        try:
            for rel in rels['relationToViewer']['relatedConnections']['values']:
                sec = "%s %s" % (rel["firstName"].replace(",", " "), rel["lastName"].replace(",", " "))
                print >>output, "%s,%s" % (con, sec)
        except:
            pass
    

if __name__ == '__main__':
    linkedin_connections()
