#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written  By Alan Viars
from django import forms
from django.utils.translation import ugettext_lazy as _
from utils import  check_if_resource_exists, get_resource
from localflavor.us.us_states import US_STATES
from pdt import vnpi
US_STATE_CHOICES = list(US_STATES)

US_STATE_CHOICES.insert(0,('', 'Any') )
US_STATE_CHOICES.extend(
    [('AS', 'American Samoa'),
    ('FM',  'Micronesia, Federated States of'),
    ('GU',  'Guam'),
    ('MH',  'Marshall Islands'),
    ('MP',  'Mariana Islands, Northern'),
    ('PR',  'Puerto Rico'),
    ('PW',  'Palau'),
    ('VI',  'Virgin Islands'),
    ('ZZ',  'Other Country')])



class ProviderLookupForm(forms.Form):
    number   = forms.CharField(required=True, label= "NPI Number")
    
    required_css_class = 'required'
    
    def clean_number(self):
        number = self.cleaned_data["number"]
        
        #check if the number meets our criteria
        if len(number) != 10:
            raise forms.ValidationError("This number must be 10 digits long.")

        try:
            number = int(number)
        except ValueError:
            raise forms.ValidationError("You must supply a number containing exactly 10 digits.")
        
        if not vnpi.verify_npi(number):
	    raise forms.ValidationError("This enumeration does not appear to be a valid NPI number.")

        http_status = check_if_resource_exists(number)
        
        if http_status == 403:
            raise forms.ValidationError("This enumeration number is not in the public registry.")
        
        if http_status == 500:
            raise forms.ValidationError("The public registry appears to be offline. Please ty again later.")
        
        if http_status == 000:
            raise forms.ValidationError("The public registry appears to be offline. Please ty again later.")
        
        return number
        
    
    def save(self):
        number = self.cleaned_data["number"]
        return number
    

ENUMERATION_CHOICES = (("", "Any"),("NPI-1","Individual"),("NPI-2", "Organization"))

DISPLAY_CHOICES = (("GALLERY", "Gallery"),("TABLE","Table"))


class ProviderSearchForm(forms.Form):
    
    enumeration_type        = forms.ChoiceField(required=False,
                                           choices = ENUMERATION_CHOICES,
                                           initial="")
    
    organization_name   = forms.CharField(required=False,
                            help_text ="Organization name applies to organizations only.")
    
    first_name          = forms.CharField(required=False,
                                           help_text ="First name applies to individuals only.")
    last_name           = forms.CharField(required=False,
                                          help_text ="Last name applies to individuals only.")
    doing_business_as   = forms.CharField(required=False,
                            help_text ="Doing Business As can apply to an organization or an individual sole proprietor.")
    city                = forms.CharField(required=False)
    state               = forms.ChoiceField(required=False, choices =US_STATE_CHOICES,  )
    zip_code            = forms.CharField(required=False)
    find_partial_matches  = forms.BooleanField(required=False, initial = False,
                             help_text ="Check this box to find partial matches.")
    direct_address      = forms.EmailField(required=False,
                                help_text ="A Direct email address, or other endpoint, for an organization or individual.")
    display             = forms.ChoiceField(required=True, choices = DISPLAY_CHOICES,
                            initial="GALLERY",
                            help_text = "Display search results in gallery or table format.",
                            label="Results Display Options")               
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(ProviderSearchForm, self).__init__(*args, **kwargs)


    
    def save(self):
	d = { "enumeration_type": self.cleaned_data.get("enumeration_type"),
	     "basic.first_name": self.cleaned_data.get("first_name"),
             "basic.last_name": self.cleaned_data.get("last_name"),
             "basic.organization_name": self.cleaned_data.get("organization_name"),
             "basic.doing_business_as" :self.cleaned_data.get("doing_business_as"),           
             "addresses.city"     :self.cleaned_data.get("city"),        
             "addresses.state"   :self.cleaned_data.get("state"),         
	     "addresses.zip"    :self.cleaned_data.get("zip_code"),
	     "affiliations.endpoint"  :self.cleaned_data.get("direct_address"),
             "regex"  : self.cleaned_data.get("find_partial_matches"),
            }
        cleaned_query = {}
        for k,v in d.items():
        
            if v:
               if hasattr(v, 'upper'):
                   cleaned_query[k] = str(v.upper())
               else:
                   cleaned_query[k] = v
        return cleaned_query

    