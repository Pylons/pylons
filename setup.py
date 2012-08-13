import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

version = '1.0.1'

tests_require = ['nose', 'Jinja2>=2.2.1']
if not sys.platform.startswith('java'):
    tests_require.extend(['Genshi', 'coverage>=2.85'])

setup(
    name="Pylons",
    version=version,
    description='Pylons Web Framework',
    long_description="""
Pylons
======

The Pylons web framework is designed for building web applications and
sites in an easy and concise manner. They can range from as small as a
single Python module, to a substantial directory layout for larger and
more complex web applications.

Pylons comes with project templates that help boot-strap a new web
application project, or you can start from scratch and set things up
exactly as desired.


Example `Hello World`
---------------------

..

    from paste.httpserver import serve
    from pylons import Configurator, Response

    class Hello(object):
        def __init__(self, request):
            self.request = request

        def index(self):
            return Response(body="Hello World!")


    if __name__ == '__main__':
        config = Configurator()
        config.begin()
        config.add_handler('home', '/', handler=Hello, action='index')
        config.end()
        serve(config.make_wsgi_app(), host='0.0.0.0')


Core Features
-------------

* A framework to make writing web applications in Python easy

* Utilizes a minimalist, component-based philosophy that makes it easy to
  expand on

* Harness existing knowledge about Python

* Extensible application design

* Fast and efficient, an incredibly small per-request call-stack providing
  top performance

* Uses existing and well tested Python packages


Current Status
--------------

Pylons 1.0 series is stable and production ready. The Pylons Project now
maintains the Pyramid web framework for future development. Pylons 1.0 users
should strongly consider using it for their next project.


Download and Installation
-------------------------

Pylons can be installed with `Easy Install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_ by typing::

    > easy_install Pylons

Dependant packages are automatically installed from
the `Pylons download page <http://pylonshq.com/download/>`_ .


Development Version
-------------------

Pylons development uses the Mercuial distributed version control system (DVCS)
with BitBucket hosting the main repository here:

    `Pylons Bitbucket repository <https://github.com/Pylons/pylons>`_


""",
    keywords='web wsgi lightweight framework sqlalchemy formencode mako templates',
    license='BSD',
    author='Ben Bangert, Philip Jenvey, James Gardner',
    author_email='ben@groovie.org, pjenvey@underboss.org',
    url='http://www.pylonshq.com/',
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=tests_require,
    install_requires=[
        "Routes>=1.12.3", "WebHelpers>=0.6.4", "Beaker>=1.5.4",
        "Paste>=1.7.5.1", "PasteDeploy>=1.5.0", "PasteScript>=1.7.4.2",
        "FormEncode>=1.2.4", "simplejson>=2.2.1", "decorator>=3.3.2",
        "nose>=1.1.2", "Mako>=0.5.0", "WebError>=0.10.3",
        "WebTest>=1.3.1", "Tempita>=0.5.1", "MarkupSafe>=0.15",
        "WebOb>=1.1.1",
    ],
    dependency_links=[
        "http://www.pylonshq.com/download/1.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Framework :: Pylons",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    extras_require={
        'genshi': ['Genshi>=0.6'],
        'jinja2': ['Jinja2'],
    },
    entry_points="""
    [paste.paster_command]
    controller = pylons.commands:ControllerCommand
    restcontroller = pylons.commands:RestControllerCommand
    routes = pylons.commands:RoutesCommand
    shell = pylons.commands:ShellCommand

    [paste.paster_create_template]
    pylons = pylons.util:PylonsTemplate
    pylons_minimal = pylons.util:MinimalPylonsTemplate

    [paste.filter_factory]
    debugger = pylons.middleware:debugger_filter_factory

    [paste.filter_app_factory]
    debugger = pylons.middleware:debugger_filter_app_factory
    """,
)
