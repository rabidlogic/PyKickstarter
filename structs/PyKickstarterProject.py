#! /usr/bin/python

from collections import namedtuple

try:
    from PyKickstarterUpdates import *
    from PyKickstarterComments import *
    from PyKickstarterUser import *
    from PyKickstarterLocation import * 
except:
    from .PyKickstarterUpdates import *
    from .PyKickstarterComments import *
    from .PyKickstarterUser import *
    from .PyKickstarterLocation import *

class PyKickstarterProjectGenerator(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data):
        self.projects = data['projects']
        self.set_more(data)

    def set_more(self, data):
        if 'more_projects' in data['urls']['api']:
            self.more = data['urls']['api']['more_projects']
        else:
            self.more = None

    def next(self):
        idx = 0
        while (idx < len(self.projects)):
            project = PyKickstarterProject(self.projects[idx], self.api)
            yield project
            if (self.more != None and idx == len(self.projects) - 1):
                data = self.api.request("GET", self.more)
                self.initialize(data)
                idx = 0
            else:
                idx += 1

class PyKickstarterProject(object):

    def __init__(self, data, api):
        self.initialize(data)
        self.api = api

    def initialize(self, data):
        self.data = namedtuple('GenericDict', data.keys())(**data)

    def enrich(self):
        response = self.api.request("GET", self.data.urls['api']['project'])
        self.initialize(response)

    def get_updates(self):
        return PyKickstarterUpdatesGenerator(self.api.request("GET", self.data.urls['api']['updates']), self.api)

    def get_comments(self):
        return PyKickstarterCommentsGenerator(self.api.request("GET", self.data.urls['api']['comments']), self.api)

    def get_apis(self):
        return self.data.urls['api']

    def star(self):
        self.api.request("PUT", self.data.urls['api']['star'])

    def unstar(self):
        self.api.request("DELETE", self.data.urls['api']['star'])

    def get_creator(self):
        return PyKickstarterUser(self.api.request("GET", self.data.creator['urls']['api']['user']), self.api)
    def get_location(self):
        return PyKickstarterLocation(self.data.location, self.api)

    def get_rewards(self):
        return self.data.rewards if hasattr(self.data, 'rewards') else []

    def get_backed_reward(self):
        if self.data.is_backing and hasattr(self.data, 'backing'):
            r_id = self.data.backing['reward_id']
            for reward in self.get_rewards():
                if reward['id'] == r_id:
                    return reward
        return None

    def post_comment(self, body):
        self.api.request("POST", self.data.urls['api']['comments'], { 'body' : body })

    def message_creator(self, body):
        self.api.request("POST", self.data.urls['api']['message_creator'], { 'body' : body })
