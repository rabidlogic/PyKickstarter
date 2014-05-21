#! /usr/bin/python

from collections import namedtuple

from PyKickstarterComments import PyKickstarterCommentsGenerator

class PyKickstarterUpdatesGenerator(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data):
        self.updates = data['updates']
        self.set_more(data)

    def set_more(self, data):
        if data['urls']['api'].has_key('more_updates'):
            self.more = data['urls']['api']['more_updates']
        else:
            self.more = None

    def next(self):
        idx = 0
        while (idx < len(self.updates)):
            project = PyKickstarterUpdate(self.updates[idx], self.api, self.access_token)
            yield project
            if (self.more != None and idx == len(self.updates) - 1):
                data = self.api.request("GET", self.more + self.access_token)
                self.initialize(data)
                idx = 0
            else:
                idx += 1

class PyKickstarterUpdate(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def get_comments(self):
        return PyKickstarterCommentsGenerator(self.api.request("GET", self.data.urls['api']['comments'] + self.access_token), self.api, self.access_token)

    def refresh(self):
        self.initialize(self.api.request("GET", self.data.urls['api']['update'] + self.access_token))

    def post_comment(self, body):
        self.api.request("POST", self.data.urls['api']['comments'] + self.access_token, { 'body' : body })
