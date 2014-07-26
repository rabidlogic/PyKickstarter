#! /usr/bin/python

from collections import namedtuple

try:
    from PyKickstarterUser import *
except:
    from .PyKickstarterUser import *

class PyKickstarterCommentsGenerator(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data):
        self.comments = data['comments']
        self.set_more(data)

    def set_more(self, data):
        if 'more_comments' in data['urls']['api']:
            self.more = data['urls']['api']['more_comments']
        else:
            self.more = None

    def next(self):
        idx = 0
        while (idx < len(self.comments)):
            project = PyKickstarterComment(self.comments[idx], self.api)
            yield project
            if (self.more != None and idx == len(self.comments) - 1):
                data = self.api.request("GET", self.more)
                self.initialize(data)
                idx = 0
            else:
                idx += 1

class PyKickstarterComment(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data): 
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def get_author(self):
        response = self.api.request("GET", self.data.author['urls']['api']['user'])
        return PyKickstarterUser(response, self.api)
