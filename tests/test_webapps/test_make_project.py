import urllib
import os
from paste.fixture import *
import pkg_resources
for spec in ['PasteScript', 'Paste', 'PasteDeploy', 'pylons']:
    pkg_resources.require(spec)

template_path = os.path.join(
    os.path.dirname(__file__), 'test_files').replace('\\','/')

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
    sys.stderr.write(' '.join(['paster', 'create', '--verbose', '--no-interactive',
                      '--svn-repository=' + testenv.svn_url,
                      '--template=pylons',
                      'ProjectName',
                      'version=0.1',
                      ]))
    res = testenv.run(_get_script_name('paster'), 'create', '--verbose', '--no-interactive',
                      '--svn-repository=' + testenv.svn_url,
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
    setup.mustcontain('projectname:make_app')
    setup.mustcontain('main=paste.script.appinstall:Installer')
    setup.mustcontain("include_package_data=True")
    assert '0.1' in setup
    testenv.run(_get_script_name('python')+' setup.py egg_info',
                cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'),
                expect_stderr=True)
    testenv.run(_get_script_name('svn'), 'commit', '-m', 'Created project', 'ProjectName')
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
    res = projenv.run(_get_script_name('svn')+' status')
    # Make sure all files are added to the repository:
    assert '?' not in res.stdout

def do_pytest():
    projenv.writefile('development.ini',
                      frompath='development.ini')
    res = projenv.run(_get_script_name('nosetests')+' projectname/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'))

def do_test_known():
    projenv.writefile('projectname/controllers/sample.py',
                      frompath='controller_sample.py')
    projenv.writefile('projectname/lib/app_globals.py',
                      frompath='app_globals.py')
    projenv.writefile('projectname/tests/functional/test_sample.py',
                      frompath='functional_sample_controller_sample1.py')
    res = projenv.run(_get_script_name('nosetests')+' projectname/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'))

def do_kid_default():
    projenv.writefile('projectname/kidtemplates/testkid.kid',
                      frompath='testkid.kid')
    projenv.writefile('projectname/kidtemplates/__init__.py')
    projenv.writefile('projectname/config/middleware.py',
                      frompath='middleware_def_engine.py')
    projenv.writefile('projectname/tests/functional/test_sample2.py',
                      frompath='functional_sample_controller_sample2.py')
    res = projenv.run(_get_script_name('nosetests')+' projectname/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'))

def do_two_engines():
    projenv.writefile('projectname/config/middleware.py',
                      frompath='middleware_two_engines.py')
    projenv.writefile('projectname/templates/test_myghty.myt',
                      frompath='test_myghty.myt')    
    projenv.writefile('projectname/tests/functional/test_sample2.py',
                      frompath='functional_sample_controller_sample3.py')
    res = projenv.run(_get_script_name('nosetests')+' projectname/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'))

def do_crazy_decorators():
    projenv.writefile('projectname/tests/functional/test_sample3.py',
                      frompath='functional_sample_controller_sample4.py')
    res = projenv.run(_get_script_name('nosetests')+' projectname/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName').replace('\\','/'))
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
    res = projenv.run(_get_script_name('svn')+' commit -m "updates"')
    # Space at the end needed so run() doesn't add \n causing svntag to complain
    res = projenv.run(_get_script_name('python')+' setup.py svntag --version=0.5 ')
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
    yield svn_repos_setup
    yield paster_create
    yield make_controller
    yield do_pytest
    yield do_test_known
    yield do_kid_default
    yield do_two_engines
    yield do_crazy_decorators
    #yield do_legacy_app
    #yield make_tag
    
