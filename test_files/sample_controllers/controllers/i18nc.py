import datetime

from pylons import request, response, session, url
from pylons import tmpl_context as c
from pylons import app_globals
from pylons.i18n import _, get_lang, set_lang, LanguageError
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect

class I18NcController(WSGIController):
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
        obj = request._current_obj()
        locale_list = request.languages
        set_lang(request.languages)
        return unicode(_('basic index page'))

    def no_lang(self):
        set_lang(None)
        response.write(_('No language'))
        set_lang([])
        response.write(_('No languages'))
        return ''
    
    def langs(self):
        locale_list = request.languages
        set_lang(request.languages)
        return str(get_lang())
