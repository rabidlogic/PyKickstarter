#! /usr/bin/python

from collections import namedtuple

from PyKickstarterProject import *

class PyKickstarterLocation(object):

    def __init__(self, data, api, access_token):
        self.data = namedtuple('GenericDict', data.keys())(**data)
        self.api = api
        self.access_token = access_token

    def get_nearby_projects(self):
        return PyKickstarterProjectGenerator(self.api.request("GET", self.data.urls['api']['neaby_projects'] + "&oauth_token=" + self.access_token), self.api, self.access_token)
