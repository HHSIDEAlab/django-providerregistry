===================================================
django-providerregistry - The NPPES Public Registry
===================================================

django-providerregistry is a simple Django application that provides UI
and a RESTFul API for read-only access to public information contained
within NPPES (a.k.a. the NPI database).

Detailed documentation for using the API is in the "docs" directory. 
Installation instructions are below.

Quick Start
-----------

1. Install MongoDB according to http://docs.mongodb.org/manual/installation/

2. Download and import the NPPES Public Data into MongoDB.

You can use the script "loadnppes.py", part of to do this for you in one big
step.  loadnppes.py is part of the provider-data-tools package.
   
3. Pip install django-providerregistry and prerequisites::

    pip install pymongo django-providerregistry


4. Add "providerregistry" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'providerregistry',
    )

5. Include the direct URLconf in your project urls.py like this::

    url(r'^registry/', include('providerregistry.urls')),

6. Create the models that contain informationto help with searching::

    python manage.py syncdb

7. Collect static content::

    python manage.py collectstatic

8. Start the development server::

    python manage.py runserver

9. Point your browser to htpp://127.0.0.1:8000/registry


