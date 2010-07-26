from zope.interface import Interface

# private interfaces

class ITemplateGlobals(Interface):
    """ Event issued when Pylons is done loading globals """
