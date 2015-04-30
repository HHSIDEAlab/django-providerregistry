#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written By Alan Viars

import requests
import json, sys
from django.conf import settings
import urllib, hashlib
import collections
from bson.code import Code
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId



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
    
def query_mongo(database_name, collection_name, query={},
                skip=0, sort=None, limit=settings.MONGO_LIMIT, return_keys=()):
    """return a response_dict  with a list of search results"""
    print query    
    
    l=[]
    response_dict={}
    
    try:
        mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
        
        db          =   mc[str(database_name)]
        collection   = db[str(collection_name)]
        
        
        #print query
        if return_keys:
            return_dict={}
            for k in return_keys:
                return_dict[k]=1
            #print "returndict=",return_dict
            mysearchresult=collection.find(query, return_dict).skip(skip).limit(limit)
        else:            
            mysearchresult=collection.find(query).skip(skip).limit(limit)
        
        if sort:
            mysearchresult.sort(sort)

        response_dict['code']=200
        response_dict['type']="search-results"
        for d in mysearchresult:
            d['id'] = d['_id'].__str__()
            del d['_id']
            l.append(d)
        response_dict['results']=l
            
    except:
        print "Error reading from Mongo"
        print str(sys.exc_info())
        response_dict['code']=500
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    
    return response_dict
