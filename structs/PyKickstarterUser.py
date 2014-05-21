#! /usr/bin/python

from collections import namedtuple

from PyKickstarterProject import *

class PyKickstarterUser(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def get_created_projects(self):
        return PyKickstarterProjectGenerator(self.api.request("GET", self.data.urls['api']['created_projects'] + self.access_token), self.api, self.access_token)

    def refresh(self):
        self.initialize(self.api.request("GET", self.data.urls['api']['user'] + self.access_token))

    def get_location(self):
        return PyKickstarterLocation(self.data.location, self.api, self.access_token)        
