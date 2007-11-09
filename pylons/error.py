"""Custom error middleware subclasses, used for error theme

These error middleware sub-classes are used mainly to provide skinning
for the Paste middleware. In the future this entire module will likely
be little more than a template, as Paste will get the skinning functionality.

The only additional thing besides skinning supplied, is the Template traceback
information.
"""
import logging

__all__ = []

log = logging.getLogger(__name__)

class InvalidTemplate(Exception):
    pass


def myghty_html_data(exc_value):
    if hasattr(exc_value, 'htmlformat'):
        return exc_value.htmlformat()[333:-14]
    if hasattr(exc_value, 'mtrace'):
        return exc_value.mtrace.htmlformat()[333:-14]


template_error_formatters = [myghty_html_data]

error_template = None

try:
    import mako.exceptions
except ImportError:
    pass
else:
    def mako_html_data(exc_value):
        if isinstance(exc_value, (mako.exceptions.CompileException, mako.exceptions.SyntaxException)):
            return mako.exceptions.html_error_template().render(full=False,
                                                                css=False)
    
    template_error_formatters.insert(0,mako_html_data)
