#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written  By Alan Viars
import urllib
from django.conf import settings
from django.shortcuts import render
from forms import ProviderLookupForm, ProviderSearchForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import random, urllib, json
from utils import (check_if_resource_exists, get_resource, hash_gravatar_email,
                    get_gravatar_url, googlemap_address_query, query_mongo)
from models import NameAlias
from django.http import HttpResponse


def index(request):
    context= {'npi_lookup_form': ProviderLookupForm()}
    return render(request, 'providerregistry/index.html', context)




def provider_lookup(request):
    
    context = {'name':"Provider Lookup",
               'subname':"by NPI"}
    
    if request.method == 'POST':
        form = ProviderLookupForm(request.POST)
        if form.is_valid():        
            number = form.save()
            return HttpResponseRedirect(reverse('provider_profile', args=(number,)))
        
        else:
            context.update({"form": form})
            return render(request, 'providerregistry/generic/bootstrapform.html', context)
    
    #this is a GET
    context.update({'form': ProviderLookupForm()})
    return render(request, 'providerregistry/generic/bootstrapform.html', context)


def provider_profile(request, number):
    if check_if_resource_exists(number) != 200:
        return render(request, 'providerregistry/404.html', {})
    
    random_background = "%s.jpg" % (random.randrange(1,27)) 
    provider          = get_resource(number)
    basic             = provider.get("basic", {})
    
    #Get Gravatar URL
    gravatar_email    = basic.get('gravatart_email', "")
    gravatar_url      = get_gravatar_url(hash_gravatar_email(gravatar_email))
    
    #Get Google q
    addresses     = provider.get("addresses", [])
    qooglemap_q = ""
    location = {}
    for a in addresses:
        if a.get("address_purpose", "")=="LOCATION":
            location = a
    
    googlemap_q = googlemap_address_query(address_1 = location.get("address_1", ""),
                                          address_2 = location.get("address_2", ""),
                                          city = location.get("city", ""),
                                          state = location.get("state", ""),
                                          zipcode = location.get("zip", ""),
                                          )

    context = { "enumeration":        provider,
                "random_bg_image": random_background,
                "gravatar_url": gravatar_url,
                "googlemap_q": googlemap_q,
                "PROVIDER_STATIC_HOST": settings.PROVIDER_STATIC_HOST
                }
 
    return render(request, 'providerregistry/stylish-portfolio.html', context)

def provider_details(request, number):
    if check_if_resource_exists(number) != 200:
        return render(request, 'providerregistry/404.html', {})
    
    provider          = get_resource(number)
    basic             = provider.get("basic", {})
    random_background = "%s.jpg" % (random.randrange(1,27)) 

    
    #Get Gravatar URL
    gravatar_email    = basic.get('gravatart_email', "")
    gravatar_url      = get_gravatar_url(hash_gravatar_email(gravatar_email))


    context = { "enumeration":        provider,
                "random_bg_image": random_background,
                "gravatar_url": gravatar_url,
                "PROVIDER_STATIC_HOST": settings.PROVIDER_STATIC_HOST,
                }
 
    return render(request, 'providerregistry/details.html', context)
    
    

def provider_search(request):
    name = "Search For Health Providers"
    
    if request.method == 'POST':
        form = ProviderSearchForm(request.POST)
        if form.is_valid():        
            query = form.save()
            display = form.cleaned_data.get("display")
            if display == "GALLERY": 
                gallery_results = reverse('search_results_gallery') + "?" + urllib.urlencode(query)
                return HttpResponseRedirect(gallery_results)
            else:
                table_results = reverse('search_results_table') + "?" + urllib.urlencode(query)
                return HttpResponseRedirect(table_results)
                
        else:
            context = {"name":name,"form": form}
            return render(request, 'providerregistry/generic/bootstrapform.html', context)
    
    #this is a GET
    context= {"name":name,'form': ProviderSearchForm()}
    return render(request, 'providerregistry/generic/bootstrapform.html', context)


def search_results_table(request, skip=0, limit=100):
    name = "Table Results"
    page_limit=100
    query = {}

    for k,v in request.GET.items():
        if k not in ('skip', 'limit', 'regex'):
            if k == "basic.first_name" and request.GET.get("regex") != "True":
                if NameAlias.objects.filter(name=v).exists():
                    #name is in alias list
                    
                    aliases = NameAlias.objects.filter(name=v)
                    alist =[v,]
                    for a in aliases:
                        alist.append(a.alias)
                    query[k] = {"$in": alist }
                    #print "QUERY", query
 
            else:
                #First name not given
                query[k]=v
        if k =='skip':
            skip=int(v)
    
    
    if request.GET.get('regex')=="True":
            regex_query = {}
            for k,v in request.GET.items():

                if k not in ('skip', 'limit', 'regex'):
                    if k != "addresses.state":
                        regex_query[k] = {"$regex": v}
                    else:
                        regex_query[k] = v
            query = regex_query
    
    
    #only get Active results
    query["basic.status"]="A"
        
    #query_mongo
    results = query_mongo(database_name="nppes",
                          collection_name="pjson",
                          query=query,
                          skip=skip, limit=limit) 
    reg_url = reverse('search_results_gallery') + "?" + urllib.urlencode(request.GET.items())
    table_url = reverse('search_results_table') + "?" + urllib.urlencode(request.GET.items())    
        
    context= {"name":name,
              "results":results["results"][:page_limit],
              "reg_url":reg_url,
              "table_url":table_url,
              "skip":skip, "limit":limit}
    
    return render(request, 'providerregistry/search-results-table.html', context)


def search_results_gallery(request, skip=0, limit=20):
    name = "Gallery Results"
    page_limit=12
    query ={}
    for k,v in request.GET.items():
        if k not in ('skip', 'limit', 'regex'):
            if k == "basic.first_name" and request.GET.get("regex") != "True":
                #If there is an alias for the name...
                if NameAlias.objects.filter(name=v).exists():
                    #name is in alias list
                    aliases = NameAlias.objects.filter(name=v)
                    alist =[v,]
                    for a in aliases:
                        alist.append(a.alias)
                    query[k] = {"$in": alist }
                
            else:
                #First name not given
                query[k]=v
        if k =='skip':
            skip=int(v)
        
        
        #if the find partial matches is true then rework query.
        if request.GET.get('regex')=="True":
            regex_query = {}
            for k,v in request.GET.items():

                if k not in ('skip', 'limit', 'regex'):
                    if k != "addresses.state":
                        regex_query[k] = {"$regex": v}
                    else:
                        regex_query[k] = v
            query = regex_query
            
        
        
            
    #only get Active results
    query["basic.status"]="A"
    #print query
    #query_mongo
    results = query_mongo(database_name="nppes", collection_name="pjson",
                          query=query, skip=skip, limit=limit) 
    
    reg_url = reverse('search_results_gallery') + "?" + urllib.urlencode(request.GET.items())
    table_url = reverse('search_results_table') + "?" + urllib.urlencode(request.GET.items())    
    context= {"name":name,"results":results["results"][:page_limit],
              "reg_url":reg_url,
              "table_url":table_url,
              "skip":skip, "limit":limit
              }
    return render(request, 'providerregistry/search-results.html', context)
