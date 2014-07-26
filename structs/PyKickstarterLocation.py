#! /usr/bin/python

from collections import namedtuple

try:
    from PyKickstarterProject import *
except:
    from .PyKickstarterProject import *

class PyKickstarterLocation(object):

    def __init__(self, data, api):
        self.data = namedtuple('GenericDict', data.keys())(**data)
        self.api = api

    def get_nearby_projects(self):
        return PyKickstarterProjectGenerator(self.api.request("GET", self.data.urls['api']['neaby_projects']), self.api)
