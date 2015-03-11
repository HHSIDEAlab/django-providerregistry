""" test_forms.py 
"""
import urllib
from django.test import TestCase
from django.core.urlresolvers import reverse
from ..forms import ProviderLookupForm,ProviderSearchForm

class ProviderLookupForm_TestCase(TestCase):
    def setUp(self):
        self.good_npi_number = '1508867359'
        self.bad_npi_number = '0000111123'

    def test_lookup_number_length(self):
        data = {'number': '12345678'}
        form = ProviderLookupForm(data)
        self.assertFalse(form.is_valid())

    def test_lookup_number_type(self):
        data = {'number': '1234567A'}
        form = ProviderLookupForm(data)
        self.assertFalse(form.is_valid())
        
    def test_lookup_valid(self):
        data = {'number': self.good_npi_number}
        form = ProviderLookupForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        
    def test_lookup_invalid(self):
        data = {'number': self.bad_npi_number}
        form = ProviderLookupForm(data)
        self.assertFalse(form.is_valid())

class ProviderSearchForm_TestCase(TestCase):
    def setUp(self):
        self.good_npi_number = '1508867359'
        self.bad_npi_number = '0000111123'

    def test_search_form(self):
        form = ProviderSearchForm()
        self.assertFalse(form.is_valid())

    def test_search_all_NPI_1(self):
        data = { u'enumeration_type' : u'NPI-1', 'basic.search': 'A', 'display' : 'GALLERY'}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        form.save()

    def test_search_all_NPI_2_gallery(self):
        data = { u'enumeration_type' : u'NPI-2', 'basic.search': 'A', 'display' : 'GALLERY'}
        form = ProviderSearchForm(data)
        self.assertTrue(form.is_valid(), 'form is not valid')
        query = form.save()
        gallery_results = reverse('search_results_gallery') + "?" + urllib.urlencode(query)
        resp = self.client.get(gallery_results)
