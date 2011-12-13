from repoze.bfg.encode import urlencode
from repoze.bfg.threadlocal import get_current_registry
from repoze.bfg.url import _join_elements

from pylons.interfaces import IRoutesMapper


def route_url(route_name, request, *elements, **kw):
    try:
        reg = request.registry
    except AttributeError:
        reg = get_current_registry()  # b/c
    mapper = reg.getUtility(IRoutesMapper)

    route = mapper.routes.get(route_name)
    if route and 'custom_url_generator' in route.__dict__:
        route_name, request, elements, kw = route.custom_url_generator(
            route_name, request, *elements, **kw)
    anchor = ''
    qs = ''
    app_url = None

    if '_query' in kw:
        qs = '?' + urlencode(kw.pop('_query'), doseq=True)

    if '_anchor' in kw:
        anchor = kw.pop('_anchor')
        if isinstance(anchor, unicode):
            anchor = anchor.encode('utf-8')
        anchor = '#' + anchor

    if '_app_url' in kw:
        app_url = kw.pop('_app_url')

    path = mapper.generate(route_name, kw)  # raises KeyError if generate fails

    if elements:
        suffix = _join_elements(elements)
        if not path.endswith('/'):
            suffix = '/' + suffix
    else:
        suffix = ''

    if app_url is None:
        # we only defer lookup of application_url until here because
        # it's somewhat expensive; we won't need to do it if we've
        # been passed _app_url
        app_url = request.application_url

    return app_url + path + suffix + qs + anchor
