#! /usr/bin/python

import json

from collections import namedtuple
from utilities.PyKickstarterAPI import PyKickstarterAPI
from structs.PyKickstarterProject import PyKickstarterProjectGenerator
from structs.PyKickstarterUser import PyKickstarterUser
from structs.PyKickstarterNotification import PyKickstarterNotificationGenerator

class PyKickstarter(object):

    API_ROOT = "https://api.kickstarter.com"
    API_KEY = "client_id=2II5GGBZLOOZAA5XBU1U0Y44BU57Q58L8KOGM7H0E0YFHP3KTG"

    API_URLS = {
            'authenticate' : API_ROOT + "/xauth/access_token",
            'search' : API_ROOT + "/v1/projects/search",
            'get_categories' : API_ROOT + "/v1/categories",
            'category_search' : API_ROOT + "/v1/categories/%d/projects/popular", # Needs the Category ID
            'picks' : API_ROOT + "/v1/categories/projects/picks"
    }

    def __init__(self):
        self.api = PyKickstarterAPI()

    def login(self, email, password):
        response = self.api.request("POST", PyKickstarter.API_URLS['authenticate'] + "?" + PyKickstarter.API_KEY, { "email" : email, "password" : password })
        self.access_token = "&oauth_token=" + self.get_auth_token(response)
        self.user = self.get_account(response)

    def logged_in(self):
        return True if (self.access_token == -1) else False

    def get_auth_token(self, data):
        return data['access_token'] if data.has_key('access_token') else -1

    def get_account(self, data):
        return namedtuple('GenericDict', data['user'].keys())(**data['user']) if data.has_key('user') else None

    def get_backed_projects(self):
        response = self.api.request("GET", self.user.urls['api']['backed_projects'] + self.access_token)
        return PyKickstarterProjectGenerator(response, self.api, self.access_token)

    def get_starred_projects(self):
        response = self.api.request("GET", self.user.urls['api']['starred_projects'] + self.access_token)
        return PyKickstarterProjectGenerator(response, self.api, self.access_token)

    def get_created_projects(self):
        response = self.api.request("GET", self.user.urls['api']['created_projects'] + self.access_token)
        return PyKickstarterProjectGenerator(response, self.api, self.access_token)

    def get_notifications(self):
        response = self.api.request("GET", self.user.urls['api']['notifications'] + self.access_token)
        return PyKickstarterNotificationGenerator(response, self.api, self.access_token)

    def get_location(self):
        return PyKickstarterLocation(self.user.location, self.api, self.access_token)

    def refresh_user(self):
        response = self.api.request("GET", self.user.urls['api']['user'] + self.access_token)
        self.data = self.get_account({ 'user' : response })

    def search_projects(self, search_terms):
        response = self.api.request("GET", PyKickstarter.API_URLS['search'] + "?" + self.api.encode_get_params({ 'q' : search_terms }) + "&" + PyKickstarter.API_KEY)
        return PyKickstarterProjectGenerator(response, self.api, "&" + PyKickstarter.API_KEY)

    def get_categories(self):
        return self.api.request("GET", PyKickstarter.API_URLS['get_categories'] + "?" + PyKickstarter.API_KEY)

    def get_category_projects(self, category_id):
        response = self.api.request("GET", PyKickstarter.API_URLS['category_search'] % category_id + "?" + PyKickstarter.API_KEY)
        return PyKickstarterProjectGenerator(response, self.api, "&" + PyKickstarter.API_KEY)

    def get_staff_picks_projects(self):
        response = self.api.request("GET", PyKickstarter.API_URLS['picks'] + "?" + PyKickstarter.API_KEY)
        return PyKickstarterProjectGenerator(response, self.api, "&" + PyKickstarter.API_KEY)
