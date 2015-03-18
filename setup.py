import os
from setuptools import setup
import reef_crawlable

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-bb-salesforce",
    version=bb_salesforce.__version__,
    packages=['bb_salesforce'],
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
        'django-nose==1.3',
        'django-setuptest==0.1.4',
        'mock'
    ],
    test_suite = "bb_salesforce.runtests.runtests",
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

