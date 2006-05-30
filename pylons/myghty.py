"""Myghty extension module"""

from formencode import htmlfill

def formfill(m, defaults, errors):
    form = m.content()
    m.write(htmlfill.render(form, defaults, errors))
