from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

version = "0.9.4"

setup(
    name="Pylons",
    version=version,
    description='Pylons Web Framework',
    long_description="""
Pylons
======

The Pylons web framework is aimed at making webapps and large programmatic website
development in Python easy. Several key points:

* A framework to make writing web applications in Python easy

* Inspired by Rails and TurboGears

* Utilizes a minimalist, component-based philosophy that makes it easy to expand on

* Harness existing knowledge about Python

Knowing Python makes Pylons easy
---------------------------------

Pylons makes it easy to expand on your knowledge of Python to master Pylons for web
development. Using a MVC style dispath, Python knowledge is used at various levels:

* The Controller is just a basic Python class, called for each request. Customizing the
  response is as easy as overriding __call__ to make your webapp work how you want.

* Myghty templating compiles directly to Python byte-code for speed and utilizes Python
  for template control rather than creating its own template syntax for "for, while, etc"

Current Status
---------------

Pylons %s described on this page is stable.

There is also an 
unstable `develoment version <http://pylonshq.com/svn/Pylons/trunk#egg=Pylons-dev>`_ 
of Pylons.

Download and Installation
-------------------------

Pylons can be installed with `Easy Install 
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_ by typing::

    > easy_install Pylons 

Dependant packages are automatically installed from 
the `Pylons download page <http://pylonshq.com/download/>`_ .


"""%version,
    keywords='web wsgi framework sqlalchemy formencode myghty templates buffet',
    license='BSD',
    author='Ben Bangert, James Gardner, Philip Jenvey',
    author_email='ben@groovie.org',
    url='http://www.pylonshq.com/',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "Routes>=1.6.1", "WebHelpers>=0.2.2", "Beaker>=0.6.2",
        "Paste>=1.1.1", "PasteDeploy>=1.0", "PasteScript>=1.0",
        "Myghty>=1.1", "FormEncode>=0.6", "simplejson>=1.4", "nose>=0.9.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    extras_require = {
        'pudge': ["docutils>=0.4", "elementtree>=1.2.6", "kid>=0.9", 
            "pudge>=0.1.2", "buildutils>=0.1.2",],
        'test': ["py>=0.8.0_alpha2"],
        'cheetah':["Cheetah>=1.0", "TurboCheetah>=0.9.5"],
        'kid':["kid>=0.9", "TurboKid==dev,>=0.9.1dev"],
        'genshi':["Genshi>=0.3.6"],
        'full':[
            "docutils>=0.4", "elementtree>=1.2.6",
            "pudge>=0.1.2", "buildutils>=0.1.2",
            "py>=0.8.0_alpha2",
            "Cheetah>=1.0", "TurboCheetah>=0.9.5",
            "kid>=0.9", "TurboKid==dev,>=0.9.1dev",
        ],
    },
    entry_points="""
    [paste.paster_command]
    controller=pylons.commands:ControllerCommand
    shell=pylons.commands:ShellCommand

    [paste.paster_create_template]
    pylons=pylons.util:PylonsTemplate
    pylons_minimal=pylons.util:MinimalPylonsTemplate
    
    [python.templating.engines]
    pylonsmyghty = pylons.templating:MyghtyTemplatePlugin
    """,
)
