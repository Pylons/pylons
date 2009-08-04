.. _configuration:

=======================
設定 (Configuration)
=======================

.. Pylons comes with two main ways to configure an application:

Pylons でアプリケーションを設定する方法は主に 2 つあります:


.. * The configuration file (:ref:`run-config`)
.. * The application's ``config`` directory

* 設定ファイル (:ref:`run-config`)
* アプリケーションの ``config`` ディレクトリ


.. The files in the ``config`` directory change certain aspects of how
.. the application behaves. Any options that the webmaster should be
.. able to change during deployment should be specified in a
.. configuration file.

``config`` ディレクトリのファイルはアプリケーションの振る舞いに関する特
定の側面を変更します。 ウェブ管理者がデプロイの際に変えることのできるど
んなオプションも設定ファイルで指定されるべきです。


.. tip::

    .. A good indicator of whether an option should be set in the
    .. ``config`` directory code vs. the configuration file is whether
    .. or not the option is necessary for the functioning of the
    .. application. If the application won't function without the
    .. setting, it belongs in the appropriate :file:`config/`
    .. directory file. If the option should be changed depending on
    .. deployment, it belongs in the :ref:`run-config`.

    あるオプションが ``config`` ディレクトリのコードと設定ファイルのど
    ちらで設定されるべきかということに関する良い指標は、そのオプション
    がアプリケーションの機能に必要であるかどうかということです。アプリ
    ケーションがその設定なしには機能しないなら、それは適切な
    :file:`config/` に置かれるべきです。もしそのオプションがデプロイに
    よって変わりうるなら :ref:`run-config` に含まれます。


.. The applications :file:`config/` directory includes:

アプリケーションの :file:`config/` ディレクトリは以下のファイルを含んで
います:


.. * :file:`config/environment.py` described in :ref:`environment-config`
.. * :file:`config/middleware.py` described in :ref:`middleware-config`
.. * :file:`config/deployment.ini_tmpl` described in :ref:`production-config`
.. * :file:`config/routing.py` described in :ref:`url-config`

* :file:`config/environment.py` は :ref:`environment-config` で説明されます
* :file:`config/middleware.py` は :ref:`middleware-config` で説明されます
* :file:`config/deployment.ini_tmpl` は :ref:`production-config` で説明されます
* :file:`config/routing.py` は :ref:`url-config` で説明されます


.. Each of these files allows developers to change key aspects of how
.. the application behaves.

これらそれぞれのファイルによって、開発者はアプリケーションの振る舞いに
関する重要な側面を変えることができます。


.. Runtime Configuration
 
.. _run-config:

*********************
実行時設定
*********************

.. When a new project is created a sample configuration file called
.. :file:`development.ini` is automatically produced as one of the
.. project files. This default configuration file contains sensible
.. options for development use, for example when developing a Pylons
.. application it is very useful to be able to see a debug report
.. every time an error occurs. The :file:`development.ini` file
.. includes options to enable debug mode so these errors are shown.

新しいプロジェクトが作られるとき、プロジェクトのファイルの 1 つとして
:file:`development.ini` と呼ばれる設定ファイルのサンプルが自動的に生成
されます。このデフォルトの設定ファイルは開発のために使用するのに適切な
オプションを含んでいます。例えば、 Pylons アプリケーションの開発中は、
エラーが発生する度にデバッグレポートを見ることができると非常に便利です。
:file:`development.ini` ファイルはデバッグモードを有効にするオプション
を含んでいるので、このようなエラーが表示されます。


.. Since the configuration file is used to determine which application
.. is run, multiple configuration files can be used to easily toggle
.. sets of options. Typically a developer might have a
.. ``development.ini`` configuration file for testing and a
.. ``production.ini`` file produced by the :command:`paster
.. make-config` command for testing the command produces sensible
.. production output. A :file:`test.ini` configuration is also
.. included in the project for test-specific options.

どのアプリケーションを実行するかを決定するために設定ファイルが使われる
ので、複数の設定ファイルを使用することで簡単にオプションのセットを切り
換えることができます。典型的に、開発者はテスト (訳注: 開発) のための
``development.ini`` 設定ファイルと :command:`paster make-config` コマン
ドで生成された ``production.ini`` ファイルを使います。
``production.ini`` ファイルは :command:`paster make-config` コマンドが
適切なプロダクション用ファイルを生成することをテストするために使用され
ます。また、 :file:`test.ini` 設定は、テスト専用のオプションのためにプ
ロジェクトに含まれています。


.. To specify a configuration file to use when running the
.. application, change the last part of the :command:`paster serve` to
.. include the desired config file:

アプリケーションを実行するときに使用する設定ファイルを指定するには、
:command:`paster serve` の最後の部分に必要な設定ファイルを含めるように
変えてください:


.. code-block :: bash 

    $ paster serve production.ini


.. seealso::

    .. Configuration file format **and options** are described in
    .. great detail in the `Paste Deploy documentation
    .. <http://pythonpaste.org/deploy/>`_.

    設定ファイルのフォーマット **とオプション** は、 `Paste Deploy
    documentation <http://pythonpaste.org/deploy/>`_ で丹念に説明されて
    います。


.. Getting Information From Configuration Files

設定ファイルから情報を得る
============================================

.. All information from the configuration file is available in the
.. ``pylons.config`` object. ``pylons.config`` also contains
.. application configuration as defined in the project's
.. :file:`config.environment` module.

設定ファイルからのすべての情報は ``pylons.config`` オブジェクトで利用可
能です。 また、 ``pylons.config`` はプロジェクトの
:file:`config.environment` モジュールで定義されたアプリケーション設定を
含んでいます。


.. code-block :: python

    from pylons import config 


.. ``pylons.config`` behaves like a dictionary. For example, if the
.. configuration file has an entry under the ``[app:main]`` block:

``pylons.config`` は辞書のように振る舞います。例えば設定ファイルの
``[app:main]`` ブロックの中に以下のエントリがある場合:


.. code-block :: ini

    cache_dir = %(here)s/data


.. That can then be read in the projects code:

プロジェクトコードではこれを次のようにして読み込むことができます:


.. code-block :: python

    from pylons import config 
    cache_dir = config['cache_dir']


.. Or the current debug status like this: 

あるいは現在のデバッグ状態については:


.. code-block :: python 

    debug = config['debug']


.. Evaluating Non-string Data in Configuration Files

設定ファイルの中の非文字列データを評価する
-------------------------------------------------

.. By default, all the values in the configuration file are considered
.. strings.  To make it easier to handle boolean values, the Paste
.. library comes with a function that will convert ``true`` and
.. ``false`` to proper Python boolean values:

デフォルトでは、設定ファイルのすべての値は文字列であるとみなされます。
ブール値をより簡単に扱えるようにするために、 Paste ライブラリは
``true`` と ``false`` を適切な Python ブール値へと変換する関数を提供し
ています:


.. code-block :: python
    
    from paste.deploy.converters import asbool
    
    debug = asbool(config['debug'])


.. This is used already in the default projects'
.. :ref:`middleware-config` to toggle middleware that should only be
.. used in development mode (with ``debug``) set to true.

この関数は、既にデフォルトプロジェクトの :ref:`middleware-config` の中
で、開発モード (``debug`` で表される) が true にセットされているときだ
け使用されるミドルウェアを切り換えるために使用されています。


.. Production Configuration Files

.. _production-config:

プロダクション設定ファイル
==============================

.. To change the defaults of the configuration INI file that should be
.. used when deploying the application, edit the
.. :file:`config/deployment.ini_tmpl` file. This is the file that will
.. be used as a template during deployment, so that the person
.. handling deployment has a starting point of the minimum options the
.. application needs set.

アプリケーションをデプロイするときに使用される設定 INI ファイルのデフォ
ルトを変えるには、 :file:`config/deployment.ini_tmpl` ファイルを編集し
てください。このファイルはデプロイの際にテンプレートとして使用されて、
デプロイを行う人にとってアプリケーションに設定する必要のある最小限のオ
プションの出発点となります。


.. One of the most important options set in the deployment ini is the
.. ``debug = true`` setting. The email options should be setup so that
.. errors can be e-mailed to the appropriate developers or webmaster
.. in the event of an application error.

deployment ini で設定される中で最も重要なオプションの 1 つは、 ``debug
= true`` という設定です。アプリケーションエラーが発生した場合に適切な開
発者またはウェブ管理者にメールが送られるように、メールオプションがセッ
トアップされるべきです。


.. Generating the Production Configuration

プロダクション設定を生成する
---------------------------------------

.. To generate the production.ini file from the projects'
.. :file:`config/deployment.ini_tmpl` it must first be installed
.. either as an :term:`egg` or under development mode. Assuming the
.. name of the Pylons application is ``helloworld``, run:

プロジェクトの :file:`config/deployment.ini_tmpl` から production.ini
を生成するには、それを最初に :term:`egg` として、または開発モードでイン
ストールしなければなりません。 Pylons アプリケーションの名前が
``helloworld`` であるとすると、以下を実行してください:


.. code-block :: bash

    $ paster make-config helloworld production.ini


.. note::

    .. This command will also work from inside the project when its
    .. being developed.

    このコマンドは、開発中のプロジェクトの中からでも実行できます。


.. It is the responsibility of the developer to ensure that a sensible
.. set of default configuration values exist when the webmaster uses
.. the ``paster make-config`` command.

ウェブ管理者が ``paster make-config`` コマンドを使用したときに適切なデ
フォルト設定値が存在することを保証するのは、開発者の責任です。


.. warning::

    .. **Always** make sure that the ``debug`` is set to ``false``
    .. when deploying a Pylons application.

    **常に** Pylons アプリケーションをデプロイするときは、確実に
    ``debug`` を ``false`` に設定するようにしてください。


.. _environment-config:

*********************
環境 (Environment)
*********************

.. The :file:`config/environment.py` module sets up the basic Pylons
.. environment variables needed to run the application. Objects that
.. should be setup once for the entire application should either be
.. setup here, or in the :file:`lib/app_globals` :meth:`__init__`
.. method.

:file:`config/environment.py` モジュールは、アプリケーションを実行する
のに必要とされる基本的な Pylons 環境変数をセットアップします。アプリケー
ション全体のために一度だけセットアップされるオブジェクトは、ここか、も
しくは :file:`lib/app_globals` の :meth:`__init__` メソッドでセットアッ
プすべきです。


.. It also calls the :ref:`url-config` function to setup how the URL's
.. will be matched up to :ref:`controllers`, creates the
.. :term:`app_globals` object, configures which module will be
.. referred to as :term:`h`, and is where the template engine is
.. setup.

それはまた、 URL がどのように :ref:`controllers` とマッチされるかをセッ
トアップする :ref:`url-config` 関数を呼び出します。そして
:term:`app_globals` オブジェクトを作り、どのモジュールが :term:`h` とし
て参照できるようになるかを設定します。さらに、テンプレートエンジンがセッ
トアップされる場所でもあります。


.. When using SQLAlchemy it's recommended that the SQLAlchemy engine
.. be setup in this module. The default SQLAlchemy configuration that
.. Pylons comes with creates the engine here which is then used in
.. :file:`model/__init__.py`.

SQLAlchemy を使用するとき、このモジュールで SQLAlchemy エンジンをセット
アップすることが推奨されます。 Pylons のデフォルトの SQLAlchemy 設定で
はここでエンジンが作成されます。そのエンジンは後に
:file:`model/__init__.py` で使用されます。


.. URL Configuration

.. _url-config:

*****************
URL 設定
*****************

.. A Python library called Routes handles mapping URLs to controllers
.. and their methods, or their :term:`action` as Routes refers to
.. them. By default, Pylons sets up the following :term:`route`\s
.. (found in :file:`config/routing.py`):

Routes と呼ばれる Python ライブラリが、 URL からコントローラとそのメソッ
ド (Routes はそれを :term:`action` と呼びます) へのマッピングを扱います。
デフォルトで、 Pylons は以下の :term:`route` をセットアップします (それ
らは :file:`config/routing.py` で見つかります):


.. code-block:: python

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')


    .. Prior to Routes 1.9, all map.connect statements required
    .. variable parts to begin with a ``:`` like
    .. ``map.connect(':controller/:action')``. This syntax is now
    .. optional, and the new ``{}`` syntax is recommended.

.. versionchanged:: 0.9.7
    Routes 1.9 より前は、 ``map.connect(':controller/:action')`` のよう
    に、すべての map.connect 文が ``:`` で始まる可変部分を必要としてい
    ました。現在この構文はオプションであり、新しい ``{}`` 構文が推奨さ
    れます。


.. Any part of the path inside the curly braces is a variable (a
.. `variable part` ) that will match any text in the URL for that
.. 'part'. A 'part' of the URL is the text between two forward
.. slashes. Every part of the URL must be present for the
.. :term:`route` to match, otherwise a 404 will be returned.

すべての中括弧の内側のパス部分は、その '部分' が URL 内のどんなテキスト
にもマッチする変数 (`可変部分`) です。 URLの '部分' とは、 2つのスラッ
シュの間のテキストのことです。 URL のすべての部分が :term:`route` にマッ
チしなければ、 404 が返されます。


.. The routes above are translated by the Routes library into regular
.. expressions for high performance URL matching. By default, all the
.. variable parts (except for the special case of ``{controller}``)
.. become a matching regular expression of ``[^/]+`` to match anything
.. except for a forward slash. This can be changed easily, for example
.. to have the ``{id}`` only match digits:

上記の route は、高性能な URL マッチングのために Routes ライブラリによっ
て正規表現に変換されます。デフォルトで、すべての可変部分は、
(``{controller}`` の特別な場合を除いて) スラッシュ以外の全ての文字とマッ
チするように ``[^/]+`` という正規表現になります。これは簡単に変えること
ができて、例えば ``{id}`` が数字だけにマッチするようにするには、このよ
うにします:


.. code-block :: python
    
    map.connect('/{controller}/{action}/{id:\d+}')


.. If the desired regular expression includes the ``{}``, then it
.. should be specified separately for the variable part. To limit the
.. ``{id}`` to only match at least 2-4 digits:

正規表現が ``{}`` を含んでいるなら、それを可変部分とは別に指定しなけれ
ばなりません。 ``{id}`` が 2-4 桁の数字にしかマッチしないように制限する
ためには:


.. code-block :: python
    
    map.connect('/{controller}/{action}/{id}',  requirements=dict(id='\d{2,4}'))


.. The controller and action can also be specified as keyword
.. arguments so that they don't need to be included in the URL:

また、キーワード引数としてコントローラとアクションを指定することができ、
その場合にはそれらが URL に含まれている必要はありません:


.. code-block :: python
    
    # Archives by 2 digit year -> /archives/08
    map.connect('/archives/{year:\d\d}', controller='articles',  action='archives')


.. Any variable part, or keyword argument in the ``map.connect``
.. statement will be available for use in the action used. For the
.. route above, which resolves to the `articles` controller:

``map.connect`` 文における可変部分、またはキーワード引数は、アクション
の中で利用することが可能です。上の route の場合、 `article` コントロー
ラに解決されます:


.. code-block :: python
    
    class ArticlesController(BaseController):

        def archives(self, year):
            ...


.. The part of the URL that matched as the year is available by name
.. in the function argument.

year とマッチした URL 部分は、関数引数の中で名前によって参照できます。


.. note::

    .. Routes also includes the ability to attempt to 'minimize' the
    .. URL. This behavior is generally not intuitive, and starting in
    .. Pylons 0.9.7 is turned off by default with the
    .. ``map.minimization=False`` setting.

    Routes は、 URLの '最小化' 機能も含んでいます。 この振舞いは一般に
    直感的でなく、 Pylons 0.9.7 からは ``map.minimization=False`` 設定
    によって、デフォルトでオフになっています。


.. The default mapping can match to any controller and any of their
.. actions which means the following URLs will match:

デフォルトのマッピングは、あらゆるコントローラのあらゆるアクションにマッ
チします。これは以下の URL がマッチすることを意味します:


.. code-block:: text

    /hello/index       >>    controller: hello, action: index
    /entry/view/4      >>    controller: entry, action: view, id:4
    /comment/edit/2    >>    controller: comment, action: edit, id:2


.. This simple scheme can be suitable for even large applications when
.. complex URL's aren't needed.

複雑な URL が必要でない場合、この簡単な方法は大規模なアプリケーションに
さえ適していることがあります。


.. Controllers can be organized into directories as well. For example,
.. if the admins should have a separate ``comments`` controller:

また、コントローラをディレクトリにまとめることができます。例えば管理画
面用に別の ``comments`` コントローラが必要なら:


.. code-block:: bash
    
    $ paster controller admin/comments


.. Will create the ``admin`` directory along with the appropriate
.. ``comments`` controller under it. To get to the comments
.. controller:

これにより ``admin`` ディレクトリの下に適切な ``comments`` コントローラ
が作成されます。 comments コントローラに到達するために:


.. code-block:: text
    
    /admin/comments/index    >>    controller: admin/comments, action: index


.. note::

    .. The ``{controller}`` match is special, in that it doesn't
    .. always stop at the next forward slash (``/``). As the example
    .. above demonstrates, it is able to match controllers nested
    .. under a directory should they exist.

    ``{controller}`` マッチは特別です。というのも、次のスラッシュ
    (``/``) で常に停止するわけではないからです。上記の例が示すように、
    それはディレクトリの下に入れ子になったコントローラとマッチします。


.. Adding a route to match ``/``

``/`` にマッチする route を追加する
=======================================

.. The controller and action can be specified directly in the
.. :meth:`map.connect` statement, as well as the raw URL to be
.. matched.

:meth:`map.connect` 文において、生の URL がマッチするのと同時に、コント
ローラとアクションを直接指定することができます:


.. code-block:: python

    map.connect('/', controller='main', action='index')


.. results in ``/`` being handled by the ``index`` method of the
.. ``main`` controller.

これにより、 ``/`` が ``main`` コントローラの ``index`` メソッドで扱わ
れるようになります。


.. .. note::
..     By default, projects' static files (in the :file:`public/`
..     directory) are served in preference to controllers. New Pylons
..     projects include a welcome page (:file:`public/index.html`)
..     that shows up at the ``/`` url. You'll want to remove this file
..     before mapping a route there.

.. note::

    デフォルトでは、 プロジェクトの静的 (:file:`public/` ディレクトリの
    中の) ファイルはコントローラよりも優先されます。新しい Pylons プロ
    ジェクトは ``/`` URL で表示されるウェルカムページ
    (:file:`public/index.html`) を含んでいるので、ルーティング設定をす
    る前にこのファイルを取り除いた方が良いでしょう。


.. Generating URLs

URL を生成する
===============

.. URLs are generated via the callable
.. :class:`routes.util.URLGenerator` object. Pylons provides an
.. instance of this special object at :data:`pylons.url`. It accepts
.. keyword arguments indicating the desired controller, action and
.. additional variables defined in a route.

URL は callable な :class:`routes.util.URLGenerator` オブジェクトを通し
て生成されます。Pylons は :data:`pylons.url` でこの特別なオブジェクトの
インスタンスを提供します。このオブジェクトはキーワード引数として route
で定義されたコントローラ、アクション、および追加の変数を受け取ります。


.. code-block:: python
    
    # generates /content/view/2
    url(controller='content', action='view', id=2)   


.. To generate the URL of the matched route of the current request,
.. call :meth:`routes.util.URLGenerator.current`:

現在のリクエストにマッチする route の URL を生成するには、
:meth:`routes.util.URLGenerator.current` をこのように呼んでください:


.. code-block:: python

    # Generates /content/view/3 during a request for /content/view/3
    url.current()


.. :meth:`routes.util.URLGenerator.current` also accepts the same
.. arguments as `url()`. This uses `Routes memory
.. <http://routes.groovie.org/manual.html#route-memory>`_ to generate
.. a small change to the current URL without the need to specify all
.. the relevant arguments:

:meth:`routes.util.URLGenerator.current` は ``url()`` と同じ引数を受け
取ります。これは、関連するすべての引数を指定することなく現在の URL に対
する小さな変更を生成するために `Routes memory
<http://routes.groovie.org/manual.html#route-memory>`_ を使用します。


.. code-block:: python

    # Generates /content/view/2 during a request for /content/view/3
    url.current(id=2)


.. seealso::

    .. `Routes manual <http://routes.groovie.org/manual.html>`_
    .. Full details and source code.

    `Routes manual <http://routes.groovie.org/manual.html>`_
    完全な詳細とソースコード。


.. _middleware-config:

************
ミドルウェア
************

.. A projects WSGI stack should be setup in the
.. :file:`config/middleware.py` module. Ideally this file should
.. import middleware it needs, and set it up in the `make_app`
.. function.

プロジェクト WSGI スタックは :file:`config/middleware.py` モジュールで
セットアップされます。観念的に、このファイルは必要とするミドルウェアを
インポートして、 `make_app` 関数でそれをセットアップします。


.. The default stack that is setup for a Pylons application is
.. described in detail in :ref:`wsgi-middleware`.

Pylons アプリケーションのためのセットアップであるデフォルトスタックは
:ref:`wsgi-middleware` で詳細に説明されます。


.. Default middleware stack:

デフォルトミドルウェアスタック:


.. code-block :: python

    # The Pylons WSGI app
    app = PylonsApp()
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    
    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])

    # Establish the Registry for this application
    app = RegistryManager(app)

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        app = Cascade([static_app, app])

    return app

    
.. Since each piece of middleware wraps the one before it, the stack
.. needs to be assembled in reverse order from the order in which its
.. called. That is, the very last middleware that wraps the WSGI
.. Application, is the very first that will be called by the server.

それぞれのミドルウェアはそれより前のものをラップするので、スタックはそ
れが呼ばれる順の逆順で組み立てられる必要があります。 すなわち、 WSGI
Application をラップする最後のミドルウェアは、サーバによって最初に呼ば
れます。


.. The last piece of middleware in the stack, called Cascade, is used
.. to serve static content files during development. For top
.. performance, consider disabling the Cascade middleware via setting
.. the ``static_files = false`` in the configuration file. Then have
.. the webserver or a :term:`CDN` serve static files.

スタックの中のミドルウェアの最後の断片は Cascade と呼ばれ、開発の間、静
的な内容ファイルを返すのに使用されます。最高の性能のためには、設定ファ
イルの中で ``static_files = false`` と設定することで Cascade ミドルウェ
アを無効にすることを考慮してください。そして、ウェブサーバあるいは
:term:`CDN` が静的なファイルを返します。


.. warning::

    .. When unsure about whether or not to change the middleware,
    .. **don't**. The order of the middleware is important to the
    .. proper functioning of a Pylons application, and shouldn't be
    .. altered unless needed.

    ミドルウェアを変更するかどうか自信がなければ、 **変更しないでくださ
    い** 。ミドルウェアの順番は Pylons アプリケーションが適切に機能する
    ために重要であり、必要でない場合には変更するべきではありません。


.. Adding custom middleware

カスタムミドルウェアを追加する
================================

.. Custom middleware should be included in the
.. :file:`config/middleware.py` at comment marker:

カスタムミドルウェアは :file:`config/middleware.py` のコメントマーカー
のところに追加します:


.. code-block:: python

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)


.. For example, to add a middleware component named `MyMiddleware`,
.. include it in :file:`config/middleware.py`:

例えば、 `MyMiddleware` というミドルウェア・コンポーネントを加える場合、
:file:`config/middleware.py` でそれを含めてください:


.. code-block:: python

    # The Pylons WSGI app
    app = PylonsApp()
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    app = MyMiddleware(app)

    
.. The app object is simply passed as a parameter to the
.. `MyMiddleware` middleware which in turn should return a wrapped
.. WSGI application.

app オブジェクトは単にパラメタとして `MyMiddleware` ミドルウェアに渡さ
れ、それは順次ラップされた WSGI アプリケーションを返します。


.. Care should be taken when deciding in which layer to place custom
.. middleware. In most cases middleware should be placed before the
.. Pylons WSGI application and its supporting Routes/Session/Cache
.. middlewares, however if the middleware should run *after* the
.. CacheMiddleware:

カスタムミドルウェアをどの層の中に置くか決めるときは注意が必要です。 多
くの場合、ミドルウェアは Pylons WSGI アプリケーションとそれをサポートす
る Routes/Session/Cache ミドルウェアの前に置かれるべきですが、そのミド
ルウェアが CacheMiddleware の *後に* 実行すべきなら、このようにします:


.. code-block:: python

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    
    # MyMiddleware can only see the cache object, nothing *above* here
    app = MyMiddleware(app)
    
    app = CacheMiddleware(app, config)


.. What is full_stack?

full_stack とは何か
===================

.. In the Pylons ini file {:file:`development.ini` or
.. :file:`production.ini`} this block determines if the flag
.. full_stack is set to true or false::

Pylons iniファイル (:file:`development.ini` または
:file:`production.ini`) では、このブロックで full_stack フラグが true
にセットされているか false にセットされているかを調べます::


    [app:main]
    use = egg:app_name
    full_stack = true


.. The full_stack flag determines if the ErrorHandler and
.. StatusCodeRedirect is included as a layer in the middleware
.. wrapping process. The only condition in which this option would be
.. set to `false` is if multiple Pylons applications are running and
.. will be wrapped in the appropriate middleware elsewhere.

full_stack フラグは、ミドルウェアをラップするプロセスの中に
ErrorHandler とStatusCodeRedirect が層として含まれているかどうか決定し
ます。このオプションが `false` に設定される唯一の状況は、複数の Pylons
アプリケーションが走っていて、他の場所で適切なミドルウェアによってラッ
プされる場合です。


.. _setup-config:

*******************************
アプリケーション・セットアップ
*******************************

.. There are two kinds of 'Application Setup' that are occasionally
.. referenced with regards to a project using Pylons.

Pylons を使用するプロジェクトに関して、言及されることのある 'アプリケー
ション・セットアップ' には 2 種類あります。


.. * Setting up a new application
.. * Configuring project information and package dependencies

* 新しいアプリケーションをセットアップする
* プロジェクト情報とパッケージの依存を設定する


.. Setting Up a New Application

新しいアプリケーションをセットアップする
========================================

.. To make it easier to setup a new instance of a project, such as
.. setting up the basic database schema, populating necessary
.. defaults, etc. a setup script can be created.

プロジェクトの新しいインスタンスをより簡単にセットアップできるように、
基本的なデータベース・スキーマをセットアップしたり、必要なデフォルト値
を生成したりといった、セットアップ・スクリプトを作成できます。


.. In a Pylons project, the setup script to be run is located in the
.. projects' :file:`websetup.py` file. The default script loads the
.. projects configuration to make it easier to write application setup
.. steps:

Pylons プロジェクトでは、実行されるセットアップ・スクリプトはプロジェク
トの :file:`websetup.py` ファイルに配置されています。アプリケーション・
セットアップ手順をより簡単に書けるように、デフォルトのスクリプトはプロ
ジェクト設定を読み込みます:


.. code-block :: python
    
    import logging

    from helloworld.config.environment import load_environment

    log = logging.getLogger(__name__)

    def setup_app(command, conf, vars):
        """Place any commands to setup helloworld here"""
        load_environment(conf.global_conf, conf.local_conf)


.. note::

    .. If the project was configured during creation to use SQLAlchemy
    .. this file will include some commands to setup the database
    .. connection to make it easier to setup database tables.

    プロジェクトが作成される際に SQLAlchemy を使用するように設定された
    なら、このファイルはより簡単にデータベースのテーブルをセットアップ
    できるように、データベース接続をセットアップするいくつかのコマンド
    を含むでしょう。


.. To run the setup script using the development configuration:

開発設定を使用してセットアップ・スクリプトを実行するには:


.. code-block :: bash
    
    $ paster setup-app development.ini


.. Configuring the Package

パッケージを設定する
=======================

.. A newly created project with Pylons is a standard Python
.. package. As a Python package, it has a :file:`setup.py` file that
.. records meta-information about the package. Most of the options in
.. it are fairly self-explanatory, the most important being the
.. 'install_requires' option:

Pylons を用いて新たに作成されたプロジェクトは標準の Python パッケージで
す。 Python パッケージなので、パッケージのメタ情報を記録する
:file:`setup.py` ファイルがあります。そのオプションの大部分はかなり一目
瞭然ですが、最も重要なオプションは 'install_requires' です:


.. code-block :: python
    
    install_requires=[
        "Pylons>=0.9.7",
    ],

    
.. These lines indicate what packages are required for the proper
.. functioning of the application, and should be updated as needed. To
.. re-parse the :file:`setup.py` line for new dependencies:

これらの行は、アプリケーションの適切な機能のためにどんなパッケージが必
要かを表し、必要に応じてそれらをアップデートすべきであることを表します。
新しい依存性のために :file:`setup.py` 行を再解析するには:


.. code-block :: bash

    $ python setup.py develop


.. In addition to updating the packages as needed so that the
.. dependency requirements are made, this command will ensure that
.. this package is active in the system (without requiring the
.. traditional :command:`python setup.py install`).

このコマンドは、依存性の要求が満たされるように必要に応じてパッケージを
アップデートすることに加えて、パッケージがシステムで確実にアクティブに
なるようにします (伝統的な :command:`python setup.py install` を必要と
せずに)。


.. seealso::
    `Declaring Dependencies <http://peak.telecommunity.com/DevCenter/setuptools#declaring-dependencies>`_
