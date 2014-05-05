#! /usr/bin/python

import httplib
import json

class PyKickstarterAPI(object):
    
    HEADERS = { "Accept" : "application/json; charset=utf-8", "User-Agent" : "PyKickstarter/v1.0" }

    def __init__(self):
        self.conn = httplib.HTTPSConnection("api.kickstarter.com")

    def request(self, method, url, data=None):
        self.conn.request(method, url, data, PyKickstarterAPI.HEADERS)
        response = self.conn.getresponse()
        return json.load(response)
