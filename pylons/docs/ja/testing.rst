.. Unit and functional testing

.. _testing:

===========================
ユニットテストと機能テスト
===========================

.. Unit Testing with :mod:`webtest`

:mod:`webtest` を用いたユニットテスト
=====================================

.. Pylons provides powerful unit testing capabilities for your web
.. application utilizing `webtest <http://pythonpaste.org/webtest/>`_
.. to emulate requests to your web application. You can then ensure
.. that the response was handled appropriately and that the controller
.. set things up properly.

Pylons は、 Web アプリケーションに対するリクエストをエミュレートするた
めに `webtest <http://pythonpaste.org/webtest/>`_ を使用している Web ア
プリケーションに強力なユニットテストの機能を提供します。そして、レスポ
ンスが適切に扱われ、コントローラーが適切に値を処理していることを保障す
ることができます。


.. To run the test suite for your web application, Pylons utilizes the
.. `nose <http://somethingaboutorange.com/mrl/projects/nose/>`_ test
.. runner/discovery package. Running ``nosetests`` in your project
.. directory will run all the tests you create in the tests
.. directory. If you don't have nose installed on your system, it can
.. be installed via setuptools with:

Web アプリケーションのテストスイートを走らせるために、 Pylons は `nose
<http://somethingaboutorange.com/mrl/projects/nose/>`_ というテスト実行
/発見パッケージを利用しています。プロジェクトディレクトリにおいて
``nosetests`` を実行すると、 tests ディレクトリで作成した全てのテストが
実行されます。システム上に nose がインストールされていない場合は、以下
のコードを用いて setuptools でインストール可能です。


.. code-block:: bash 

    $ easy_install -U nose 


.. To avoid conflicts with your development setup, the tests use the
.. `test.ini` configuration file when run. This means **you must
.. configure any databases, etc. in your test.ini file or your tests
.. will not be able to find the database configuration**.

開発用の設定と衝突するのを避けるために、テストは実行するときに
`test.ini` 設定ファイルを使用します。 これは、 **test.ini ファイルでデー
タベースなどの設定をしなければ、テストはデータベース設定を見つけられな
い** ということを意味します。


.. warning:: 

    .. Nose can trigger errors during its attempt to search for doc
    .. tests since it will try and import all your modules one at a
    .. time *before* your app was loaded. This will cause files under
    .. models/ that rely on your app to be running, to fail.

    nose が doctest を検索している際にエラーが起きる場合があります。こ
    れは、アプリケーションがロードされる *前に* 、nose がモジュールを一
    度にインポートしようとするためです。このため、アプリケーションが起
    動していることに依存している moduls/ 以下のファイルが失敗します。


.. Pylons 0.9.6.1 and later includes a plugin for nose that loads the
.. app before the doctests scan your modules, allowing models to be
.. doctested. You can use this option from the command line with nose:

Pylons 0.9.6.1 以降は nose の plugin を含んでいます。それは doctest が
モジュールをスキャンする前にアプリケーションをロードするためのもので、
モデルに対して doctest を行うことを可能にします。コマンドラインから
nose と共にこのオプションを使用できます:


.. code-block:: bash 

    nosetests --with-pylons=test.ini 


.. Or by setting up a `[nosetests]` block in your setup.cfg: 

または setup.cfg で `[nosetests]` ブロックをセットアップすることによっ
て:


.. code-block:: ini 

    [nosetests] 
    verbose=True 
    verbosity=2 
    with-pylons=test.ini 
    detailed-errors=1 
    with-doctest=True 


.. Then just run: 

テストを実行するには以下を実行します:


.. code-block:: bash 

    python setup.py nosetests 


.. to run the tests. 


Example: Testing a Controller 
============================= 

.. First let's create a new project and controller for this example: 

まず、下の例のように新しいプロジェクトとコントローラーを作成しましょう。


.. code-block:: bash 

    $ paster create -t pylons TestExample 
    $ cd TestExample 
    $ paster controller comments 


.. You'll see that it creates two files when you create a
.. controller. The stub controller, and a test for it under
.. ``testexample/tests/functional/``.

コントローラーを作成すると、 2 つのファイルが生成されるのがわかるでしょ
う。スタブ・コントローラーと、 ``testexample/tests/functional/`` 以下の
テストです。


.. Modify the ``testexample/controllers/comments.py`` file so it looks
.. like this:

``testexample/controllers/comments.py`` ファイルを以下のように修正して
ください。


.. code-block:: python 

    from testexample.lib.base import * 

    class CommentsController(BaseController): 

        def index(self): 
            return 'Basic output' 

        def sess(self): 
            session['name'] = 'Joe Smith' 
            session.save() 
            return 'Saved a session' 


.. Then write a basic set of tests to ensure that the controller
.. actions are functioning properly, modify
.. ``testexample/tests/functional/test_comments.py`` to match the
.. following:

そうしたら、コントローラーのアクションが適切に機能していることを確かめ
るために基本的なテストを書きましょう。
``testexample/tests/functional/test_comments.py`` を以下のように編集し
てください。


.. code-block:: python 

    from testexample.tests import * 

    class TestCommentsController(TestController): 
        def test_index(self): 
            response = self.app.get(url(controller='/comments')) 
            assert 'Basic output' in response 

        def test_sess(self): 
            response = self.app.get(url(controller='/comments', action='sess')) 
            assert response.session['name'] == 'Joe Smith' 
            assert 'Saved a session' in response 


.. Run ``nosetests`` in your main project directory and you should see
.. them all pass:

メインプロジェクトのディレクトリの中で ``nosetests`` を実行すると、すべ
てのテストが通ることが確認できるはずです。


.. code-block:: pycon 

    .. 
    ---------------------------------------------------------------------- 
    Ran 2 tests in 2.999s 

    OK 


.. Unfortunately, a plain assert does not provide detailed information
.. about the results of an assertion should it fail, unless you
.. specify it a second argument. For example, add the following test
.. to the ``test_sess`` function:

残念ながら、 通常の assert 文は、第 2 引数を指定しない限り、失敗したア
サーションの結果に関する詳細な情報を提供しません。例えば、
``test_sess`` 関数に以下のテストを追加してみてください。


.. code-block:: python 

    assert response.session.has_key('address') == True 


.. When you run ``nosetests`` you will get the following,
.. not-very-helpful result:

``nosetests`` を実行すると、以下のようなあまり親切でない結果が返ってき
ます:


.. code-block:: pycon 

    .F 
    ====================================================================== 
    FAIL: test_sess (testexample.tests.functional.test_comments.TestCommentsController) 
    ---------------------------------------------------------------------- 
    Traceback (most recent call last): 
    File "~/TestExample/testexample/tests/functional/test_comments.py", line 12, in test_sess 
    assert response.session.has_key('address') == True 
    AssertionError: 


    ---------------------------------------------------------------------- 
    Ran 2 tests in 1.417s 

    FAILED (failures=1) 


.. You can augment this result by doing the following:

次のようにすることで、この結果を変えることができます:


.. code-block:: python 

    assert response.session.has_key('address') == True, "address not found in session" 


.. Which results in: 

その結果はこうなります:


.. code-block:: pycon 

    .F 
    ====================================================================== 
    FAIL: test_sess (testexample.tests.functional.test_comments.TestCommentsController) 
    ---------------------------------------------------------------------- 
    Traceback (most recent call last): 
    File "~/TestExample/testexample/tests/functional/test_comments.py", line 12, in test_sess 
    assert response.session.has_key('address') == True 
    AssertionError: address not found in session 


    ---------------------------------------------------------------------- 
    Ran 2 tests in 1.417s 

    FAILED (failures=1) 


.. But detailing every assert statement could be time consuming. Our
.. TestController subclasses the standard Python ``unittest.TestCase``
.. class, so we can use utilize its helper methods, such as
.. ``assertEqual``, that can automatically provide a more detailed
.. AssertionError. The new test line looks like this:

しかし、すべての assert 文でこのようなことをしなければならないのは時間
の無駄というものです。 TestController は Python 標準の
``unittest.TestCase`` クラスのサブクラスなので、より詳細な
AssertionError を自動的に提供する ``assertEqual`` などのヘルパーメソッ
ドを使うことができます。新しいテストコードは以下のようになります。


.. code-block:: python 

    self.assertEqual(response.session.has_key('address'), True) 


.. Which provides the more useful failure message: 

これは、より有用な失敗メッセージを出力します:


.. code-block:: pycon 

    .F 
    ====================================================================== 
    FAIL: test_sess (testexample.tests.functional.test_comments.TestCommentsController) 
    ---------------------------------------------------------------------- 
    Traceback (most recent call last): 
    File "~/TestExample/testexample/tests/functional/test_comments.py", line 12, in test_sess 
    self.assertEqual(response.session.has_key('address'), True) 
    AssertionError: False != True 


.. Testing Pylons Objects 

Pylon のオブジェクトをテストする
================================

.. Pylons will provide several additional attributes for the
.. :mod:`webtest` :class:`webtest.TestResponse` object that let you
.. access various objects that were created during the web request:

Pylons は :mod:`webtest` の :class:`webtest.TestResponse` オブジェクト
に属性をいくつか追加するので、その属性を通して Web リクエストの間に生成
された様々な変数にアクセスできます。


``session`` 

    .. Session object 

    セッションオブジェクト

``req`` 

    .. Request object 

    リクエストオブジェクト

``c`` 

    .. Object containing variables passed to templates 

    テンプレートに渡される変数を含んだオブジェクト

``g`` 

    .. Globals object 

    グローバルオブジェクト


.. To use them, merely access the attributes of the response *after*
.. you've used a get/post command:

これらの変数を使うには、単に get/post コマンドを利用した *後で*
response の属性にアクセスします。


.. code-block:: python 

    response = app.get('/some/url') 
    assert response.session['var'] == 4 
    assert 'REQUEST_METHOD' in response.req.environ 


.. note:: 

    .. The :class:`response <webtest.TestResponse>` object already has
    .. a TestRequest object assigned to it, therefore Pylons assigns
    .. its ``request`` object to the response as ``req``.

    :class:`response <webtest.TestResponse>` オブジェクトはすでに
    TestRequest オブジェクトを持っているため、 Pylons は ``request`` オ
    ブジェクトを response の ``req`` 属性として割り当てています。


.. Testing Your Own Objects 

独自のオブジェクトをテストする
==============================

.. WebTest's fixture testing allows you to designate your own objects
.. that you'd like to access in your tests. This powerful functionality
.. makes it easy to test the value of objects that are normally only
.. retained for the duration of a single request.

WebTest の fixture テストでは、テストの中でアクセスしたい独自オブジェク
トを指定することができます。この強力な機能のおかげで、 1 回のリクエスト
の間だけ保持されているようなオブジェクトの値のテストを簡単に行うことが
できます。


.. Before making objects available for testing, its useful to know
.. when your application is being tested. WebTest will provide an
.. environ variable called ``paste.testing`` that you can test for the
.. presence and truth of so that your application only populates the
.. testing objects when it has to.

テストのためにオブジェクトを使えるようにする前に、アプリケーションがい
つテストされるかを知ることは役に立ちます。 WebTest は
``paste.testing`` という環境変数を提供しており、その存在や真偽を確認す
ることで必要な時だけアプリケーションがテストオブジェクトを投入すること
ができます。

.. Populating the :mod:`webtest` response object with your objects is
.. done by adding them to the environ dict under the key
.. ``paste.testing_variables``.  Pylons creates this dict before
.. calling your application, so testing for its existence and adding
.. new values to it is recommended. All variables assigned to the
.. ``paste.testing_variables`` dict will be available on the response
.. object with the key being the attribute name.

:mod:`webtest` のレスポンスオブジェクトへの独自オブジェクトの投入は、独
自オブジェクトを environ 辞書の ``paste.testing_variables`` キーに追加
することによって行います。 Pylons はこの辞書をアプリケーションが呼ばれ
る前に作成するので、存在を確かめてから新しい値を追加することが推奨され
ます。 ``paste.testing_variables`` 辞書に割り当てられているすべての変数
は、そのキーを属性名にすることで、レスポンスオブジェクトで利用可能です。


.. note::

    .. WebTest is an extracted stand-alone version of a Paste
    .. component called paste.fixture. For backwards compatibility,
    .. WebTest continues to honor the ``paste.testing_variables`` key
    .. in the environ.

    WebTest は paste.fixture と呼ばれる Paste コンポーネントから抽出さ
    れたスタンドアロンバージョンです。 後方互換性のため、 WebTest は
    environ の ``paste.testing_variables`` キーを尊重し続けています。


.. Example: 

例:


.. code-block:: python 

    # testexample/lib/base.py 

    from pylons import request
    from pylons.controllers import WSGIController
    from pylons.templating import render_mako as render

    class BaseController(WSGIController): 
        def __call__(self, environ, start_response): 
            # Create a custom email object 
            email = MyCustomEmailObj() 
            email.name = 'Fred Smith' 
            if 'paste.testing_variables' in request.environ: 
                request.environ['paste.testing_variables']['email'] = email 
            return WSGIController.__call__(self, environ, start_response) 


    # testexample/tests/functional/test_controller.py 
    from testexample.tests import * 

    class TestCommentsController(TestController): 
        def test_index(self): 
            response = self.app.get(url(controller='/')) 
            assert response.email.name == 'Fred Smith' 


.. seealso::

    .. `WebTest Documentation <http://pythonpaste.org/webtest/>`_
    ..     Documentation covering webtest and its usage
    
    `WebTest Documentation <http://pythonpaste.org/webtest/>`_
        webtest とその使用法をカバーしたドキュメント
    
    .. :mod:`WebTest Module docs <webtest>`
    ..     Module API reference for methods available for use when testing
    ..     the application

    :mod:`WebTest Module docs <webtest>`
        アプリケーションをテストするときに使用できるメソッドに対するモ
        ジュール API リファレンス


.. _unit_testing:

Unit Testing
============

XXX: Describe unit testing an applications models, libraries


.. _functional_testing:

Functional Testing
==================

XXX: Describe functional/integrated testing, WebTest
