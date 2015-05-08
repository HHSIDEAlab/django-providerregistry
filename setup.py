import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-providerregistry',
    version='0.5.5',
    packages=['providerregistry'],
    include_package_data=True,
    license='Public Domain',  
    description='A simple Django application that provides a UI and RESTFul API for read only access to NPPES data.',
    long_description=README,
    url='https://github.com/hhsidealab/django-providerregistry',
    author='Alan Viars',
    author_email='alan.viars@cms.hhs.gov',
    install_requires=[
        'pymongo', 'requests', 'django-localflavor',
        'django-bootstrap-form', 'django-djmongo'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

