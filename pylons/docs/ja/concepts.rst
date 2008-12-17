.. _concepts:

.. Concepts of Pylons

======================
Pylons のコンセプト
======================

.. Understanding the basic concepts of Pylons, the flow of a request
.. and response through the stack and how Pylons operates makes it
.. easier to customize when needed, in addition to clearing up
.. misunderstandings about why things behave the way they do.

Pylons に関する基本コンセプトや、スタックを通したリクエストとレスポンス
の流れ、および Pylons がどのように作動するかを理解することは、ものごと
がなぜそのように振る舞うのかに関する誤解を解決することに加えて、必要な
際にはカスタマイズすることがより簡単になります。


.. This section acts as a basic introduction to the concept of a
.. :term:`WSGI` application, and :term:`WSGI Middleware` in addition
.. to showing how Pylons utilizes them to assemble a complete working
.. web framework.

このセクションは :term:`WSGI` アプリケーションと :term:`WSGI
Middleware` のコンセプトへの基本的な introduction として機能します。そ
して、Pylons が完全に動作するウェブフレームワークを組み立てるのにそれら
をどのように利用するかを示します。


.. To follow along with the explanations below, create a project
.. following the :ref:`getting_started` Guide.

以下の説明を読み進める際には、 :ref:`getting_started` ガイドに従ってプ
ロジェクトを作成してください。


.. The 'Why' of a Pylons Project

*****************************
Pylons プロジェクトの 'Why'
*****************************

.. A new Pylons project works a little differently than in many other
.. web frameworks. Rather than loading the framework, which then finds
.. a new projects code and runs it, Pylons creates a Python package
.. that does the opposite. That is, when its run, it imports objects
.. from Pylons, assembles the WSGI Application and stack, and returns
.. it.

新しい Pylons プロジェクトは、他の多くのウェブフレームワークと少し異な
る動作をします。フレームワークをロードする (そして、新しいプロジェクト
コードを見つけてそれを実行する) のではなく、 Pylons はその正反対をする
Python パッケージを作成します。すなわち、それは実行されると Pylons から
オブジェクトをインポートして、 WSGI アプリケーションとスタックを組み立
てて、それを返します。


.. If desired, a new project could be completely cleared of the Pylons
.. imports and run any arbitrary WSGI application instead. This is
.. done for a greater degree of freedom and flexibility in building a
.. web application that works the way the developer needs it to.

望むなら、新しいプロジェクトでは Pylons インポートを完全に除去してしま
い、代わりにどんな任意の WSGI アプリケーションを実行しても構いません。
これは、開発者が必要とする方法で動作するウェブアプリケーションを組み立
てることにおけるより大きな自由度と柔軟性のためです。


.. By default, the project is configured to use standard components
.. that most developers will need, such as sessions, template engines,
.. caching, high level request and response objects, and an
.. :term:`ORM`. By having it all setup in the project (rather than
.. hidden away in 'framework' code), the developer is free to tweak
.. and customize as needed.

デフォルトでは、プロジェクトはほとんどの開発者が必要とする標準コンポー
ネント、例えばセッションや、テンプレートエンジンや、キャッシュや、高レ
ベルのリクエストおよびレスポンスオブジェクトや、 :term:`ORM` などを使用
するように構成されます。すべてのセットアップが ('フレームワーク' コード
に遠く隠されているのではなく) プロジェクトの中にあることにより、開発者
は必要に応じてそれを自由に調整やカスタマイズができます。


.. In this manner, Pylons has setup a project with its *opinion* of
.. what may be needed by the developer, but the developer is free to
.. use the tools needed to accomplish the projects goals. Pylons
.. offers an unprecedented level of customization by exposing its
.. functionality through the project while still maintaining a
.. remarkable amount of simplicity by retaining a single standard
.. interface between core components (:term:`WSGI`).

このように、 Pylons は開発者によって必要とされるかもしれないものに関す
る *意見* を伴ってプロジェクトをセットアップしますが、開発者はプロジェ
クトの目標を達成するために必要なツールを自由に使用できます。 Pylons は、
プロジェクトを通してその機能を露出することによって、前例のないカスタマ
イズのレベルを提供する一方、コア構成要素の間でただ一つの標準インター
フェース (:term:`WSGI`) を retain することによって、今もなお
remarkable amount of simplicity を維持しています。


.. WSGI Applications

*********************
WSGI アプリケーション
*********************

.. WSGI is a basic specification known as :pep:`333`, that describes a
.. method for interacting with a HTTP server. This involves a way to
.. get access to HTTP headers from the request, and how set HTTP
.. headers and return content on the way back out.

WSGI は、 :pep:`333` として知られる、HTTP サーバと対話するための方法を
記述する基本仕様です。これは、リクエストから HTTP ヘッダにアクセスする
方法と、HTTP ヘッダをどのようにセットして、内容をどのように返すかという
ことに関係します。


.. A 'Hello World' WSGI Application:

'Hello World' WSGI アプリケーション:


.. code-block :: python
    
    def simple_app(environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return ['<html><body>Hello World</body></html>']


.. This WSGI application does nothing but set a 200 status code for
.. the response, set the HTTP 'Content-type' header, and return some
.. HTML.

この WSGI アプリケーションは、レスポンスに 200 ステータスコードを設定し
て、 HTTP 'Content-type' ヘッダーを設定して、多少の HTML を返す以外、何
もしていません。


.. The WSGI specification lays out a `set of keys that will be set in
.. the environ dict
.. <http://www.python.org/dev/peps/pep-0333/#environ-variables>`_.

WSGI 仕様は `environ 辞書にセットされるキーの集合
<http://www.python.org/dev/peps/pep-0333/#environ-variables>`_ を定めて
います。


.. The WSGI interface, that is, this method of calling a function (or
.. method of a class) with two arguments, and handling a response as
.. shown above, is used throughout Pylons as a standard interface for
.. passing control to the next component.

WSGI インタフェース、すなわち上に示されるように 2 引数の関数 (または、
クラスのメソッド) を呼んでレスポンスを扱うというこの方法は、制御を次の
コンポーネントに渡すための標準インターフェースとして、 Pylons のいたる
ところで使用されています。


.. Inside a new projects :file:`config/middleware.py`, the `make_app`
.. function is responsible for creating a WSGI application, wrapping
.. it in WSGI middleware (explained below) and returning it so that it
.. may handle requests from a HTTP server.

新しいプロジェクトの :file:`config/middleware.py` の中では、 WSGI アプ
リケーションを作成し、それを WSGI ミドルウェア (以下で説明されます) で
ラップして、 HTTP サーバからのリクエストを扱うことができるようにそれを
返すことに対して `make_app` 関数が責任を持ちます。


.. WSGI Middleware

.. _wsgi-middleware:

*******************
WSGI ミドルウェア
*******************

.. Within :file:`config/middleware.py` a Pylons application is wrapped
.. in successive layers which add functionality. The process of
.. wrapping the Pylons application in middleware results in a
.. structure conceptually similar to the layers in an onion.

:file:`config/middleware.py` の中では、 Pylons アプリケーションは機能性
を加える連続した層でラップされます。 Pylons アプリケーションをミドルウェ
アでラップするプロセスは、概念的にたまねぎの中の層と同様の構造をもたら
します。


.. image:: _static/pylons_as_onion.png
   :alt: Pylons middleware onion analogy
   :align: center


.. Once the middleware has been used to wrap the Pylons application,
.. the make_app function returns the completed app with the following
.. structure (outermost layer listed first):

ミドルウェアがいったん Pylons アプリケーションをラップするのに使用され
ると、 make_app 関数は以下の構造を持つ完成したアプリケーションを返しま
す (最外の層が最初に記載されています):


.. code-block:: text

    Registry Manager
        Status Code Redirect
            Error Handler
                Cache Middleware
                    Session Middleware
                        Routes Middleware
                            Pylons App (WSGI Application)


.. WSGI middleware is used extensively in Pylons to add functionality
.. to the base WSGI application. In Pylons, the 'base' WSGI
.. Application is the :class:`~pylons.wsgiapp.PylonsApp`. It's
.. responsible for looking in the `environ` dict that was passed in
.. (from the Routes Middleware).

WSGI ミドルウェアは、ベースの WSGI アプリケーションに機能性を追加するた
めに Pylons で幅広く使用されます。 Pylonsでは、 'ベース' WSGI アプリケー
ションは :class:`~pylons.wsgiapp.PylonsApp` です。それは (Routes
Middleware から) 渡される `environ` 辞書の中を looking in することに責
任を持ちます。


.. To see how this functionality is created, consider a small class
.. that looks at the `HTTP_REFERER` header to see if its Google:

この機能がどのように作成されるかを理解するために、 `HTTP_REFERER` ヘッ
ダーを見てそれが Google かどうかを調べる小さなクラスを考えてください:


.. code-block :: python
    
    class GoogleRefMiddleware(object):
        def __init__(self, app):
            self.app = app
        
        def __call__(self, environ, start_response):
            environ['google'] = False
            if 'HTTP_REFERER' in environ:
                if environ['HTTP_REFERER'].startswith('http://google.com'):
                    environ['google'] = True
            return self.app(environ, start_response)


.. This is considered WSGI Middleware as it still can be called and
.. returns like a WSGI Application, however, it's adding something to
.. environ, and then calls a WSGI Application that it is initialized
.. with. That's how the layers are built up in the `WSGI Stack` that
.. is configured for a new Pylons project.

これは WSGI アプリケーションのように呼ばれ、戻り値を返すことができるの
で、 WSGI ミドルウェアであるとみなすことができますが、それは environ に
何かを加えてから、初期化時に渡された WSGI アプリケーションを呼び出しま
す。新しい Pylons プロジェクトのために構成される `WSGI スタック` では、
このようにして層が確立されます。


.. Some of the layers, like the Session, Routes, and Cache middleware,
.. only add objects to the `environ` dict, or add HTTP headers to the
.. response (the Session middleware for example adds the session
.. cookie header). Others, such as the Status Code Redirect, and the
.. Error Handler may fully intercept the request entirely, and change
.. how its responded to.

Session, Routes, Cache ミドルウェアのようないくつかの層は、単に
`environ` 辞書にオブジェクトを加えるか、またはレスポンスに HTTP ヘッダ
を加えるだけです (例えば、 Session ミドルウェアはセッションクッキーヘッ
ダーを加えます)。 Status Code Redirect や、 Error Handler などの他のミ
ドルウェアは、リクエストを横取りして、そのレスポンスのしかたを全く変え
てしまうこともあります。


.. Controller Dispatch

*************************
コントローラディスパッチ
*************************

.. When the request passes down the middleware, the incoming URL gets
.. parsed in the RoutesMiddleware, and if it matches a URL (See
.. :ref:`url-config`), the information about the controller that
.. should be called is put into the `environ` dict for use by
.. :class:`~pylons.wsgiapp.PylonsApp`.

リクエストがミドルウェアを伝わるとき、入って来た URL は
RoutesMiddleware で分析されます。そして、それが URL とマッチした場合は
(:ref:`url-config` を見てください) :class:`~pylons.wsgiapp.PylonsApp`
で使用するため、呼び出すべきコントローラの情報が `environ` 辞書に入れら
れます。


.. The :class:`~pylons.wsgiapp.PylonsApp` then attempts to find a
.. controller in the :file:`controllers` directory that matches the
.. name of the controller, and searches for a class inside it by a
.. similar scheme (controller name + 'Controller', ie,
.. HelloController). Upon finding a controller, its then called like
.. any other WSGI application using the same WSGI interface that
.. :class:`~pylons.wsgiapp.PylonsApp` was called with.

:class:`~pylons.wsgiapp.PylonsApp` は次に、コントローラを見つけようとし
ます。 :file:`controllers` ディレクトリでコントローラの名前と一致するファ
イルを探し、その中で同様のスキーム (コントローラ名 + 'Controller' 、こ
の場合は HelloController) に従ってクラスを検索します。コントローラが見
つかると、それは他の WSGI アプリケーションと全く同じように、
:class:`~pylons.wsgiapp.PylonsApp` が呼び出されるのと同様の WSGI インタ
フェースで呼び出されます。


.. This is why the BaseController that resides in a projects
.. :file:`lib/base.py` module inherits from
.. :class:`~pylons.controllers.core.WSGIController` and has a
.. `__call__` method that takes the `environ` and
.. `start_response`. The
.. :class:`~pylons.controllers.core.WSGIController` locates a method
.. in the class the corresponds to the `action` that Routes found,
.. calls it, and returns the response completing the request.

これが、プロジェクトの :file:`lib/base.py` モジュールに置かれている
BaseController が WSGIController から派生している理由であり、
`environ` と `start_response` を受け取る `__call__` メソッドを持ってい
る理由です。 WSGIController は、 Routes が見つけた `action` に対応する
メソッドの場所をクラスの中で見つけ、それを呼び出してリクエストを完了す
るレスポンスを返します。


******
Paster
******

.. Running the :command:`paster` command all by itself will show the
.. sets of commands it accepts:

:command:`paster` コマンドを何の引数も付けずに単独で実行すると、受け付
けるコマンドの集合が表示されます:


.. code-block :: bash
    
    $ paster
    Usage: paster [paster_options] COMMAND [command_options]

    Options:
      --version         show program's version number and exit
      --plugin=PLUGINS  Add a plugin to the list of commands (plugins are Egg
                        specs; will also require() the Egg)
      -h, --help        Show this help message

    Commands:
      create          Create the file layout for a Python distribution
      grep            Search project for symbol
      help            Display help
      make-config     Install a package and create a fresh config file/directory
      points          Show information about entry points
      post            Run a request for the described application
      request         Run a request for the described application
      serve           Serve the described application
      setup-app       Setup an application, given a config file

    pylons:
      controller      Create a Controller and accompanying functional test
      restcontroller  Create a REST Controller and accompanying functional test
      shell           Open an interactive shell with the Pylons app loaded


.. If :command:`paster` is run inside of a Pylons project, this should
.. be the output that will be printed. The last section, `pylons` will
.. be absent if it is not run inside a Pylons project. This is due to
.. a dynamic plugin system the :command:`paster` script uses, to
.. determine what sets of commands should be made available.

:command:`paster` が Pylons プロジェクトの中で実行された場合、出力結果
はこのようになるはずです。最後のセクション `pylons` は、 Pylons プロジェ
クトの中で実行しなければ存在しないでしょう。これは、 :command:`paster`
スクリプトが利用可能なコマンドを決定するために使用する、ダイナミックな
プラグインシステムのためです。


.. Inside a Pylons project, there is a directory ending in
.. `.egg-info`, that has a :file:`paster_plugins.txt` file in it. This
.. file is looked for and read by the :command:`paster` script, to
.. determine what other packages should be searched dynamically for
.. commands. Pylons makes several commands available for use in a
.. Pylons project, as shown above.

Pylons プロジェクトの中には、 `.egg-info` で終わるディレクトリがあり、
その中に :file:`paster_plugins.txt` ファイルがあります。このファイルは
:command:`paster` スクリプトによって検索され読み込まれます。そして、他
のどんなパッケージからコマンドを動的に検索すべきかを決定するために使わ
れます。上で示されるように、 Pylons でもいくつかのコマンドが提供されて
いて、 Pylons プロジェクトで使えるようになっています。


.. Loading the Application

*************************
アプリケーションのロード
*************************

.. Running (and thus loading) an application is done using the
.. :command:`paster` command:

アプリケーションを実行する (したがってロードする) には、
:command:`paster` コマンドが使用されます。


.. code-block :: bash
    
    $ paster serve development.ini


.. This instructs the paster script to go into a 'serve' mode. It will
.. attempt to load both a server and a WSGI application that should be
.. served, by parsing the configuration file specified. It looks for a
.. `[server]` block to determine what server to use, and an `[app]`
.. block for what WSGI application should be used.

これは、 paster スクリプトに 'serve' モードに入るよう指定します。
paster は指定された構成ファイルを構文解析して、サーバとサーブすべき
WSGI アプリケーションの両方をロードすることを試みるでしょう。それは
`[server]` ブロックを見てどんなサーバを使用するかを決定します。そして
`[app]` ブロックを見てどの WSGI アプリケーションを使用すればよいかを決
定します。


.. The basic egg block in the :file:`development.ini` for a
.. `helloworld` project:

`helloworld` プロジェクトのための :file:`development.ini` の中の基本的
な egg ブロック:


.. code-block :: ini
    
    [app:main]
    use = egg:helloworld


.. That will tell paster that it should load the helloworld
.. :term:`egg` to locate a WSGI application. A new Pylons application
.. includes a line in the :file:`setup.py` that indicates what
.. function should be called to make the WSGI application:

これは WSGI アプリケーションの場所を見つけるために helloworld
:term:`egg` を読み込むことを paster に伝えます。新しい Pylons アプリケー
ションでは、 WSGI アプリケーションを作るためにどんな関数が呼ばれるかを
示す行が :file:`setup.py` にあります:


.. code-block :: python
    
    entry_points="""
    [paste.app_factory]
    main = helloworld.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,


.. Here, the `make_app` function is specified as the `main` WSGI
.. application that Paste (the package that :command:`paster` comes
.. from) should use.

ここでは Paste (:command:`paster` を提供しているパッケージ) が使用すべ
き `main` WSGI アプリケーションとして `make_app` 関数が指定されています。


.. The `make_app` function from the project is then called, and the
.. server (by default, a HTTP server) runs the WSGI application.

その後プロジェクトの `make_app` 関数が呼ばれて、サーバ (デフォルトで、
HTTP サーバ) が WSGI アプリケーションを実行します。
