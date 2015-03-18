#!/usr/bin/env python

import oauth2 as oauth
import urlparse
import simplejson
import codecs

consumer_key = "scrape_deez_nutz"
consumer_secret = "scrape_deez_nutz"

OAUTH_TOKEN = "scrape_deez_nutz"
OAUTH_TOKEN_SECRET = "scrape_deez_nutz"

OUTPUT = "linked.csv"

def linkedin_connections():
    # Use your credentials to build the oauth client
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    # Fetch first degree connections
    resp, content = client.request('http://api.linkedin.com/v1/people/~/connections?format=json')
    results = simplejson.loads(content)    
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
