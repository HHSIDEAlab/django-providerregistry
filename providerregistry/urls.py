#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written  By Alan Viars

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   
    
    url(r'^provider-lookup$', provider_lookup, name="provider_lookup"),
    
    url(r'^provider-view/(?P<number>[^/]+)$', provider_profile, name="provider_profile"),
    
    url(r'^provider-details/(?P<number>[^/]+)$', provider_details, name="provider_details"),
    
    url(r'^provider-search$', provider_search, name="provider_search"),
    
    url(r'^search-results-table$', search_results_table, name="search_results_table"),
    
    url(r'^search-results$', search_results_gallery, name="search_results_gallery"),
    
    url(r'^$', index, name="registry_index"),
    )
