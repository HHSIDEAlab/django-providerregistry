""" test_views.py 
"""
import unittest
import urllib

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from ..forms import ProviderLookupForm,ProviderSearchForm

class RegistryIndex_TestCase(TestCase):
    """ Test the registry_index page """
    def setUp(self):
        #self.client=Client()
        #self.client.login(username="alan",password="")
        self.url = reverse('registry_index')
        
    def test_RegistryIndexPage(self):
        """ Test the page responds """
        response = self.client.get(self.url)
        # Check response status code 
        self.assertEqual(response.status_code, 200)        

class ProviderLookup_TestCase(TestCase):
    """ Test the provider_lookup page """
    def setUp(self):
        #self.client=Client()
        #self.client.login(username="alan",password="")
        self.url = reverse('provider_lookup')
        self.good_npi_number = '1508867359'
        self.bad_npi_number = '0000111123'
        
    def test_page(self):
        """ Test the page responds """
        response = self.client.get(self.url)
        #print response.content
        # Check response status code 
        self.assertEqual(response.status_code, 200)        

    def test_lookup_bad_number_length(self):
        response = self.client.post(self.url, {'number':'123456789012'})
        #print response.content
        # Check response status code 
        self.assertEqual(response.status_code, 200)
        self.assertContains( response, 'This number must be 10 digits long.')

    def test_lookup_bad_number_type(self):
        response = self.client.post(self.url, {'number':'123456789A'})
        #print response.content
        # Check response status code 
        self.assertEqual(response.status_code, 200)
        self.assertContains( response, 'You must supply a number containing exactly 10 digits.')

    def test_lookup_good_number(self):
        response = self.client.post(self.url, {'number': str(self.good_npi_number)})
        # Check response status code 
        self.assertEqual(response.status_code, 200)
        # TBD - Should add more checks on a successful NPI lookup

    #@unittest.skip('Skipping lookup bad number')
    def test_lookup_bad_number(self):
        response = self.client.post(self.url, {'number': str(self.bad_npi_number)})
        # Check response status code 
        self.assertEqual(response.status_code, 200)
        self.assertContains( response, "This enumeration number is not in the public registry.")

class ProviderProfile_TestCase(TestCase):
    """ Test the provider_lookup page """

    def setUp(self):
        #self.client=Client()
        #self.client.login(username="alan",password="")
        #self.url = reverse('provider_profile')
        self.good_npi_number = '1508867359'
        self.bad_npi_number = '0000111123'
        
    def test_good_profile(self):
        """ Test the page responds """
        response = self.client.get('/registry/provider-profile/%s' % self.good_npi_number)
        #print response.content
        # Check response status code 
        self.assertEqual(response.status_code, 200)        

    def test_bad_profile(self):
        response = self.client.get('/registry/provider-profile/%s' % self.bad_npi_number)
        #print response.content
        # Check response status code 
        self.assertEqual(response.status_code, 200)        

class ProviderSearch_TestCase(TestCase):
    """ Test the registry_index page """

    def setUp(self):
        #self.client=Client()
        #self.client.login(username="alan",password="")
        self.url = reverse('provider_search')
        
    def test_page(self):
        """ Test the page responds """
        response = self.client.get(self.url)
        # Check response status code 
        self.assertEqual(response.status_code, 200)        

    def test_search_all_NPI_1(self):
        """ Test the page responds """
        data = { u'enumeration_type' : u'NPI-1', 'basic.search': 'A'}
        response = self.client.post(self.url, data)
        #print response.content
        # Check response status code 
        self.assertEqual(response.status_code, 200)        

    def test_search_all_NPI_2_gallery(self):
        """ Test the page responds """
        data = { u'enumeration_type' : u'NPI-2', 'basic.search': 'A', 'display' : 'GALLERY'}
        resp = self.client.post(self.url, data)
        #print response.content
        # Check response status code 
        self.assertEqual(resp.status_code, 302) 
        #resp2 = self.client.post(reverse('search_results_gallery'), data)
        ##print response.content
        ## Check response status code 
        #self.assertEqual(resp.status_code, 302)        

    def test_search_all_NPI_2_table(self):
        """ Test the page responds """
        data = { u'enumeration_type' : u'NPI-2', 'basic.search': 'A', 'display' : 'TABLE'}
        resp = self.client.post(self.url, data)
        #print response.content
        # Check response status code 
        self.assertEqual(resp.status_code, 302) 
        #resp2 = self.client.post(reverse('search_results_gallery'), data)
        ##print response.content
        ## Check response status code 
        #self.assertEqual(resp.status_code, 302)        

class SearchResultsTable_TestCase(TestCase):
    """ Test the gistry_index page """
    def setUp(self):
        #self.client=Client()
        #self.client.login(username="alan",password="")
        self.url = reverse('search_results_table')
        self.display = 'TABLE'
        self.skip = '100'
        
    def test_search_all_NPI_2(self):
        data = { 'enumeration_type' : 'NPI-2', 'display' : self.display}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 
        
    def test_search_all_NPI_2_skip_100(self):
        data = { 'enumeration_type' : 'NPI-2', 'display' : self.display}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + '?skip=%s&' % self.skip + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 

    def test_search_first_name(self):
        data = { 'first_name' : 'sandy', 'display' : self.display}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 

    def test_search_find_partial_matches(self):
        data = { 'first_name' : 'medical', 'display' : self.display, 'find_partial_matches' : True}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 

    def test_search_find_partial_matches_with_state(self):
        data = { 'first_name' : 'medical', 'display' : self.display, 'find_partial_matches' : True, 'state' : 'NY'}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 

class SearchResultsGallery_TestCase(TestCase):
    """ Test the gistry_index page """
    def setUp(self):
        #self.client=Client()
        #self.client.login(username="alan",password="")
        self.url = reverse('search_results_gallery')
        self.display = 'GALLERY'
        self.skip = '12'
        
    def test_search_all_NPI_2(self):
        data = { 'enumeration_type' : 'NPI-2', 'display' : self.display}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 
        
    def test_search_all_NPI_2_skip_100(self):
        data = { 'enumeration_type' : 'NPI-2', 'display' : self.display}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + '?skip=%s&' % self.skip + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 

    def test_search_first_name(self):
        data = { 'first_name' : 'sandy', 'display' : self.display}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        table_results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(table_results)
        self.assertEqual(resp.status_code, 200) 

    def test_search_find_partial_matches(self):
        data = { 'first_name' : 'medical', 'display' : self.display, 'find_partial_matches' : True}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 

    def test_search_find_partial_matches_with_state(self):
        data = { 'first_name' : 'medical', 'display' : self.display, 'find_partial_matches' : True, 'state' : 'NY'}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        results = self.url + "?" + urllib.urlencode(query)
        resp = self.client.get(results)
        self.assertEqual(resp.status_code, 200) 
