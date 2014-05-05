#! /usr/bin/python

from collections import namedtuple

from PyKickstarterUpdates import *
from PyKickstarterComments import *
from PyKickstarterUser import *
from PyKickstarterLocation import * 

class PyKickstarterProjectGenerator(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data):
        self.projects = data['projects']
        self.set_more(data)

    def set_more(self, data):
        if data['urls']['api'].has_key('more_projects'):
            self.more = data['urls']['api']['more_projects']
        else:
            self.more = None

    def next(self):
        idx = 0
        while (idx < len(self.projects)):
            project = PyKickstarterProject(self.projects[idx], self.api, self.access_token)
            yield project
            if (self.more != None and idx == len(self.projects) - 1):
                data = self.api.request("GET", self.more + "&oauth_token=" + self.access_token)
                self.initialize(data)
                idx = 0
            else:
                idx += 1

class PyKickstarterProject(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def enrich(self):
        response = self.api.request("GET", self.data.urls['api']['project'] + '&oauth_token=' + self.access_token)
        self.initialize(response)

    def get_updates(self):
        return PyKickstarterUpdatesGenerator(self.api.request("GET", self.data.urls['api']['updates'] + '&oauth_token=' + self.access_token), self.api, self.access_token)

    def get_comments(self):
        return PyKickstarterCommentsGenerator(self.api.request("GET", self.data.urls['api']['comments'] + '&oauth_token=' + self.access_token), self.api, self.access_token)

    def get_apis(self):
        return self.data.urls['api']

    def star(self):
        self.api.request("PUT", self.data.urls['api']['star'] + "&oauth_token=" + self.access_token)

    def unstar(self):
        self.api.request("DELETE", self.data.urls['api']['star'] + "&oauth_token=" + self.access_token)

    def get_creator(self):
        return PyKickstarterUser(self.api.request("GET", self.data.creator['urls']['api']['user'] + "&oauth_token=" + self.access_token), self.api, self.access_token)

    def get_location(self):
        return PyKickstarterLocation(self.data.location, self.api, self.access_token)

