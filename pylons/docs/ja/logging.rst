.. _logging:

==========
ログの出力
==========

.. Logging messages 

ログにメッセージを出力する
--------------------------

.. As of Pylons 0.9.6, Pylons controllers (created via ``paster
.. controller/restcontroller``) and ``websetup.py`` create their own
.. Logger objects via `Python's logging module
.. <http://docs.python.org/lib/module-logging.html>`_.

Pylons 0.9.6 からは、 Pylons コントローラ (``paster
controller/restcontroller`` で作成されたもの) と ``websetup.py`` は、
`Python の logging モジュール
<http://docs.python.org/lib/module-logging.html>`_ を通して自身の
Logger オブジェクトを作るようになります。


.. For example, in the helloworld project's hello controller
.. (``helloworld/controllers/hello.py``):

例えば、 helloworld プロジェクトの hello コントローラ
(``helloworld/controllers/hello.py``) ではこのようになります:


.. code-block:: python 

    import logging 

    from pylons import request, response, session, tmpl_context as c
    from pylons.controllers.util import abort, redirect_to

    log = logging.getLogger(__name__) 

    class HelloController(BaseController): 

        def index(self): 
            ...


.. Python's special ``__name__`` variable refers to the current module's
.. fully qualified name; in this case, ``helloworld.controllers.hello``.

Python の特殊変数 ``__name__`` は現在のモジュールの完全修飾された名前を
参照します。この場合は ``helloworld.controllers.hello`` です。


.. To log messages, simply use methods available on that Logger
.. object:

メッセージをログ出力するには、単に Logger オブジェクトで利用できるメソッ
ドを使うだけです。


.. code-block:: python 

    import logging 

    from pylons import request, response, session, tmpl_context as c
    from pylons.controllers.util import abort, redirect_to

    log = logging.getLogger(__name__) 

    class HelloController(BaseController): 

        def index(self): 
            content_type = 'text/plain' 
            content = 'Hello World!' 

            log.debug('Returning: %s (content-type: %s)', content, content_type) 
            response.content_type = content_type 
            return content 


.. Which will result in the following printed to the console, on
.. stderr:

これは標準エラーに以下の出力を行います (コンソールに出力されます):


.. code-block:: text 

    16:20:20,440 DEBUG [helloworld.controllers.hello] Returning: Hello World!
                       (content-type: text/plain) 


.. Basic Logging configuration 

基本的な logging の設定
---------------------------
 
.. As of Pylons 0.9.6, the default ini files include a basic
.. configuration for the logging module. Paste ini files use the Python
.. standard `ConfigParser format
.. <http://docs.python.org/lib/module-ConfigParser.html>`_; the same
.. format used for the Python `logging module's Configuration file format
.. <http://docs.python.org/lib/logging-config-fileformat.html>`_.

Pylons 0.9.6 からはデフォルトの ini ファイルに logging モジュール用の基
本的な設定が含まれています。 Paste の ini ファイルは Python の標準的な
`ConfigParser フォーマット
<http://docs.python.org/lib/module-ConfigParser.html>`_ を使います;
`logging モジュールの設定ファイルフォーマット
<http://docs.python.org/lib/logging-config-fileformat.html>`_ も同じ
フォーマットを使います。


.. ``paster``, when loading an application via the ``paster`` ``serve``,
.. ``shell`` or ``setup-app`` commands, calls the `logging.fileConfig
.. function <http://docs.python.org/lib/logging-config-api.html>`_ on
.. that specified ini file if it contains a 'loggers'
.. entry. ``logging.fileConfig`` reads the logging configuration from a
.. ``ConfigParser`` file.

``paster`` は、 ``serve``, ``shell``, ``setup-app`` の各コマンドによっ
てアプリケーションをロードする際に、指定された ini ファイルが
'loggers' エントリを含んでいれば `logging.fileConfig 関数
<http://docs.python.org/lib/logging-config-api.html>`_ を呼び出します。
``logging.fileConfig`` は ``ConfigParser`` ファイルから logging 設定を
読み込みます。


.. Logging configuration is provided in both the default
.. ``development.ini`` and the production ini file (created via ``paster
.. make-config <package_name> <ini_file>``). The production ini's logging
.. setup is a little simpler than the ``development.ini``'s, and is as
.. follows:

logging 設定はデフォルトの ``development.ini`` と (``paster
make-config <package_name> <ini_file>`` で作られる) プロダクション ini
ファイルの両方で提供されます。プロダクション ini ファイルの logging セッ
トアップは ``development.ini`` より少し単純で、次のようになります:


.. code-block:: ini 

    # Logging configuration 
    [loggers] 
    keys = root 

    [handlers] 
    keys = console 

    [formatters] 
    keys = generic 

    [logger_root] 
    level = INFO 
    handlers = console 

    [handler_console] 
    class = StreamHandler 
    args = (sys.stderr,) 
    level = NOTSET 
    formatter = generic 

    [formatter_generic] 
    format = %(asctime)s %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s 


.. One root Logger is created that logs only messages at a level above or
.. equal to the ``INFO`` level to stderr, with the following format:

一つのルートロガーが作られ、 ``INFO`` レベル以上のメッセージのみを標準
エラーに出力するようになります。フォーマットは以下のようになります:


.. code-block:: text 

    2007-08-17 15:04:08,704 INFO [helloworld.controllers.hello] Loading resource, id: 86 


.. For those familiar with the ``logging.basicConfig`` function, this
.. configuration is equivalent to the code:

``logging.basicConfig`` 関数のことをよく知っている人にとっては、この設
定は以下のコードと等価です:


.. code-block:: python 

    logging.basicConfig(level=logging.INFO, 
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s') 


.. The default ``development.ini``'s logging section has a couple of
.. differences: it uses a less verbose timestamp, and defaults your
.. application's log messages to the ``DEBUG`` level (described in the
.. next section).

デフォルトの ``development.ini`` の logging セクションは、 2 つの点で異
なっています。 より冗長でないタイムスタンプを使うことと、アプリケーショ
ンのログメッセージをデフォルトで ``DEBUG`` レベルとすることです。 (次の
セクションで記述されます)


.. Pylons and many other libraries (such as Beaker, SQLAlchemy, Paste)
.. log a number of messages for debugging purposes. Switching the root
.. Logger level to ``DEBUG`` reveals them:

Pylons と他のたくさんのライブラリ (Beaker, SQLAlchemy, Paste など) はデ
バッグ目的のために大量のメッセージを出力します。ルートロガーのレベルを
``DEBUG`` に変更するとそれが明らかになります:


.. code-block:: ini 

    [logger_root] 
    #level = INFO 
    level = DEBUG 
    handlers = console 


.. Filtering log messages

ログメッセージのフィルタリング
--------------------------------

.. Often there's too much log output to sift through, such as when
.. switching the root Logger's level to ``DEBUG``.

ルートロガーのレベルを ``DEBUG`` に変更した場合など、しばしば取捨選択で
きないほどたくさんのログ出力が行われることがあります。


.. An example: you're diagnosing database connection issues in your
.. application and only want to see SQLAlchemy's ``DEBUG`` messages in
.. relation to database connection pooling. You can leave the root
.. Logger's level at the less verbose ``INFO`` level and set that
.. particular SQLAlchemy Logger to ``DEBUG`` on its own, apart from
.. the root Logger:

例: あなたは、アプリケーションにおけるデータベース接続の問題を診断して
いて、コネクションプーリングに関連した SQLAlchemy の ``DEBUG`` メッセー
ジだけを見たいと思っています。ルートロガーのレベルを、それほど冗長でな
い ``INFO`` レベルのままにしておき、ルートロガートとは別に特定の
SQLAlchemy のロガーを ``DEBUG`` に設定できます:


.. code-block:: ini 

    [logger_sqlalchemy.pool] 
    level = DEBUG 
    handlers = 
    qualname = sqlalchemy.pool 


.. then add it to the list of Loggers: 

次にこれをロガーのリストに追加します:


.. code-block:: ini 

    [loggers] 
    keys = root, sqlalchemy.pool 


.. No Handlers need to be configured for this Logger as by default non
.. root Loggers will propagate their log records up to their parent
.. Logger's Handlers. The root Logger is the top level parent of all
.. Loggers.

このロガーのために Handlers を構成する必要はありません。ルート以外のロ
ガーは、デフォルトでログレコードを親のロガーの Handlers に伝播するから
です。ルートロガーはすべてのロガーのトップレベルの親です。


.. This technique is used in the default ``development.ini``. The root
.. Logger's level is set to ``INFO``, whereas the application's log
.. level is set to ``DEBUG``:

このテクニックはデフォルトの ``development.ini`` で使用されています。ルー
トロガーのレベルは ``INFO`` に設定される一方で、アプリケーションのログ
レベルは ``DEBUG`` に設定されます:


.. code-block:: ini 

    # Logging configuration 
    [loggers] 
    keys = root, helloworld 


.. code-block:: ini 

    [logger_helloworld] 
    level = DEBUG 
    handlers = 
    qualname = helloworld 


.. All of the child Loggers of the helloworld Logger will inherit the
.. ``DEBUG`` level unless they're explicitly set differently. Meaning the
.. ``helloworld.controllers.hello``, ``helloworld.websetup`` (and all
.. your app's modules') Loggers by default have an effective level of
.. ``DEBUG`` too.

明示的に異なる設定がされていない限り、 helloworld ロガーの子供ロガーの
すべてが ``DEBUG`` レベルを引き継ぐことになります。 つまり、
``helloworld.controllers.hello``, ``helloworld.websetup`` (そしてアプリ
ケーションの他のモジュールの) ロガーも、デフォルトで実効レベル
``DEBUG`` になります。


.. For more advanced filtering, the logging module provides a `Filter
.. <http://docs.python.org/lib/node423.html>`_ object; however it
.. cannot be used directly from the configuration file.

より高度なフィルタリングのために、 logging モジュールは `Filter
<http://docs.python.org/lib/node423.html>`_ オブジェクトを提供していま
す。ただし Filter オブジェクトを設定ファイルから直接使用することはでき
ません。


.. Advanced Configuration 

高度な構成
----------------------

.. To capture log output to a separate file, use a `FileHandler
.. <http://docs.python.org/lib/node412.html>`_ (or a
.. `RotatingFileHandler <http://docs.python.org/lib/node413.html>`_):

ログ出力を個別のファイルに記録するためには、 `FileHandler
<http://docs.python.org/lib/node412.html>`_ (または
`RotatingFileHandler <http://docs.python.org/lib/node413.html>`_) を使
います:


.. code-block:: ini 

    [handler_accesslog] 
    class = FileHandler 
    args = ('access.log','a') 
    level = INFO 
    formatter = generic 


.. Before it's recognized, it needs to be added to the list of
.. Handlers:

それが認識される前に、 Handlers のリストに追加される必要があります:


.. code-block:: ini 

    [handlers] 
    keys = console, accesslog 


.. and finally utilized by a Logger. 

最後にロガーによって使われます。


.. code-block:: ini 

    [logger_root] 
    level = INFO 
    handlers = console, accesslog 


.. These final 3 lines of configuration directs all of the root Logger's
.. output to the access.log as well as the console; we'll want to disable
.. this for the next section.

この最後の 3 行の構成が、ルートロガーの出力のすべてをコンソールに加えて
access.log に向けます。次のセクションではこれを無効にしたいと思うでしょう。


.. Request logging with Paste's TransLogger 

Paste の TransLogger によるリクエストログ
-----------------------------------------

.. Paste provides the `TransLogger
.. <http://pythonpaste.org/module-paste.translogger.html>`_ middleware
.. for logging requests using the `Apache Combined Log Format
.. <http://httpd.apache.org/docs/2.2/logs.html#combined>`_. TransLogger
.. combined with a FileHandler can be used to create an ``access.log``
.. file similar to Apache's.

Paste は `Apache Combined Log Format
<http://httpd.apache.org/docs/2.2/logs.html#combined>`_ を使ってリクエ
ストを記録するための `TransLogger
<http://pythonpaste.org/module-paste.translogger.html>`_ ミドルウェアを
提供しています。 FileHandler と TransLogger を組み合わせると、 Apache
のログファイルのような ``access.log`` を作成することができます。


.. Like any standard middleware with a Paste entry point, TransLogger
.. can be configured to wrap your application in the ``[app:main]``
.. section of the ini file:

Paste エントリーポイントを持つ他の標準的なミドルウェアと同様に、 ini ファ
イルの ``[app:main]`` セクションでアプリケーションをラップするように
TransLogger を構成できます:


.. code-block:: ini 

    filter-with = translogger 

    [filter:translogger] 
    use = egg:Paste#translogger 
    setup_console_handler = False 


.. This is equivalent to wrapping your app in a TransLogger instance
.. via the bottom of your project's ``config/middleware.py`` file:

これは、プロジェクトの ``config/middleware.py`` ファイルの最後でアプリ
ケーションを TransLogger インスタンスでラップするのと同等です:


.. code-block:: python 

    from paste.translogger import TransLogger 
    app = TransLogger(app, setup_console_handler=False) 
    return app 


.. TransLogger will automatically setup a logging Handler to the
.. console when called with no arguments, so it 'just works' in
.. environments that don't configure logging. Since we've configured
.. our own logging Handlers, we need to disable that option via
.. ``setup_console_handler = False``.

TransLogger は、引数なしで呼ばれると自動的に logging Handler をコンソー
ルに設定するので、 logging を構成しない環境でもそのままで動きます
('just works')。 私たちは自身の logging Handlers を構成したので、
``setup_console_handler = False`` によってそのオプションを無効にする必
要があります。


.. With the filter in place, TransLogger's Logger (named the 'wsgi'
.. Logger) will propagate its log messages to the parent Logger (the
.. root Logger), sending its output to the console when we request a
.. page:

フィルタが適切な場所にあると、ページがリクエストされたときに
TransLogger のロガー ('wsgi' ロガーという名前になります) は親ロガー (ルー
トロガー) にログメッセージを伝播し、その出力はコンソールに送られます:


.. code-block:: text 

    00:50:53,694 INFO [helloworld.controllers.hello] Returning: Hello World!
                      (content-type: text/plain) 
    00:50:53,695 INFO [wsgi] 192.168.1.111 - - [11/Aug/2007:20:09:33 -0700] "GET /hello
    HTTP/1.1" 404 - "-" 
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.6) Gecko/20070725
    Firefox/2.0.0.6" 


.. To direct TransLogger to the ``access.log`` FileHandler defined
.. above, we need to add that FileHandler to the wsgi Logger's list of
.. Handlers:

TransLogger を上で定義された ``access.log`` FileHandler に向けるために、
wsgi ロガーの Handlers リストにその FileHandler を追加する必要がありま
す:


.. code-block:: ini 

    # Logging configuration 
    [loggers] 
    keys = root, wsgi 


.. code-block:: ini 

    [logger_wsgi] 
    level = INFO 
    handlers = handler_accesslog 
    qualname = wsgi 
    propagate = 0 


.. As mentioned above, non-root Loggers by default propagate their log
.. Records to the root Logger's Handlers (currently the console
.. Handler). Setting ``propagate`` to 0 (false) here disables this; so
.. the ``wsgi`` Logger directs its records only to the ``accesslog``
.. Handler.

前述のように、ルート以外のロガーはデフォルトでルートロガーの Handlers
(現在はコンソール Handler) にログレコードを伝播します。ここで
``propagate`` を 0 (false) に設定すると、これを無効にできます。そのため、
``wsgi`` ロガーは ``accesslog`` Handler だけに記録を向けます。


.. Finally, there's no need to use the ``generic`` Formatter with
.. TransLogger as TransLogger itself provides all the information we
.. need. We'll use a Formatter that passes-through the log messages as
.. is:

TransLogger 自身が必要とするすべての情報を提供するので、最終的に、
TransLogger と共に ``generic`` Formatter を使用する必要は全くありません。
ログメッセージをそのまま素通しする Formatter を使用することにします:


.. code-block:: ini 

    [formatters] 
    keys = generic, accesslog 


.. code-block:: ini 

    [formatter_accesslog] 
    format = %(message)s 


.. Then wire this new ``accesslog`` Formatter into the FileHandler: 

次に、この新しい ``accesslog`` Formatter を FileHandler に接続してくだ
さい:


.. code-block:: ini 

    [handler_accesslog] 
    class = FileHandler 
    args = ('access.log','a') 
    level = INFO 
    formatter = accesslog 


.. Logging to wsgi.errors 

wsgi.errors に対するログ出力
-----------------------------

.. Pylons provides a custom logging Handler class,
.. `pylons.log.WSGIErrorsHandler
.. <http://pylonshq.com/docs/class-pylons.log.WSGIErrorsHandler.html>`_,
.. for logging output to ``environ['wsgi.errors']``: the WSGI server's
.. error stream (see the `WSGI Spefification, PEP 333
.. <http://www.python.org/dev/peps/pep-0333/>`_ for more
.. information). ``wsgi.errors`` can be useful to log to in certain
.. situations, such as when deployed under Apache mod_wsgi/mod_python,
.. where the ``wsgi.errors`` stream is the Apache error log.

Pylons は WSGI サーバのエラーストリーム ``environ['wsgi.errors']`` (詳
しくは `WSGI Spefification, PEP 333
<http://www.python.org/dev/peps/pep-0333/>`_ を参照) にログ出力するため
のカスタムな logging Handler クラス `pylons.log.WSGIErrorsHandler
<http://pylonshq.com/docs/class-pylons.log.WSGIErrorsHandler.html>`_ を
提供しています。 ``wsgi.errors`` は特定の状況、例えば Apache
mod_wsgi/mod_python のもとでデプロイされているような場合には、ログ出力
に便利です。その場合、 ``wsgi.errors`` ストリームは、Apache エラーログ
です。


.. To configure logging of only ``ERROR`` (and ``CRITICAL``) messages
.. to ``wsgi.errors``, add the following to the ini file:

``ERROR`` (と ``CRITICAL``) メッセージだけを ``wsgi.errors`` にログ出力
するように構成するには、 ini ファイルに以下を追加してください:


.. code-block:: ini 

    [handlers] 
    keys = console, wsgierrors 


.. code-block:: ini 

    [handler_wsgierrors] 
    class = pylons.log.WSGIErrorsHandler 
    args = () 
    level = ERROR 
    format = generic 


.. then add the new Handler name to the list of Handlers used by the
.. root Logger:

次に、 ルートロガーによって使用される Handlers のリストに新しい
Handler 名を追加してください:


.. code-block:: ini 

    [logger_root] 
    level = INFO 
    handlers = console, wsgierrors 


.. warning :: 

    .. ``WSGIErrorsHandler`` does not receive log messages created
    .. during application startup. This is due to the ``wsgi.errors``
    .. stream only being available through the ``environ`` dictionary;
    .. which isn't available until a request is made.

    ``WSGIErrorsHandler`` はアプリケーションを開始する間に作成されたロ
    グメッセージを受け取りません。 これは ``wsgi.errors`` ストリームは
    ``environ`` 辞書を通してのみ利用可能だからです。リクエストがあるま
    でそれは利用可能ではありません。


.. Lumberjacking with log4j's Chainsaw 

log4j の Chainsaw による lumberjacking
---------------------------------------

.. Java's ``log4j`` project provides the Java GUI application
.. `Chainsaw <http://logging.apache.org/log4j/docs/chainsaw.html>`_
.. for viewing and managing log messages. Among its features are the
.. ability to filter log messages on the fly, and customizable color
.. highlighting of log messages.

Java の ``log4j`` プロジェクトは、ログメッセージを表示したり管理したり
するために Java GUI アプリケーション `Chainsaw
<http://logging.apache.org/log4j/docs/chainsaw.html>`_ を提供しています。
その特徴として、 on the fly でログメッセージをフィルタリングする機能、
およびカスタマイズ可能なカラーハイライトがあります。


.. We can configure Python's logging module to output to a format
.. parsable by Chainsaw, ``log4j``'s `XMLLayout
.. <http://logging.apache.org/log4j/docs/api/org/apache/log4j/xml/XMLLayout.html>`_
.. format.

Python の logging モジュールを、 Chainsaw でパース可能な形式
(``log4j`` の `XMLLayout
<http://logging.apache.org/log4j/docs/api/org/apache/log4j/xml/XMLLayout.html>`_
形式) で出力するように構成できます。


.. To do so, we first need to install the `Python XMLLayout package
.. <http://pypi.python.org/pypi/XMLLayout>`_:

それをするために、最初に `Python XMLLayout package
<http://pypi.python.org/pypi/XMLLayout>`_ をインストールする必要があり
ます:


.. code-block:: bash 

    $ easy_install XMLLayout 


.. It provides a log Formatter that generates ``XMLLayout`` XML. It
.. also provides ``RawSocketHandler``; like the logging module's
.. ``SocketHandler``, it sends log messages across the network, but
.. does not pickle them.

このモジュールは ``XMLLayout`` XML を生成するログフォーマッタを提供しま
す。 また、 ``RawSocketHandler`` を提供します。それは、 logging モジュー
ルの ``SocketHandler`` のようにネットワークの向こう側にログメッセージを
送りますが、それらを pickle しません。


.. The following is an example configuration for sending ``XMLLayout``
.. log messages across the network to Chainsaw, if it were listening
.. on `localhost` port `4448`:

以下は、 ``XMLLayout`` ログメッセージをネットワーク経由で Chainsaw
(`localhost` の `4448` ポート で listen している場合) へ送付するための
構成例です:


.. code-block:: ini 

    [handlers] 
    keys = console, chainsaw 

    [formatters] 
    keys = generic, xmllayout 

    [logger_root] 
    level = INFO 
    handlers = console, chainsaw 


.. code-block:: ini 

    [handler_chainsaw] 
    class = xmllayout.RawSocketHandler 
    args = ('localhost', 4448) 
    level = NOTSET 
    formatter = xmllayout 


.. code-block:: ini 

    [formatter_xmllayout] 
    class = xmllayout.XMLLayout 


.. This configures any log messages handled by the root Logger to also
.. be sent to Chainsaw. The default ``development.ini`` configures the
.. root Logger to the ``INFO`` level, however in the case of using
.. Chainsaw, it is preferable to configure the root Logger to
.. ``NOTSET`` so *all* log messages are sent to Chainsaw. Instead, we
.. can restrict the console handler to the ``INFO`` level:

これは、ルートロガーによって扱われたすべてのログメッセージを Chainsaw
に送るように構成します。デフォルトの ``development.ini`` はルートロガー
を ``INFO`` レベルに構成しますが、 Chainsaw を使用する場合はルートロガー
を ``NOTSET`` に構成して *すべての* ログメッセージを Chainsaw に送るの
が望ましいでしょう。代わりに、コンソールハンドラを ``INFO`` レベルに制
限することができます:


.. code-block:: ini 

    [logger_root] 
    level = NOTSET 
    handlers = console 

    [handler_console] 
    class = StreamHandler 
    args = (sys.stderr,) 
    level = INFO 
    formatter = generic 


.. Chainsaw can be downloaded from its `home page
.. <http://logging.apache.org/log4j/docs/chainsaw.html>`_, but can
.. also be launched directly from a Java-enabled browser via the link:
.. `Chainsaw web start
.. <http://logging.apache.org/log4j/docs/webstart/chainsaw/chainsawWebStart.jnlp>`_.

Chainsaw は `ホームページ
<http://logging.apache.org/log4j/docs/chainsaw.html>`_ からダウンロード
できますが、 Java が有効なブラウザで以下のリンクから直接実行することも
できます: `Chainsaw web start
<http://logging.apache.org/log4j/docs/webstart/chainsaw/chainsawWebStart.jnlp>`_.


.. It can be configured from the GUI, but it also supports reading its
.. configuration from a ``log4j.xml`` file.

Chainsaw は GUI から構成することもできますが、 ``log4j.xml`` ファイルか
ら構成を読み込むこともサポートしています。


.. The following ``log4j.xml`` file configures Chainsaw to listen on port
.. `4448` for ``XMLLayout`` style log messages. It also hides Chainsaw's
.. own logging messages under the ``WARN`` level, so only your app's log
.. messages are displayed:

以下の ``log4j.xml`` ファイルは、ポート `4448` で ``XMLLayout`` スタイ
ルのログメッセージを listen するように Chainsaw を構成します。また、
``WARN`` レベルより下の Chainsaw 自身のログメッセージを隠すので、あなた
のアプリケーションのログメッセージだけを表示します:


.. code-block:: xml 

    <?xml version="1.0" encoding="UTF-8" ?> 
    <!DOCTYPE configuration> 
    <configuration xmlns="http://logging.apache.org/"> 

    <plugin name="XMLSocketReceiver" class="org.apache.log4j.net.XMLSocketReceiver"> 
        <param name="decoder" value="org.apache.log4j.xml.XMLDecoder"/> 
        <param name="port" value="4448"/> 
    </plugin> 

    <logger name="org.apache.log4j"> 
        <level value="warn"/> 
    </logger> 

    <root> 
        <level value="debug"/> 
    </root> 

    </configuration> 


.. Chainsaw will prompt for a configuration file upon startup. The
.. configuration can also be loaded later by clicking `File`/`Load
.. Log4J File...`. You should see an XMLSocketReceiver instance loaded
.. in Chainsaw's Receiver list, configured at port `4448`, ready to
.. receive log messages.

Chainsaw は開始時に構成ファイルについてのプロンプトを表示します。また、
`File`/`Load Log4J File...` をクリックすることで、後で構成をロードする
こともできます。 Chainsaw の Receiver リストに XMLSocketReceiver インス
タンスがロードされているのが見られるはずです。それはポート `4448` で構
成されて、ログメッセージを受け取る準備ができています。


.. Here's how the Pylons stack's log messages can look with colors
.. defined (using Chainsaw on OS X):

これは、 Pylons スタックのログメッセージが定義済みの色でどのように見え
るかを示しています (OS X で Chainsaw を使用):


.. image:: _static/Pylons_Stack-Chainsaw-OSX.png 
    :width: 750px
    :height: 469px


.. Alternate Logging Configuration style

ログ出力設定の別のスタイル
-------------------------------------

.. Pylons' default ini files include a basic configuration for
.. Python's logging module. Its format matches the standard Python
.. :mod:`logging` module's `config file format
.. <http://docs.python.org/lib/logging-config-fileformat.html>`_. If a
.. more concise format is preferred, here is Max Ischenko's
.. demonstration of an alternative style to setup logging.

Pylons のデフォルト ini ファイルは Python の logging モジュールのための
基本構成を含んでいます。 そのフォーマットは標準 Python :mod:`logging`
モジュールの `設定ファイルフォーマット
<http://docs.python.org/lib/logging-config-fileformat.html>`_ に適合し
ています。より簡潔なフォーマットが好みなら、 Max Ischenko が実証したロ
グ出力設定の別のスタイルがあります。


.. The following function is called at the application start up
.. (e.g. Global ctor):

以下の関数はアプリケーション開始時に呼ばれます (例えば、Global コンスト
ラクタ):


.. code-block:: python

    def setup_logging():
        logfile = config['logfile']
        if logfile == 'STDOUT': # special value, used for unit testing
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                   #format='%(name)s %(levelname)s %(message)s',
                   #format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                   format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                   datefmt='%H:%M:%S')
        else:
            logdir = os.path.dirname(os.path.abspath(logfile))
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            logging.basicConfig(filename=logfile, mode='at+',
                 level=logging.DEBUG,
                 format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                 datefmt='%Y-%b-%d %H:%M:%S')
        setup_thirdparty_logging()


.. The setup_thirdparty_logging function searches through the certain
.. keys of the application ``.ini`` file which specify logging level
.. for a particular logger (module).

setup_thirdparty_logging 関数は、アプリケーション ``.ini`` ファイルから
特定の logger (モジュール) に logging レベルを指定するキーを検索します。


.. code-block:: python

    def setup_thirdparty_logging():
        for key in config:
            if not key.endswith('logging'):
                continue
            value = config.get(key)
            key = key.rstrip('.logging')
            loglevel = logging.getLevelName(value)
            log.info('Set %s logging for %s', logging.getLevelName(loglevel), key)
            logging.getLogger(key).setLevel(loglevel)


.. Relevant section of the .ini file (example):

.ini ファイルの関連セクション (例):


.. code-block:: ini

    sqlalchemy.logging = WARNING
    sqlalchemy.orm.unitofwork.logging = INFO
    sqlalchemy.engine.logging = DEBUG
    sqlalchemy.orm.logging = INFO
    routes.logging = WARNING


.. This means that routes logger (and all sub-loggers such as
.. routes.mapper) only passes through messages of at least WARNING
.. level; sqlalachemy defaults to WARNING level but some loggers are
.. configured with more verbose level to aid debugging.

これは routes logger (そして routes.mapper などのすべての sub-logger)
が WARNING レベル以上のメッセージのみを通すことを表しています。
sqlalachemy はデフォルトで WARNING レベルですが、いくつかの logger は
デバッグを支援するためにより冗長なレベルによって構成されています。
