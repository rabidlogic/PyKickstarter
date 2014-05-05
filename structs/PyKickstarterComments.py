#! /usr/bin/python

from collections import namedtuple

from PyKickstarterUser import *

class PyKickstarterCommentsGenerator(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data):
        self.comments = data['comments']
        self.set_more(data)

    def set_more(self, data):
        if data['urls']['api'].has_key('more_comments'):
            self.more = data['urls']['api']['more_comments']
        else:
            self.more = None

    def next(self):
        idx = 0
        while (idx < len(self.comments)):
            project = PyKickstarterComment(self.comments[idx], self.api, self.access_token)
            yield project
            if (self.more != None and idx == len(self.comments) - 1):
                data = self.api.request("GET", self.more + "&oauth_token=" + self.access_token)
                self.initialize(data)
                idx = 0
            else:
                idx += 1

class PyKickstarterComment(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data): 
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def get_author(self):
        print str(self.api.request("GET", self.data.author['urls']['api']['user'] + "&oauth_token=" + self.access_token, self.access_token))
