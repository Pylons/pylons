import datetime

from projectname.lib.base import *
try:
    import sqlalchemy as sa
    from projectname.model.meta import Session, metadata
    from projectname.model import Foo
    SQLAtesting = True
except:
    SQLAtesting = False
import projectname.lib.helpers as h
from pylons import request, response, session
from pylons import tmpl_context as c
from pylons import app_globals
from pylons.decorators import rest
from pylons.i18n import _, get_lang, set_lang, LanguageError
from pylons.templating import render_mako, render_genshi, render_jinja2
from pylons.controllers.util import abort, redirect_to, url_for

class SampleController(BaseController):
    def index(self):
        return 'basic index page'
    
    def testsqlalchemy(self):
        if SQLAtesting:
            c.foos = Session.query(Foo).all()
            return render_mako('test_sqlalchemy.html')
        pass
    
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
        
