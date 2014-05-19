#! /usr/bin/python

from datetime import datetime

def make_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp)
