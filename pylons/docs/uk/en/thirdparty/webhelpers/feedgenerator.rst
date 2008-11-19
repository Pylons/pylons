:mod:`~webhelpers.feedgenerator` -- Feed generator
===================================================

The feed generator is intended for use in controllers, and generates an
output stream. Currently the following feeds can be created by imported the
appropriate class:

* RssFeed
* RssUserland091Feed
* Rss201rev2Feed
* Atom1Feed

All of these format specific Feed generators inherit from the 
:meth:`~webhelpers.feedgenerator.SyndicationFeed` class.

Example controller method::
    
    import logging

    from pylons import request, response, session
    from pylons import tmpl_context as c
    from pylons.controllers.util import abort, redirect_to, url_for
    from webhelpers.feedgenerator import Atom1Feed

    from helloworld.lib.base import BaseController, render

    log = logging.getLogger(__name__)

    class CommentsController(BaseController):

        def index(self):
            feed = Atom1Feed(
                title=u"An excellent Sample Feed",
                link=url_for(),
                description=u"A sample feed, showing how to make and add entries",
                language=u"en",
            )
            feed.add_item(title="Sample post", 
                          link=u"http://hellosite.com/posts/sample", 
                          description="Testing.")
            response.content_type = 'application/atom+xml'
            return feed.writeString('utf-8')


Module Contents
---------------

.. currentmodule:: webhelpers.feedgenerator

.. autoclass:: SyndicationFeed
    :members:
    
    .. automethod:: __init__
.. autoclass:: Enclosure
    :members:
.. autoclass:: RssFeed
    :members:
.. autoclass:: RssUserland091Feed
    :members:
.. autoclass:: Rss201rev2Feed
    :members:
.. autoclass:: Atom1Feed
    :members:
.. autofunction:: rfc2822_date
.. autofunction:: rfc3339_date
.. autofunction:: get_tag_uri

