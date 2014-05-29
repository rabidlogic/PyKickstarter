#! /usr/bin/python

from urlparse import urlsplit, parse_qs, urlunsplit
from urllib import urlencode

import httplib
import json

class PyKickstarterAPI(object):
    
    HEADERS = { "Accept" : "application/json; charset=utf-8", "User-Agent" : "PyKickstarter/v3.0" }

    def __init__(self, access_token):
        self.set_access_token(access_token)

    def set_access_token(self, access_token):
        self.access_token = access_token

    def request(self, method, url, data=None):
        self.conn = httplib.HTTPSConnection("api.kickstarter.com")
        if (data != None):
            data = json.dumps(data)
        url = self.add_access_token(url)
        self.conn.request(method, url, data, PyKickstarterAPI.HEADERS)
        response = self.conn.getresponse()
        return json.load(response)

    def add_access_token(self, url):
        url_parts = urlsplit(url)
        query_str = url_parts.query
        query_parts = parse_qs(query_str)
        query_parts = dict(query_parts.items() + [ self.access_token ])
        query_str = urlencode(query_parts, doseq=True)
        new_url = ( url_parts.scheme, url_parts.netloc, url_parts.path, query_str, url_parts.fragment )
        return urlunsplit(new_url)
        
