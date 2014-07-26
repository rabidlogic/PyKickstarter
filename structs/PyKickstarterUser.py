#! /usr/bin/python

from collections import namedtuple

try:
    from PyKickstarterProject import *
except:
    from .PyKickstarterProject import *

class PyKickstarterUser(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def get_created_projects(self):
        return PyKickstarterProjectGenerator(self.api.request("GET", self.data.urls['api']['created_projects']), self.api)

    def refresh(self):
        self.initialize(self.api.request("GET", self.data.urls['api']['user']))

    def get_location(self):
        return PyKickstarterLocation(self.data.location, self.api)        
