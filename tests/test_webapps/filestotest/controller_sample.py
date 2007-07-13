from projectname.lib.base import *
from pylons import h as deprecated_h, Response
from pylons.decorators import rest
from pylons.i18n import get_lang, set_lang, LanguageError
from pylons.templating import render_response

class SampleController(BaseController):
    def index(self):
        return Response('basic index page')
    
    def session_increment(self):
        session.setdefault('counter', -1)
        session['counter'] += 1
        session.save()
        return Response('session incrementer')
    
    def globalup(self):
        return Response(g.message)
    
    def global_store(self, id):
        if id:
            g.counter += int(id)
        return Response(str(g.counter))
    
    def myself(self):
        return Response(h.url_for())
    
    def myparams(self):
        return Response(str(request.params))
    
    def testdefault(self):
        c.test = "This is in c var"
        return render_response('testkid')
    
    def test_extra_engine(self):
        return render_response('kid', 'testkid')
    
    def test_template_caching(self):
        return render_response('/test_mako.html', cache_expire='never')
    
    def test_only_post(self):
        return Response('It was a post!')
    test_only_post = rest.dispatch_on(GET='test_only_get')(rest.restrict('POST')(test_only_post))
    
    def test_only_get(self):
        return Response('It was a get!')
    test_only_get = rest.restrict('GET')(test_only_get)
    
    def impossible(self):
        return Response('This should never be shown')
    impossible = rest.restrict('POST')(rest.dispatch_on(POST='test_only_post')(impossible))

    def testcheetah(self):
        c.test = "This is in c var"
        return render_response('testcheetah')

    def set_lang(self):
        lang = request.GET['lang']
        try:
            set_lang(lang)
        except (LanguageError, IOError), e:
            resp_unicode = _('Could not set language to "%(lang)s"') % {'lang': lang}
        else:
            session['lang'] = lang
            session.save()
            resp_unicode = _('Set language to "%(lang)s"') % {'lang': lang}
        return Response(resp_unicode)

    def i18n_index(self):
        locale_list = request.languages
        set_lang(request.languages)
        return Response(unicode(_('basic index page')))

    def no_lang(self):
        resp = Response()
        set_lang(None)
        resp.write(_('No language'))
        set_lang([])
        resp.write(_('No languages'))
        return resp
        
    def deprecated_h(self):
        return Response('%s is %s' % \
                            (h.url_for(), deprecated_h.url_for()))
