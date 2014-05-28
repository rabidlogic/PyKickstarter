#! /usr/bin/python

import httplib
import urllib
import json

class PyKickstarterAPI(object):
    
    HEADERS = { "Accept" : "application/json; charset=utf-8", "User-Agent" : "PyKickstarter/v3.0" }

    #def __init__(self):
    #    self.conn = httplib.HTTPSConnection("api.kickstarter.com")

    def request(self, method, url, data=None):
        self.conn = httplib.HTTPSConnection("api.kickstarter.com")
        if (data != None):
            data = json.dumps(data)
        self.conn.request(method, url, data, PyKickstarterAPI.HEADERS)
        response = self.conn.getresponse()
        return json.load(response)

    def encode_get_params(self, params):
        return urllib.urlencode(params)
