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

   

2. Pip install django-providerregistry and prerequisites::

    pip install pymongo django-providerregistry


3. Add "providerregistry" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'providerregistry',
    )

4. Include the direct URLconf in your project urls.py like this::

    url(r'^registry/', include('providerregistry.urls')),

5. Create the models that contain informationto help with searching::

    python manage.py syncdb

6. Collect static content::

    python manage.py collectstatic

7. Start the development server::

    python manage.py runserver

8. Point your browser to htpp://127.0.0.1:8000/registry


