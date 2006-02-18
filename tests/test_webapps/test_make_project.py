import urllib
import os
from paste.fixture import *
import pkg_resources
for spec in ['PasteScript', 'Paste', 'PasteDeploy', 'pylons']:
    pkg_resources.require(spec)

template_path = os.path.join(
    os.path.dirname(__file__), 'test_files')

test_environ = os.environ.copy()
test_environ['PASTE_TESTING'] = 'true'

testenv = TestFileEnvironment(
    os.path.join(os.path.dirname(__file__), 'output'),
    template_path=template_path,
    environ=test_environ)

def svn_repos_setup():
    res = testenv.run('svnadmin', 'create', 'REPOS',
                      printresult=False)
    testenv.svn_url = 'file://' + testenv.base_path + '/REPOS'
    assert 'REPOS' in res.files_created
    testenv.ignore_paths.append('REPOS')

def paster_create():
    global projenv
    res = testenv.run('paster', 'create', '--verbose', '--no-interactive',
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
        assert fn in res.files_created
        assert fn in res.stdout
    setup = res.files_created['ProjectName/setup.py']
    setup.mustcontain('0.1')
    setup.mustcontain('projectname:make_app')
    setup.mustcontain('main=paste.script.appinstall:Installer')
    setup.mustcontain("include_package_data=True")
    assert '0.1' in setup
    testenv.run('python setup.py egg_info',
                cwd=os.path.join(testenv.cwd, 'ProjectName'),
                expect_stderr=True)
    testenv.run('svn', 'commit', '-m', 'Created project', 'ProjectName')
    # A new environment with a new
    projenv = TestFileEnvironment(
        os.path.join(testenv.base_path, 'ProjectName'),
        start_clear=False,
        template_path=template_path,
        environ=test_environ)
    print projenv
    projenv.environ['PYTHONPATH'] = (
        projenv.environ.get('PYTHONPATH', '') + ':'
        + projenv.base_path)

def make_controller():
    res = projenv.run('paster controller test1')
    assert 'projectname/controllers/test1.py' in res.files_created
    assert 'projectname/tests/functional/test_test1.py' in res.files_created
    res = projenv.run('svn status')
    # Make sure all files are added to the repository:
    assert '?' not in res.stdout

def do_pytest():
    res = projenv.run('nosetests projectname/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName'))

def do_test_known():
    projenv.writefile('projectname/controllers/test1.py',
                      frompath='controller_test1.py')
    projenv.writefile('projectname/lib/app_globals.py',
                      frompath='app_globals.py')
    projenv.writefile('projectname/tests/functional/test_test1.py',
                      frompath='functional_test_controller_test1.py')
    res = projenv.run('nosetests projectname/tests',
                      expect_stderr=True,
                      cwd=os.path.join(testenv.cwd, 'ProjectName'))

def make_tag():
    global tagenv
    res = projenv.run('svn commit -m "updates"')
    res = projenv.run('python setup.py svntag --version=0.5')
    assert 'Tagging 0.5 version' in res.stdout
    assert 'Auto-update of version strings' in res.stdout
    res = testenv.run('svn co %s/ProjectName/tags/0.5 Proj-05'
                      % testenv.svn_url)
    setup = res.files_created['Proj-05/setup.py']
    setup.mustcontain('0.5')
    assert 'Proj-05/setup.cfg' not in res.files_created
    tagenv = TestFileEnvironment(
        os.path.join(testenv.base_path, 'Proj-05'),
        start_clear=False,
        template_path=template_path)

def test_project():
    global projenv
    projenv = None
    yield svn_repos_setup
    yield paster_create
    yield make_controller
    yield do_pytest
    yield do_test_known
    #yield make_tag
    
