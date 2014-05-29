#! /usr/bin/python

from collections import namedtuple

class PyKickstarterNotificationGenerator(object):

    def __init__(self, data, api):
        self.data = data
        self.api = api

    def next(self):
        for notification in self.data:
            yield PyKickstarterNotification(notification, self.api)

class PyKickstarterNotification(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def acknowledge(self):
        self.api.request("GET", self.data.urls['api']['notification'])
