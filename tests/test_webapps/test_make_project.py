import urllib
import os
from paste.fixture import *
import pkg_resources
for spec in ['PasteScript', 'Paste', 'PasteDeploy', 'pylons']:
    pkg_resources.require(spec)

template_path = os.path.join(
    os.path.dirname(__file__), 'filestotest').replace('\\','/')

test_environ = os.environ.copy()
test_environ['PASTE_TESTING'] = 'true'

testenv = TestFileEnvironment(
    os.path.join(os.path.dirname(__file__), 'output').replace('\\','/'),
    template_path=template_path,
    environ=test_environ)

projenv = None
    
def _get_script_name(script):
    if sys.platform == 'win32':
        script += '.exe'
    return script

def svn_repos_setup():
    res = testenv.run(_get_script_name('svnadmin'), 'create', 'REPOS',
                      printresult=False)
    path = testenv.base_path.replace('\\','/').replace(' ','%20')
    base = 'file://'
    if ':' in path:
        base = 'file:///'
    testenv.svn_url = base + path + '/REPOS'
    assert 'REPOS' in res.files_created
    testenv.ignore_paths.append('REPOS')

def paster_create():
    global projenv
    res = testenv.run(_get_script_name('paster'), 'create', '--verbose', '--no-interactive',
                      #'--svn-repository=' + testenv.svn_url,
                      '--template=pylons',
                      'ProjectName',
                      'version=0.1',
                      )
    expect_fn = ['projectname', 'development.ini', 'setup.cfg', 'README.txt',
                 'setup.py', 'ProjectName.egg-info',
                 ]
    for fn in expect_fn:
        fn = os.path.join('ProjectName', fn)
        #~ if fn not in res.files_created.keys():
            #~ sys.stderr.write('ERROR not creates %r'%fn)
        #~ if fn not in res.stdout:
            #~ sys.stderr.write('ERROR not in stdout %r'%fn)
        assert fn in res.files_created.keys()
        assert fn in res.stdout
    
    setup = res.files_created[os.path.join('ProjectName','setup.py')]
    setup.mustcontain('0.1')
    setup.mustcontain('projectname.config.middleware:make_app')
    setup.mustcontain('main = pylons.util:PylonsInstaller')
    setup.mustcontain("include_package_data=True")
    assert '0.1' in setup
    testenv.run(_get_script_name('python')+' setup.py egg_info',
                cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'),
                expect_stderr=True)
    #testenv.run(_get_script_name('svn'), 'commit', '-m', 'Created project', 'ProjectName')
    # A new environment with a new
    projenv = TestFileEnvironment(
        os.path.join(testenv.base_path, 'ProjectName').replace('\\','/'),
        start_clear=False,
        template_path=template_path,
        environ=test_environ)
    projenv.environ['PYTHONPATH'] = (
        projenv.environ.get('PYTHONPATH', '') + ':'
        + projenv.base_path)

def make_controller():
    res = projenv.run(_get_script_name('paster')+' controller sample')
    assert os.path.join('projectname','controllers','sample.py') in res.files_created
    assert os.path.join('projectname','tests','functional','test_sample.py') in res.files_created
    #res = projenv.run(_get_script_name('svn')+' status')
    # Make sure all files are added to the repository:
    assert '?' not in res.stdout

def _do_proj_test(copydict, emptyfiles=None):
    """Given a dict of files, where the key is a filename in filestotest, the value is
    the destination in the new projects dir. emptyfiles is a list of files that should
    be created and empty."""
    if not emptyfiles:
        emptyfiles = []
    for original, newfile in copydict.iteritems():
        projenv.writefile(newfile, frompath=original)
    for fi in emptyfiles:
        projenv.writefile(fi)
    res = projenv.run(_get_script_name('nosetests')+' -d',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'))

def do_pytest():
    _do_proj_test({'development.ini':'development.ini'})

def do_knowntest():
    copydict = {
        'controller_sample.py':'projectname/controllers/sample.py',
        'app_globals.py':'projectname/lib/app_globals.py',
        'functional_sample_controller_sample1.py':'projectname/tests/functional/test_sample.py',
    }
    _do_proj_test(copydict)

def do_i18ntest():
    copydict = {
        'functional_sample_controller_i18n.py':'projectname/tests/functional/test_i18n.py',
        'messages.ja.po':'projectname/i18n/ja/LC_MESSAGES/projectname.po',
        'messages.ja.mo':'projectname/i18n/ja/LC_MESSAGES/projectname.mo',
    }
    _do_proj_test(copydict)

def do_kid_default():
    copydict = {
        'testkid.kid':'projectname/kidtemplates/testkid.kid',
        'middleware_def_engine.py':'projectname/config/middleware.py',
        'functional_sample_controller_sample2.py':'projectname/tests/functional/test_sample2.py'
    }
    empty = ['projectname/kidtemplates/__init__.py']
    _do_proj_test(copydict, empty)

def do_two_engines():
    copydict = {
        'middleware_two_engines.py':'projectname/config/middleware.py',
        'test_mako.html':'projectname/templates/test_mako.html',
        'functional_sample_controller_sample3.py':'projectname/tests/functional/test_sample2.py',
    }
    _do_proj_test(copydict)

def do_crazy_decorators():
    _do_proj_test({'functional_sample_controller_sample4.py':'projectname/tests/functional/test_sample3.py'})

def do_cheetah():
    copydict = {
        'controller_sample.py':'projectname/controllers/sample.py',
        'testcheetah.tmpl':'projectname/cheetah/testcheetah.tmpl',
        'middleware_cheetah_engine.py':'projectname/config/middleware.py',
        'functional_sample_controller_cheetah.py':'projectname/tests/functional/test_cheetah.py',
    }
    empty = [
         'projectname/cheetah/__init__.py',
         'projectname/tests/functional/test_sample.py',
         'projectname/tests/functional/test_sample2.py',
         'projectname/tests/functional/test_sample3.py'
     ]
    _do_proj_test(copydict, empty)

def do_cache_decorator():
    copydict = {
        'middleware_def_engine.py':'projectname/config/middleware.py',
        'app_globals.py':'projectname/lib/app_globals.py',
        'cache_controller.py':'projectname/controllers/cache.py',
        'functional_controller_cache_decorator.py':'projectname/tests/functional/test_cache.py',
    }
    empty = [
        'projectname/tests/functional/test_mako.py',
        'projectname/tests/functional/test_cheetah.py',
        'projectname/tests/functional/test_sample.py',
        'projectname/tests/functional/test_sample2.py',
        'projectname/tests/functional/test_sample3.py'
     ]
    _do_proj_test(copydict, empty)

def do_xmlrpc():
    copydict = {
        'base_with_xmlrpc.py':'projectname/lib/base.py',
        'controller_xmlrpc.py':'projectname/controllers/xmlrpc.py',
        'functional_controller_xmlrpc.py':'projectname/tests/functional/test_xmlrpc.py'
    }
    empty = [
        'projectname/tests/functional/test_cache.py',
    ]
    _do_proj_test(copydict, empty)

def do_legacy_app():
    legacyenv = TestFileEnvironment(
        os.path.join(testenv.base_path, 'legacyapp').replace('\\','/'),
        start_clear=False,
        template_path=template_path,
        environ=test_environ)
    res = legacyenv.run(_get_script_name('nosetests')+' legacyapp/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'legacyapp').replace('\\','/'))

def make_tag():
    global tagenv
    #res = projenv.run(_get_script_name('svn')+' commit -m "updates"')
    # Space at the end needed so run() doesn't add \n causing svntag to complain
    #res = projenv.run(_get_script_name('python')+' setup.py svntag --version=0.5 ')
    # XXX Still fails => setuptools problem on win32?
    assert 'Tagging 0.5 version' in res.stdout
    assert 'Auto-update of version strings' in res.stdout
    res = testenv.run(_get_script_name('svn')+' co %s/ProjectName/tags/0.5 Proj-05 '
                      % testenv.svn_url)
    setup = res.files_created['Proj-05/setup.py']
    setup.mustcontain('0.5')
    assert 'Proj-05/setup.cfg' not in res.files_created
    tagenv = TestFileEnvironment(
        os.path.join(testenv.base_path, 'Proj-05').replace('\\','/'),
        start_clear=False,
        template_path=template_path)

def test_project():
    #yield svn_repos_setup
    yield (paster_create,)
    yield (make_controller,)
    yield (do_pytest,)
    yield (do_knowntest,)
    yield (do_i18ntest,)
    yield (do_kid_default,)
    yield (do_two_engines,)
    yield (do_cheetah,)
    yield (do_crazy_decorators,)
    yield (do_cache_decorator,)
    yield (do_xmlrpc,)
    #yield do_legacy_app
    #yield make_tag
    
