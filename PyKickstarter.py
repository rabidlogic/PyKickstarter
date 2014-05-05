#! /usr/bin/python

import urllib2
import json
import sys

from collections import namedtuple
from utilities.PyKickstarterAPI import PyKickstarterAPI
from structs.PyKickstarterProject import PyKickstarterProjectGenerator
from structs.PyKickstarterUser import PyKickstarterUser
from structs.PyKickstarterNotification import PyKickstarterNotificationGenerator

class PyKickstarter(object):

    API_URL = "https://api.kickstarter.com"
    API_KEY = "2II5GGBZLOOZAA5XBU1U0Y44BU57Q58L8KOGM7H0E0YFHP3KTG"
    TOK_URI = "/xauth/access_token?client_id="

    def __init__(self, email, password):
        self.api = PyKickstarterAPI()
        login_data = json.dumps({ "email" : email, "password" : password })
        response = self.api.request("POST", PyKickstarter.API_URL + PyKickstarter.TOK_URI + PyKickstarter.API_KEY, login_data)
        self.access_token = self.get_auth_token(response)
        self.user = self.get_account(response)

    def valid(self):
        return True if (self.access_token == -1) else False

    def get_auth_token(self, data):
        return data['access_token'] if data.has_key('access_token') else -1

    def get_account(self, data):
        return namedtuple('GenericDict', data['user'].keys())(**data['user']) if data.has_key('user') else None

    def get_backed_projects(self):
        response = self.api.request("GET", self.user.urls['api']['backed_projects'] + "&oauth_token=" + self.access_token)
        return PyKickstarterProjectGenerator(response, self.api, self.access_token)

    def get_starred_projects(self):
        response = self.api.request("GET", self.user.urls['api']['starred_projects'] + "&oauth_token=" + self.access_token)
        return PyKickstarterProjectGenerator(response, self.api, self.access_token)

    def get_created_projects(self):
        response = self.api.request("GET", self.user.urls['api']['created_projects'] + "&oauth_token=" + self.access_token)
        return PyKickstarterProjectGenerator(response, self.api, self.access_token)

    def get_notifications(self):
        response = self.api.request("GET", self.user.urls['api']['notifications'] + "&oauth_token=" + self.access_token)
        return PyKickstarterNotificationGenerator(response, self.api, self.access_token)

    def get_location(self):
        return PyKickstarterLocation(self.user.location, self.api, self.access_token)

    def refresh_user(self):
        response = self.api.request("GET", self.user.urls['api']['user'] + "&oauth_token=" + self.access_token)
        self.data = self.get_account({ 'user' : response })
