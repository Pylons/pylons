from zope.interface import implements

from pylons.interfaces import ITemplateGlobals

class TemplateGlobals(object):
    """ An instance of this class is emitted as an :term:`event`
    whenever :mod:`pylons` has finished setting up the template
    globals. The instance has an attribute, ``system``, which is a
    dict of all the globals that will be added to the template's
    global namespace during rendering.
    
    """
    implements(ITemplateGlobals)
    def __init__(self, system):
        self.system = system
