#! /usr/bin/python

from collections import namedtuple

try:
    from PyKickstarterComments import PyKickstarterCommentsGenerator
except:
    from .PyKickstarterComments import PyKickstarterCommentsGenerator

class PyKickstarterUpdatesGenerator(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data):
        self.updates = data['updates']
        self.set_more(data)

    def set_more(self, data):
        if 'more_updates' in data['urls']['api']:
            self.more = data['urls']['api']['more_updates']
        else:
            self.more = None

    def next(self):
        idx = 0
        while (idx < len(self.updates)):
            project = PyKickstarterUpdate(self.updates[idx], self.api)
            yield project
            if (self.more != None and idx == len(self.updates) - 1):
                data = self.api.request("GET", self.more)
                self.initialize(data)
                idx = 0
            else:
                idx += 1

class PyKickstarterUpdate(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def get_comments(self):
        return PyKickstarterCommentsGenerator(self.api.request("GET", self.data.urls['api']['comments']), self.api)

    def refresh(self):
        self.initialize(self.api.request("GET", self.data.urls['api']['update']))

    def post_comment(self, body):
        self.api.request("POST", self.data.urls['api']['comments'], { 'body' : body })
