"""Render functions and helpers

Render functions and helpers
============================

:mod:`pylons.templating` includes several basic render functions,
:func:`render_mako`, :func:`render_genshi` and :func:`render_jinja2`
that render templates from the file-system with the assumption that
variables intended for the will be attached to :data:`tmpl_context`
(hereafter referred to by its short name of :data:`c` which it is
commonly imported as).

The default render functions work with the template language loader
object that is setup on the :data:`app_globals` object in the project's
:file:`config/environment.py`.

Usage
-----

Generally, one of the render functions will be imported in the
controller. Variables intended for the template are attached to the
:data:`c` object. The render functions return unicode (they actually
return :class:`~webhelpers.html.literal` objects, a subclass of
unicode).

.. admonition :: Tip
    
    :data:`tmpl_context` (template context) is abbreviated to :data:`c`
    instead of its full name since it will likely be used extensively
    and it's much faster to use :data:`c`. Of course, for users that
    can't tolerate one-letter variables, feel free to not import 
    :data:`tmpl_context` as :data:`c` since both names are available in
    templates as well.

Example of rendering a template with some variables::

    from pylons import tmpl_context as c
    from pylons.templating import render_mako as render

    from sampleproject.lib.base import BaseController

    class SampleController(BaseController):

        def index(self):
            c.first_name = "Joe"
            c.last_name = "Smith"
            return render('/some/template.mako')

And the accompanying Mako template:

.. code-block:: mako
    
    Hello ${c.first name}, I see your lastname is ${c.last_name}!

Your controller will have additional default imports for commonly used
functions.

Template Globals
----------------

Templates rendered in Pylons should include the default Pylons globals
as the :func:`render_mako`, :func:`render_genshi` and
:func:`render_jinja2` functions. The full list of Pylons globals that
are included in the template's namespace are:

- :term:`c` -- Template context object
- :term:`tmpl_context` -- Template context object
- :data:`config` -- Pylons :class:`~pylons.configuration.PylonsConfig`
  object (acts as a dict)
- :term:`app_globals` -- Project application globals object
- :term:`h` -- Project helpers module reference
- :data:`request` -- Pylons :class:`~pylons.controllers.util.Request`
  object for this request
- :data:`response` -- Pylons :class:`~pylons.controllers.util.Response`
  object for this request
- :class:`session` -- Pylons session object (unless Sessions are
  removed)
- :class:`url <routes.util.URLGenerator>` -- Routes url generator
  object
- :class:`translator` -- Gettext translator object configured for
  current locale
- :func:`ungettext` -- Unicode capable version of gettext's ngettext
  function (handles plural translations)
- :func:`_` -- Unicode capable gettext translate function
- :func:`N_` -- gettext no-op function to mark a string for
  translation, but doesn't actually translate

Configuring the template language
---------------------------------

The template engine is created in the projects 
``config/environment.py`` and attached to the ``app_globals`` (g)
instance. Configuration options can be directly passed into the
template engine, and are used by the render functions.

.. warning::

    Don't change the variable name on :data:`app_globals` that the
    template loader is attached to if you want to use the render_*
    functions that :mod:`pylons.templating` comes with. The render_*
    functions look for the template loader to render the template.

"""
import logging

from webhelpers.html import literal

import pylons

__all__ = ['render_genshi', 'render_jinja2', 'render_mako', 'render_response']

PYLONS_VARS = ['c', 'app_globals', 'config', 'h', 'render', 'request',
               'session', 'translator', 'ungettext', '_', 'N_']

log = logging.getLogger(__name__)

def pylons_globals():
    """Create and return a dictionary of global Pylons variables
    
    Render functions should call this to retrieve a list of global
    Pylons variables that should be included in the global template
    namespace if possible.
    
    Pylons variables that are returned in the dictionary:
        ``c``, ``h``, ``_``, ``N_``, config, request, response, 
        translator, ungettext, ``url``
    
    If SessionMiddleware is being used, ``session`` will also be
    available in the template namespace.
    
    """
    conf = pylons.config._current_obj()
    c = pylons.tmpl_context._current_obj()
    app_globals = conf.get('pylons.app_globals')
    pylons_vars = dict(
        c=c,
        tmpl_context=c,
        config=conf,
        app_globals=app_globals,
        h=conf.get('pylons.h'),
        request=pylons.request._current_obj(),
        response=pylons.response._current_obj(),
        url=pylons.url._current_obj(),
        translator=pylons.translator._current_obj(),
        ungettext=pylons.i18n.ungettext,
        _=pylons.i18n._,
        N_=pylons.i18n.N_
    )
    
    # If the session was overriden to be None, don't populate the session
    # var
    econf = pylons.config['pylons.environ_config']
    if 'beaker.session' in pylons.request.environ or \
        ('session' in econf and econf['session'] in pylons.request.environ):
        pylons_vars['session'] = pylons.session._current_obj()
    log.debug("Created render namespace with pylons vars: %s", pylons_vars)
    return pylons_vars


def cached_template(template_name, render_func, ns_options=(),
                    cache_key=None, cache_type=None, cache_expire=None,
                    **kwargs):
    """Cache and render a template
    
    Cache a template to the namespace ``template_name``, along with a
    specific key if provided.
    
    Basic Options
    
    ``template_name``
        Name of the template, which is used as the template namespace.
    ``render_func``
        Function used to generate the template should it no longer be
        valid or doesn't exist in the cache.
    ``ns_options``
        Tuple of strings, that should correspond to keys likely to be
        in the ``kwargs`` that should be used to construct the
        namespace used for the cache. For example, if the template
        language supports the 'fragment' option, the namespace should
        include it so that the cached copy for a template is not the
        same as the fragment version of it.
    
    Caching options (uses Beaker caching middleware)
    
    ``cache_key``
        Key to cache this copy of the template under.
    ``cache_type``
        Valid options are ``dbm``, ``file``, ``memory``, ``database``,
        or ``memcached``.
    ``cache_expire``
        Time in seconds to cache this template with this ``cache_key``
        for. Or use 'never' to designate that the cache should never
        expire.
    
    The minimum key required to trigger caching is
    ``cache_expire='never'`` which will cache the template forever
    seconds with no key.
    
    """
    # If one of them is not None then the user did set something
    if cache_key is not None or cache_expire is not None or cache_type \
        is not None:

        if not cache_type:
            cache_type = 'dbm'
        if not cache_key:
            cache_key = 'default'     
        if cache_expire == 'never':
            cache_expire = None
        namespace = template_name
        for name in ns_options:
            namespace += str(kwargs.get(name))
        cache = pylons.cache.get_cache(namespace, type=cache_type)
        content = cache.get_value(cache_key, createfunc=render_func, 
            expiretime=cache_expire)
        return content
    else:
        return render_func()


def render_mako(template_name, extra_vars=None, cache_key=None, 
                cache_type=None, cache_expire=None):
    """Render a template with Mako
    
    Accepts the cache options ``cache_key``, ``cache_type``, and
    ``cache_expire``.
    
    """    
    # Create a render callable for the cache function
    def render_template():
        # Pull in extra vars if needed
        globs = extra_vars or {}
        
        # Second, get the globals
        globs.update(pylons_globals())

        # Grab a template reference
        template = globs['app_globals'].mako_lookup.get_template(template_name)
        
        return literal(template.render_unicode(**globs))
    
    return cached_template(template_name, render_template, cache_key=cache_key,
                           cache_type=cache_type, cache_expire=cache_expire)


def render_mako_def(template_name, def_name, cache_key=None,
                    cache_type=None, cache_expire=None, **kwargs):
    """Render a def block within a Mako template
    
    Takes the template name, and the name of the def within it to call.
    If the def takes arguments, they should be passed in as keyword
    arguments.
    
    Example::
        
        # To call the def 'header' within the 'layout.mako' template
        # with a title argument
        render_mako_def('layout.mako', 'header', title='Testing')
    
    Also accepts the cache options ``cache_key``, ``cache_type``, and
    ``cache_expire``.
    
    """
    # Create a render callable for the cache function
    def render_template():
        # Pull in extra vars if needed
        globs = kwargs or {}
        
        # Second, get the globals
        globs.update(pylons_globals())

        # Grab a template reference
        template = globs['app_globals'].mako_lookup.get_template(
            template_name).get_def(def_name)
        
        return literal(template.render_unicode(**globs))
    
    return cached_template(template_name, render_template, cache_key=cache_key,
                           cache_type=cache_type, cache_expire=cache_expire)


def render_genshi(template_name, extra_vars=None, cache_key=None, 
                  cache_type=None, cache_expire=None, method='xhtml'):
    """Render a template with Genshi
    
    Accepts the cache options ``cache_key``, ``cache_type``, and
    ``cache_expire`` in addition to method which are passed to Genshi's
    render function.
    
    """
    # Create a render callable for the cache function
    def render_template():
        # Pull in extra vars if needed
        globs = extra_vars or {}
        
        # Second, get the globals
        globs.update(pylons_globals())

        # Grab a template reference
        template = globs['app_globals'].genshi_loader.load(template_name)
        
        return literal(template.generate(**globs).render(method=method,
                                                         encoding=None))
    
    return cached_template(template_name, render_template, cache_key=cache_key,
                           cache_type=cache_type, cache_expire=cache_expire,
                           ns_options=('method'), method=method)


def render_jinja2(template_name, extra_vars=None, cache_key=None, 
                 cache_type=None, cache_expire=None):
    """Render a template with Jinja2

    Accepts the cache options ``cache_key``, ``cache_type``, and
    ``cache_expire``.

    """    
    # Create a render callable for the cache function
    def render_template():
        # Pull in extra vars if needed
        globs = extra_vars or {}
        
        # Second, get the globals
        globs.update(pylons_globals())

        # Grab a template reference
        template = \
            globs['app_globals'].jinja2_env.get_template(template_name)

        return literal(template.render(**globs))

    return cached_template(template_name, render_template, cache_key=cache_key,
                           cache_type=cache_type, cache_expire=cache_expire)
