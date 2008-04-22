"""Custom EvalException support

Provides template engine HTML error formatters for the Template tab of
EvalException.

"""
try:
    import mako.exceptions
except ImportError:
    mako = None

__all__ = []

# Legacy support for < 0.9.7 projects
error_template = None

def myghty_html_data(exc_value):
    """Format a Myghty exception as HTML"""
    if hasattr(exc_value, 'htmlformat'):
        return exc_value.htmlformat()[333:-14]
    if hasattr(exc_value, 'mtrace'):
        return exc_value.mtrace.htmlformat()[333:-14]

template_error_formatters = [myghty_html_data]


if mako:
    def mako_html_data(exc_value):
        """Format a Mako exception as HTML"""
        if isinstance(exc_value, (mako.exceptions.CompileException,
                                  mako.exceptions.SyntaxException)):
            return mako.exceptions.html_error_template().render(full=False,
                                                                css=False)
    template_error_formatters.insert(0, mako_html_data)
