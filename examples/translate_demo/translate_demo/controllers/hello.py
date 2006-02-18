from translate_demo.lib.base import *

class HelloController(BaseController):

    def index(self):
        m.write('Default: %s<br />'%h._('Hello'))
        for lang in ['fr','en','es']:
            h.lang = lang
            m.write("%s: %s<br />"%(h.lang, h._('Hello')))