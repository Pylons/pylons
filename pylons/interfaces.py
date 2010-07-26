from repoze.bfg.interfaces import IAfterTraversal
from repoze.bfg.interfaces import INewRequest
from repoze.bfg.interfaces import INewResponse
from repoze.bfg.interfaces import IWSGIApplicationCreatedEvent
from zope.interface import Interface

# internal interfaces

class ITemplateGlobals(Interface):
    """ Event issued when Pylons is done loading globals """
