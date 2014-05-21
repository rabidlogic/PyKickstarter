#! /usr/bin/python

from collections import namedtuple

class PyKickstarterNotificationGenerator(object):

    def __init__(self, data, api, access_token):
        self.data = data
        self.api = api
        self.access_token = access_token

    def next(self):
        for notification in self.data:
            yield PyKickstarterNotification(notification, self.api, self.access_token)

class PyKickstarterNotification(object):

    def __init__(self, data, api, access_token):
        self.initialize(data)
        self.api = api
        self.access_token = access_token

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def acknowledge(self):
        self.api.request("GET", self.data.urls['api']['notification'] + self.access_token)
