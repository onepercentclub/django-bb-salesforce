#!/usr/bin/env python
import os
import setuptools
import bb_salesforce

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="django-bb-salesforce",
    version=bb_salesforce.__version__,
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='None',
    description='Salesforce synchronisation for Bluebottle',
    long_description=README,
    url="http://onepercentclub.com",
    author="1%Club Developers",
    author_email="devteam@onepercentclub.com", 
    install_requires=[
        'Django>=1.6.8',
        'django-salesforce==0.5',
    ],
    tests_require=[
        'factory-boy==2.3.1',
        'django-choices',
        'django-extensions==1.1.1',
        'django-nose==1.4',
        'django-setuptest==0.1.4',
        'surlex',
        'mock'
    ],
    test_suite = "runtests.runtests",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: None', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]

)

