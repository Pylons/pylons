"""Custom error middleware subclasses, used for error theme

These error middleware sub-classes are used mainly to provide skinning
for the Paste middleware. In the future this entire module will likely
be little more than a template, as Paste will get the skinning functionality.

The only additional thing besides skinning supplied, is the Template traceback
information.
"""
import cgi
import logging
import sys

from paste.evalexception.middleware import *
from paste.exceptions.formatter import *

import pylons
from pylons.middleware import media_path
from pylons.util import get_prefix

__all__ = []

log = logging.getLogger(__name__)


class Supplement(errormiddleware.Supplement):
    """This is a supplement used to display standard WSGI information in
    the traceback.
    """
    def extraData(self):
        data = {}
        cgi_vars = data[('extra', 'CGI Variables')] = {}
        wsgi_vars = data[('extra', 'WSGI Variables')] = {}
        # XXX: Legacy: hiding paste.config
        hide_vars = ['paste.config', 'wsgi.errors', 'wsgi.input',
                     'wsgi.multithread', 'wsgi.multiprocess',
                     'wsgi.run_once', 'wsgi.version',
                     'wsgi.url_scheme']
        for name, value in self.environ.items():
            if name.upper() == name:
                if value:
                    cgi_vars[name] = value
            elif name not in hide_vars:
                wsgi_vars[name] = value
        if self.environ['wsgi.version'] != (1, 0):
            wsgi_vars['wsgi.version'] = self.environ['wsgi.version']
        proc_desc = tuple([int(bool(self.environ[key]))
                           for key in ('wsgi.multiprocess',
                                       'wsgi.multithread',
                                       'wsgi.run_once')])
        wsgi_vars['wsgi process'] = self.process_combos[proc_desc]
        wsgi_vars['application'] = self.middleware.application
        data[('extra', 'Configuration')] = pylons.config.current_conf()
            
        # Add any extra sections here
       
        return data


class HTMLFormatter(formatter.HTMLFormatter):
    def format_collected_data(self, exc_data):
        general_data = {}
        if self.show_extra_data:
            for name, value_list in exc_data.extra_data.items():
                if isinstance(name, tuple):
                    importance, title = name
                else:
                    importance, title = 'normal', name
                for value in value_list:
                    general_data[(importance, name)] = self.format_extra_data(
                        importance, title, value)
        lines = []
        frames = self.filter_frames(exc_data.frames)
        for frame in frames:
            sup = frame.supplement
            if sup:
                if sup.object:
                    general_data[('important', 'object')] = self.format_sup_object(
                        sup.object)
                if sup.source_url:
                    general_data[('important', 'source_url')] = self.format_sup_url(
                        sup.source_url)
                if sup.line:
                    lines.append(self.format_sup_line_pos(sup.line, sup.column))
                if sup.expression:
                    lines.append(self.format_sup_expression(sup.expression))
                if sup.warnings:
                    for warning in sup.warnings:
                        lines.append(self.format_sup_warning(warning))
                if sup.info:
                    lines.extend(self.format_sup_info(sup.info))
            if frame.supplement_exception:
                lines.append('Exception in supplement:')
                lines.append(self.quote_long(frame.supplement_exception))
            if frame.traceback_info:
                lines.append(self.format_traceback_info(frame.traceback_info))
            filename = frame.filename
            if filename and self.trim_source_paths:
                for path, repl in self.trim_source_paths:
                    if filename.startswith(path):
                        filename = repl + filename[len(path):]
                        break
            lines.append(self.format_source_line(filename or '?', frame))
            source = frame.get_source_line()
            long_source = frame.get_source_line(2)
            if source:
                lines.append(self.format_long_source(
                    source, long_source))
        exc_info = self.format_exception_info(
            exc_data.exception_type,
            exc_data.exception_value)
        data_by_importance = {'important': [], 'normal': [],
                              'supplemental': [], 'extra': []}
        for (importance, name), value in general_data.items():
            data_by_importance[importance].append(
                (name, value))
        for value in data_by_importance.itervalues():
            value.sort()
        return self.format_combine(data_by_importance, lines, exc_info)
        
    def format_extra_data(self, importance, title, value):
        if isinstance(value, str):
            s = self.pretty_string_repr(value)
            if '\n' in s:
                return '%s:<br><pre>%s</pre>' % (title, self.quote(s))
            else:
                return '%s: <tt>%s</tt>' % (title, self.quote(s))
        elif isinstance(value, dict):
            return self.zebra_table(title, value)
        elif (isinstance(value, (list, tuple))
              and self.long_item_list(value)):
            return '%s: <tt>[<br>\n&nbsp; &nbsp; %s]</tt>' % (
                title, ',<br>&nbsp; &nbsp; '.join(map(self.quote, map(repr, value))))
        else:
            return '%s: <tt>%s</tt>' % (title, self.quote(repr(value)))
            
    def zebra_table(self, title, rows, table_class="variables"):
        if isinstance(rows, dict):
            rows = rows.items()
            rows.sort()
        table = ['<table class="%s">' % table_class,
                 '<tr class="header"><th colspan="2">%s</th></tr>'
                 % self.quote(title)]
        odd = False
        for name, value in rows:
            try:
                value = repr(value)
            except Exception, e:
                value = 'Cannot print: %s' % e
            odd = not odd
            table.append(
                '<tr class="%s"><td>%s</td>'
                % (odd and 'odd' or 'even', self.quote(name)))
            table.append(
                '<td><tt>%s</tt></td></tr>'
                % make_wrappable(self.quote(value)))
        table.append('</table>')
        return '\n'.join(table)

    def format_combine(self, data_by_importance, lines, exc_info):
        
        lines[:0] = [value for n, value in data_by_importance['important']]
        lines.append(exc_info)
        for name in 'normal', 'supplemental':
            lines.extend([value for n, value in data_by_importance[name]])
            
        extra_data = []
        if data_by_importance['extra']:
            #extra_data.append(
            #    '<script type="text/javascript">\nshow_button(\'extra_data\', \'extra data\');\n</script>\n' +
            #    '<div id="extra_data" class="hidden-data">\n')
            extra_data.extend([value for n, value in data_by_importance['extra']])
            #extra_data.append('</div>')
        extra_data_text = self.format_combine_lines(extra_data)
        text = self.format_combine_lines(lines)
        if self.include_reusable:
            return str(error_css + hide_display_js + text), extra_data
        else:
            # Usually because another error is already on this page,
            # and so the js & CSS are unneeded
            return text, extra_data


class InvalidTemplate(Exception):
    pass


class PylonsEvalException(EvalException):

    def __init__(self, application, global_conf=None, xmlhttp_key=None,
                 error_template=error_template, **errorparams):
        self.application = application
        self.error_template=error_template
        self.debug_infos = {}
        if xmlhttp_key is None:
            if global_conf is None:
                xmlhttp_key = '_'
            else:
                xmlhttp_key = global_conf.get('xmlhttp_key', '_')
        self.xmlhttp_key = xmlhttp_key
        self.errorparams = errorparams
        self.errorparams['debug_mode'] = self.errorparams['debug']
        del self.errorparams['debug']
        
        for s in ['head','traceback_data','extra_data','template_data']:
            if "%("+s+")s" not in self.error_template:
                raise InvalidTemplate("Could not find %s in template"%("%("+s+")s"))
        try:
            error_template%{'head': '',
                'traceback_data': '',
                'extra_data':'',
                'template_data':'',
                'set_tab':'',
                'prefix':''}
        except:
            raise Exception('Invalid template. Please ensure all % signs are properly '
                            'quoted as %% and no extra substitution strings are present.')

    def media(self, environ, start_response):
        """Handle Pylons specific media content @ /_debug/media/pylons"""
        if environ['PATH_INFO'].startswith('/pylons'):
            request.path_info_pop(environ)
            app = urlparser.StaticURLParser(media_path)
            return app(environ, start_response)
        else:
            return super(self.__class__, self).media(environ, start_response)
    media.exposed = True
            
    def respond(self, environ, start_response):
        if environ.get('paste.throw_errors'):
            return self.application(environ, start_response)
        base_path = request.construct_url(environ, with_path_info=False,
                                          with_query_string=False)
        environ['paste.throw_errors'] = True
        started = []
        def detect_start_response(status, headers, exc_info=None):
            try:
                return start_response(status, headers, exc_info)
            except:
                raise
            else:
                started.append(True)
        try:
            __traceback_supplement__ = Supplement, self, environ
            app_iter = self.application(environ, detect_start_response)
            try:
                return_iter = list(app_iter)
                return return_iter
            finally:
                if hasattr(app_iter, 'close'):
                    app_iter.close()
        except:
            exc_info = sys.exc_info()
            for expected in environ.get('paste.expected_exceptions', []):
                if isinstance(exc_info[1], expected):
                    raise

            # Tell the Registry to save its StackedObjectProxies current state
            # for later restoration
            registry.restorer.save_registry_state(environ)

            count = get_debug_count(environ)
            view_uri = self.make_view_url(environ, base_path, count)
            if not started:
                headers = [('content-type', 'text/html')]
                headers.append(('X-Debug-URL', view_uri))
                start_response('500 Internal Server Error',
                               headers,
                               exc_info)
            environ['wsgi.errors'].write('Debug at: %s\n' % view_uri)

            exc_data = collector.collect_exception(*exc_info)
            #debug_info = PylonsDebugInfo(count, exc_info, exc_data, base_path,
            debug_info = PylonsDebugInfo(count, exc_info, exc_data,
                                         get_prefix(environ, warn=False),
                                         environ, view_uri, error_template)
            assert count not in self.debug_infos
            self.debug_infos[count] = debug_info

            if self.xmlhttp_key:
                get_vars = wsgilib.parse_querystring(environ)
                if dict(get_vars).get(self.xmlhttp_key):
                    exc_data = collector.collect_exception(*exc_info)
                    html = formatter.format_html(
                        exc_data, include_hidden_frames=False,
                        include_reusable=False, show_extra_data=False)
                    return [html]
            
            # @@: it would be nice to deal with bad content types here
            return debug_info.content()


def myghty_html_data(exc_value):
    if hasattr(exc_value, 'htmlformat'):
        return exc_value.htmlformat()[333:-14]
    if hasattr(exc_value, 'mtrace'):
        return exc_value.mtrace.htmlformat()[333:-14]


template_error_formatters = [myghty_html_data]


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


class PylonsDebugInfo(DebugInfo):
    def __init__(self, counter, exc_info, exc_data, base_path,
                 environ, view_uri, error_template):
        DebugInfo.__init__(self, counter, exc_info, exc_data, base_path,
                           environ, view_uri)
        self.error_template = error_template

    def content(self):
        html, extra_data = format_eval_html(self.exc_data, self.base_path, self.counter)
        head_html = (formatter.error_css + formatter.hide_display_js)
        head_html += self.eval_javascript(self.counter)
        repost_button = make_repost_button(self.environ)
        template_data = '<p>No Template information available.</p>'
        tab = 'traceback_data'
        
        for formatter_ in template_error_formatters:
            result = formatter_(self.exc_value)
            if result:
                tab = 'template_data'
                template_data = result
                break

        head_html = (error_head_template % {'prefix':self.base_path}) + head_html

        traceback_data = error_traceback_template % {
            'prefix':self.base_path,
            'body':html,
            'repost_button': repost_button or '',
        }

        extra_data = """<h1 class="first"><a name="content"></a>Extra Data</h1>""" + \
            '\n'.join(extra_data)
        page = self.error_template % {
            'head': head_html,
            'traceback_data': traceback_data,
            'extra_data':extra_data,
            'template_data':template_data.replace('<h2>',
                                              '<h1 class="first">').replace('</h2>',
                                                                            '</h1>'),
            'set_tab':tab,
            'prefix':self.base_path,
            }
        return [page]

    def eval_javascript(self, counter):
        base_path = self.base_path + '/_debug'
        return (
            '<script type="text/javascript" src="%s/mochikit/MochiKit.js">'
            '</script>\n'
            '<script type="text/javascript" src="%s/media/debug.js">'
            '</script>\n'
            '<script type="text/javascript">\n'
            'debug_base = %r;\n'
            'debug_count = %r;\n'
            '</script>\n'
            % (base_path, base_path, base_path, counter))


class EvalHTMLFormatter(HTMLFormatter):

    def __init__(self, base_path, counter, **kw):
        super(EvalHTMLFormatter, self).__init__(**kw)
        self.base_path = base_path
        self.counter = counter
    
    def format_source_line(self, filename, frame):
        line = formatter.HTMLFormatter.format_source_line(
            self, filename, frame)
        return (line +
                '  <a href="#" class="switch_source" '
                'tbid="%s" onClick="return showFrame(this)">&nbsp; &nbsp; '
                '<img src="%s/_debug/media/pylons/img/plus.jpg" border=0 width=9 '
                'height=9> &nbsp; &nbsp;</a>'
                % (frame.tbid, self.base_path))


def format_eval_html(exc_data, base_path, counter):
    short_formatter = EvalHTMLFormatter(
        base_path=base_path,
        counter=counter,
        include_reusable=False)
    short_er, extra_data = short_formatter.format_collected_data(exc_data)
    short_text_er = formatter.format_text(exc_data, show_extra_data=False)
    long_formatter = EvalHTMLFormatter(
        base_path=base_path,
        counter=counter,
        show_hidden_frames=True,
        show_extra_data=False,
        include_reusable=False)
    long_er, extra_data_none = long_formatter.format_collected_data(exc_data)
    long_text_er = formatter.format_text(exc_data, show_hidden_frames=True,
                                         show_extra_data=False)

    extra_data_text = format_extra_data_text(exc_data)
    if extra_data_text:
        extra_data.append("""
        <br />
        <div id="util-link">
            <script type="text/javascript">
            show_button('extra_data_text', 'text version')
            </script>
        </div>
        <div id="extra_data_text" class="hidden-data">
        <textarea style="width: 100%%" rows=%s cols=60>%s</textarea>
        </div>
        """ % (len(extra_data_text.splitlines()), extra_data_text))

    if short_formatter.filter_frames(exc_data.frames) != \
        long_formatter.filter_frames(exc_data.frames):
        # Only display the full traceback when it differs from the
        # short version
        long_text_er = cgi.escape(long_text_er)
        full_traceback_html = """
        <br />
        <div id="util-link">
            <script type="text/javascript">
            show_button('full_traceback', 'full traceback')
            </script>
        </div>
        <div id="full_traceback" class="hidden-data">
        %s
            <br />
            <div id="util-link">
                <script type="text/javascript">
                show_button('long_text_version', 'full traceback text version')
                </script>
            </div>
            <div id="long_text_version" class="hidden-data">
            <textarea style="width: 100%%" rows=%s cols=60>%s</textarea>
            </div>
        </div>
        """ % (long_er, len(long_text_er.splitlines()), long_text_er)
    else:
        full_traceback_html = ''

    short_text_er = cgi.escape(short_text_er)
    return """
    <style type="text/css">
            #util-link a, #util-link a:link, #util-link a:visited,
            #util-link a:active {
                border-bottom: 2px outset #aaa
            }
    </style>
    %s
    <br />
    <br />
    <div id="util-link">
        <script type="text/javascript">
        show_button('short_text_version', 'text version')
        </script>
    </div>
    <div id="short_text_version" class="hidden-data">
    <textarea style="width: 100%%" rows=%s cols=60>%s</textarea>
    </div>
    %s
    """ % (short_er, len(short_text_er.splitlines()), short_text_er,
           full_traceback_html), extra_data


def format_extra_data_text(exc_data):
    """ Return a text representation of the 'extra_data' dict when one exists """
    extra_data_text = ''
    if not exc_data.extra_data:
        return extra_data_text

    text_formatter = TextFormatter()
    by_title = {}
    for name, value_list in exc_data.extra_data.items():
        if isinstance(name, tuple):
            importance, title = name
        else:
            importance, title = 'normal', name
        if importance != 'extra':
            continue
        for value in value_list:
            by_title[title] = text_formatter.format_extra_data(importance, title, value)

    titles = by_title.keys()
    titles.sort()
    for title in titles:
        extra_data_text += by_title[title]
    return extra_data_text


error_template = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
 <title>Server Error</title>
 %(head)s

<!-- CSS Imports -->
<link rel="stylesheet" href="%(prefix)s/_debug/media/pylons/style/orange.css" type="text/css" media="screen" />

<!-- Favorite Icons -->
<link rel="icon" href="%(prefix)s/_debug/media/pylons/img/icon-16.png" type="image/png" />

<!-- Mako Styles -->
<style type="text/css">
    .stacktrace { margin:5px 5px 5px 5px; }
    .highlight { padding:0px 10px 0px 10px; background-color:#9F9FDF; }
    .nonhighlight { padding:0px; background-color:#DFDFDF; }
    .sample { padding:10px; margin:10px 10px 10px 10px; font-family:monospace; font-size: 110%%; }
    .sampleline { padding:0px 10px 0px 10px; }
    .sourceline { margin:5px 5px 10px 5px; font-family:monospace; font-size: 110%%;}
</style>

</head>

<body id="documentation" onload="switch_display('%(set_tab)s')">
<!-- We are only using a table to ensure old browsers see the message correctly -->

<noscript>
<div style="border-bottom: 1px solid #808080">
<div style="border-bottom: 1px solid #404040">
<table width="100%%" border="0" cellpadding="0" bgcolor="#FFFFE1"><tr><td valign="middle"><img src="%(prefix)s/_debug/media/pylons/img/warning.gif" alt="Warning" /></td><td>&nbsp;</td><td><span style="padding: 0px; margin: 0px; font-family: Tahoma, sans-serif; font-size: 11px">Warning, your browser does not support JavaScript so you will not be able to use the interactive debugging on this page.</span></td></tr></table>
</div>
</div>
</noscript>
    
    <!-- Top anchor -->
    <a name="top"></a>
    
    <!-- Logo -->
    <h1 id="logo"><a class="no-underline" href="http://pylonshq.com"><img class="no-border" src="%(prefix)s/_debug/media/pylons/img/logo.gif" alt="Pylons" title="Pylons"/></a></h1>
    <p class="invisible"><a href="#content">Skip to content</a></p>

    <!-- Main Content -->
    <div id="nav-bar">

        <!-- Section Navigation -->
        <h4 class="invisible">Section Links</h4>

            <ul id="navlist">
               <!--  %%(links)s -->
                <li id='traceback_data_tab' class="active"><a href="javascript:switch_display('traceback_data')" id='traceback_data_link' class="active"  accesskey="1">Traceback</a></li>
                <li id='extra_data_tab' class="" ><a href="javascript:switch_display('extra_data')" id='extra_data_link' accesskey="2" >Extra Data</a></li>
                <li id='template_data_tab'><a href="javascript:switch_display('template_data')" accesskey="3" id='template_data_link'>Template</a></li>
            </ul>
    </div>
    <div id="main-content">
        <div class="hr"><hr class="hr" /></div>
        <div class="content-padding">
            <div id="extra_data" class="hidden-data">
                %(extra_data)s
            </div>
            <div id="template_data" class="hidden-data">
                %(template_data)s
            </div>
            <div id="traceback_data">
                %(traceback_data)s
            </div>
        </div>
        <br class="clear" />
        <div class="hr"><hr class="clear" /></div>
        <!-- Footer -->
    </div>
    <div style=" background: #FFFF99; padding: 10px 10px 10px 6%%">
        The Pylons Team | 
        <a href="#top" accesskey="9" title="Return to the top of the navigation links">Top</a>
    </div>
</body>
</html>
'''


error_head_template = """
<!-- 
    This is the Pylons error handler.

    Adapted for inclusion in Pylons by James Gardner. 
    Uses code from Ian Bicking, Mike Bayer and others.
-->

<style type="text/css">
        .red {
            color:#FF0000;
        }
        .bold {
            font-weight: bold;
        }
</style>
<script type="text/javascript">

if (document.images)
{
  pic1= new Image(100,25); 
  pic1.src="%(prefix)s/_debug/media/pylons/img/tab-yellow.png"; 
}

function switch_display(id) {
    ids = ['extra_data', 'template_data', 'traceback_data']
    for (i in ids){
        part = ids[i] 
        var el = document.getElementById(part);
        el.className = "hidden-data";
        var el = document.getElementById(part+'_tab');
        el.className = "not-active";
        var el = document.getElementById(part+'_link');
        el.className = "not-active";
    }
    var el = document.getElementById(id);
    el.className = "active";
    var el = document.getElementById(id+'_link');
    el.className = "active";
    var el = document.getElementById(id+'_tab');
    el.className = "active";
}   
</script>
"""


error_traceback_template = """
        <div style="float: left; width: 100%%; padding-bottom: 20px;">
        <h1 class="first"><a name="content"></a>Error Traceback</h1>
        <div id="error-area" style="display: none; background-color: #600; color: #fff; border: 2px solid black">
        <button onclick="return clearError()">clear this</button>
        <div id="error-container"></div>
        <button onclick="return clearError()">clear this</button>
        </div>
        %(body)s
        <br />
        <div class="highlight" style="padding: 20px;">
        <b>Extra Features</b>
        <table border="0">
        <tr><td>&gt;&gt;</td><td>Display the lines of code near each part of the traceback</td></tr>
        <tr><td><img src="%(prefix)s/_debug/media/pylons/img/plus.jpg" /></td><td>Show a debug prompt to allow you to directly debug the code at the traceback</td></tr>
        </table>
        </div>%(repost_button)s"""
