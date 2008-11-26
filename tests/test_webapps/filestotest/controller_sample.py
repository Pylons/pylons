import datetime

from projectname.lib.base import *
import projectname.lib.helpers as h
from pylons import h as deprecated_h
from pylons import request, response, session
from pylons import tmpl_context as c
from pylons import app_globals as g
from pylons.decorators import rest
from pylons.i18n import _, get_lang, set_lang, LanguageError
from pylons.templating import render as old_render, render_genshi, \
    render_jinja2, render_response
from pylons.controllers.util import abort, redirect_to, url_for

class SampleController(BaseController):
    def index(self):
        return 'basic index page'
    
    def session_increment(self):
        session.setdefault('counter', -1)
        session['counter'] += 1
        session.save()
        return 'session incrementer'
    
    def globalup(self):
        return g.message
    
    def global_store(self, id=None):
        if id:
            g.counter += int(id)
        return str(g.counter)
    
    def myself(self):
        return h.url_for()
    
    def myparams(self):
        return str(request.params)
    
    def testdefault(self):
        c.test = "This is in c var"
        return render_genshi('testgenshi.html')

    def testdefault_legacy(self):
        c.test = "This is in c var"
        return old_render('testgenshi')
        
    def test_template_caching(self):
        return render_response('/test_mako.html', cache_expire='never')
    
    def test_only_post(self):
        return 'It was a post!'
    test_only_post = rest.dispatch_on(GET='test_only_get')(rest.restrict('POST')(test_only_post))
    
    def test_only_get(self):
        return 'It was a get!'
    test_only_get = rest.restrict('GET')(test_only_get)
    
    def impossible(self):
        return 'This should never be shown'
    impossible = rest.restrict('POST')(rest.dispatch_on(POST='test_only_post')(impossible))

    def testjinja2(self):
        c.test = "This is in c var"
        c.now = datetime.datetime.now
        return render_jinja2('testjinja2.html')

    def set_lang(self):
        return self._set_lang(_)

    def set_lang_pylonscontext(self, pylons):
        return self._set_lang(lambda *args: pylons.translator.ugettext(*args))

    def _set_lang(self, gettext):
        lang = request.GET['lang']
        try:
            set_lang(lang)
        except (LanguageError, IOError), e:
            resp_unicode = gettext('Could not set language to "%(lang)s"') % {'lang': lang}
        else:
            session['lang'] = lang
            session.save()
            resp_unicode = gettext('Set language to "%(lang)s"') % {'lang': lang}
        return resp_unicode

    def i18n_index(self):
        locale_list = request.languages
        set_lang(request.languages)
        return unicode(_('basic index page'))

    def no_lang(self):
        set_lang(None)
        response.write(_('No language'))
        set_lang([])
        response.write(_('No languages'))
        return ''
        
    def deprecated_h(self):
        return '%s is %s' % (h.url_for(), deprecated_h.url_for())
