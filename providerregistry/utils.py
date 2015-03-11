#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written By Alan Viars

import requests
import json
from django.conf import settings
import urllib, hashlib
import collections


def hash_gravatar_email(email):
    hashed_email = hashlib.md5(email.lower()).hexdigest()
    return hashed_email

def googlemap_address_query(address_1, address_2="", city="", state="", zipcode=""):
   address = "%s %s %s %s %s" % (address_1, address_2, city, state, zipcode)
   google_address = str(address).replace(" ", "+")
   return address

def check_if_resource_exists(number, url = settings.PROVIDER_STATIC_HOST):
    provider_url = "%snpi/%s.json" % (url, number)
    status = 500
    try:
        r = requests.head(provider_url)
        status = r.status_code
        #prints the int of the status code. Find more at httpstatusrappers.com :)
    except requests.ConnectionError:
        status = 000
    return status


def get_resource(number, url = settings.PROVIDER_STATIC_HOST):
    provider_url = "%snpi/%s.json" % (url, number)
    d = collections.OrderedDict()
    try:
        r = requests.get(provider_url)
        #print r.text
        #print r.json()
        d = json.loads(r.text, object_pairs_hook=collections.OrderedDict)
    except requests.ConnectionError:
        d = collections.OrderedDict()
    return d

def get_gravatar_url(hashed_email):
    
    default = "mm"
    size   = 140
    gravatar_url = "https://www.gravatar.com/avatar/" + hashed_email + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size), 'r':'g'})
    return gravatar_url
    