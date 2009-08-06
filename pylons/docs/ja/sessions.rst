.. _sessions:

==========
セッション
==========

セッション
==========

.. .. note::
..     The session code is due an extensive rewrite. It uses the Caching
..     container API in Beaker which is optimized for use patterns that
..     are more common in caching (infrequent updates / frequent
..     reads). Unlike caching, a session is a single load, then a single
..     save and multiple simultaneous writes to the same session occur
..     only rarely. In consequence, the excessive but necessary locking
..     that the cache interface currently performs is just a waste of
..     performance where sessions are concerned.

.. note::

    セッションコードは大幅な書き直しが必要です。それはキャッシングにお
    いてより一般的な使用パターン (たまにしかないアップデート/頻繁な読み
    取り) に最適化された Beaker の Caching コンテナ API を使用していま
    す。キャッシュとは異なり、セッションは一度だけロードされ、そして一
    度だけ保存されます。そして同じセッションに対して複数の書き込みが同
    時に起こることはめったにありません。そのため、現在のキャッシュイン
    タフェースが行う過剰な、しかし必要なロックは、セッションに関しては
    単なる性能の浪費です。


.. Session Objects

セッションオブジェクト
======================

SessionObject
-------------

.. This session proxy / lazy creator object handles access to the real
.. session object. If the session hasn't been used before a session
.. object will automatically be created and set up. Using a proxy in this
.. fashion to handle access to the real session object avoids creating
.. and loading the session from persistent store unless it is actually
.. used during the request.

このセッションプロキシ/遅延作成オブジェクトは、本物のセッションオブジェ
クトへのアクセスを処理します。セッションがそれまでに使用されたことがな
ければ、セッションオブジェクトは自動的に作成されてセットアップされます。
本物のセッションオブジェクトへのアクセスを扱うのにこのようなやり方でプ
ロキシを使用するのは、リクエストの間にセッションが実際に使用されない場
合に、セッションを作成して永続的なストレージからロードするのを避けるた
めです。


CookieSession
-------------

.. Pure cookie-based session. The options recognized when using
.. cookie-based sessions are slightly more restricted than general
.. sessions.

純粋なクッキーベースのセッション。クッキーベースのセッションを使用する
際に認識されるオプションは、一般的なセッションよりわずかに制限されてい
ます。

    
* ``key``

    .. The name the cookie should be set to.

    クッキーにセットされる名前。

* ``timeout``

    .. How long session data is considered valid. This is used regardless
    .. of the cookie being present or not to determine whether session
    .. data is still valid.

    セッションデータがどの程度の期間有効とみなすか。これはクッキーが存
    在しているかどうかにかかわらず、セッションデータがまだ有効であるか
    どうかを決定するために使用されます。

* ``encrypt_key``

    .. The key to use for the session encryption, if not provided the
    .. session will not be encrypted.

    セッション暗号化のために使用するキー。指定しなければセッションは暗
    号化されません。

* ``validate_key``

    .. The key used to sign the encrypted session

    暗号化されたセッションに署名するために使用されるキー。

* ``cookie_domain``

    .. Domain to use for the cookie.

    クッキーに使用するドメイン。

* ``secure``

    .. Whether or not the cookie should only be sent over SSL.

    クッキーが SSL を通じてのみ送られるかどうか。


Beaker
======

.. code-block:: ini 

    beaker.session.key = wiki 
    beaker.session.secret = ${app_instance_secret} 


.. Pylons comes with caching middleware enabled that is part of the same
.. package that provides the session handling, `Beaker
.. <http://beaker.groovie.org>`_. Beaker supports several different types
.. of cache back-end: memory, filesystem, memcached and database. The
.. supported database packages are: SQLite, SQLAlchemy and Google
.. BigTable.

Pylons にはキャッシュミドルウェアが有効な状態で付属しています。それはセッ
ションの取り扱いを提供するのと同じパッケージである `Beaker
<http://beaker.groovie.org>`_ の一部です。 Beaker はいくつかの異なる種
類のキャッシュバックエンドをサポートします: メモリ, ファイルシステム,
memcached, そしてデータベースです。サポートされるデータベースパッケージ
は、 SQLite, SQLAlchemy, および Google BigTable です。


.. Beaker's cache and session options are configured via a dictionary.

Beaker のキャッシュとセッションオプションは辞書で構成されます。


.. note::

    .. When used with the Paste package, all Beaker options should be
    .. prefixed with ``beaker.`` so that Beaker can discriminate its
    .. options from other application configuration options.

    Paste パッケージと共に使用する場合、 Beaker が自身のオプションと他
    のアプリケーションの設定オプションを区別できるように、すべての
    Beaker オプションは ``beaker.`` プリフィックスをつけるべきです。


.. General Config Options

一般的な設定オプション
----------------------

.. Config options should be prefixed with either ``session.`` or
.. ``cache.``

設定オプションは ``session.`` または ``cache.`` プリフィックスをつける
べきです。


data_dir
^^^^^^^^

*Accepts:* string
*Default:* None


.. The data directory where cache data will be stored. If this argument
.. is not present, the regular data_dir parameter is used, with the path
.. "./sessions" appended to it.

キャッシュデータが保存されるデータディレクトリ。この引数が存在していな
いなら、通常の ``data_dir`` パラメータに "./sessions" を追加したものが
使用されます。


type
^^^^

*Accepts:* string
*Default:* dbm


.. Type of storage used for the session, current types are "dbm", "file",
.. "memcached", "database", and "memory". The storage uses the Container
.. API that is also used by the cache system.

セッションに使用されるストレージのタイプ。現在のタイプは "dbm",
"file", "memcached", "database", および "memory" です。ストレージはキャッ
シュシステムも使用する Container API を使用します。


.. When using dbm files, each user's session is stored in its own dbm
.. file, via the :class:`beaker.container.DBMNamespaceManager` class.

dbm ファイルを使用する場合、各ユーザのセッションは
:class:`beaker.container.DBMNamespaceManager` クラスを通してそれぞれ別
の dbm ファイルに保存されます。


.. When using 'database' or 'memcached', additional configuration options
.. are required as documented in the appropriate section below.

'database' または 'memcached' を使用する場合、以下の対応するセクション
で文書化されるように、追加の設定オプションが必要です。


.. For sessions only, there is an additional choice of a "cookie" type,
.. which requires the Sessions "secret" option to be set as well.

セッションオンリーには、 "cookie" タイプの追加選択があります。
それはセッションに "secret" オプションが設定されることを必要とします。


.. Database Configuration

データベース設定
----------------------

.. When the type is set to 'database', the following additional options
.. can be used.

タイプが 'database' にセットされているとき、以下の追加オプションを使用
できます。


url (*required*)
^^^^^^^^^^^^^^^^

.. *Accepts:* string (formatted as required for an `SQLAlchemy db uri`__)

*Accepts:* string (`SQLAlchemy db uri`__ と同じ書式)
*Default:* None

.. __: http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_establishing


.. The database URI as formatted for SQLAlchemy to use for the
.. database. The appropriate database packages for the database must also
.. be installed.

SQLAlchemy がデータベースに対して使用する書式と同様のデータベース URI 。
データベースのための適切なデータベースパッケージもインストールしなけれ
ばなりません。


table_name
^^^^^^^^^^

*Accepts:* string
*Default:* beaker_cache


.. Table name to use for beaker's storage.

Beaker のストレージに使用するテーブル名。


optimistic
^^^^^^^^^^

*Accepts:* boolean
*Default:* False


.. Use optimistic session locking, note that this will result in an
.. select when updating a cache value to compare version numbers.

楽観的なセッションロックを使用します。この場合、キャッシュ値をアップデー
トするときに、バージョン番号を比較するために select が行われることに注
意してください。


sa_opts (*Only for SQLAlchemy 0.3*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Accepts:* dict
*Default:* None


.. A dictionary of values that are passed directly to SQLAlchemy's
.. engine. Note that this is only applicable for SQLAlchemy 0.3.

SQLAlchemy のエンジンに直接渡される値の辞書。これは SQLAlchemy 0.3 に対
してのみ適切であることに注意してください。


sa.*
^^^^

.. *Accepts:* Valid `SQLAlchemy 0.4 database options`__

*Accepts:* 有効な `SQLAlchemy 0.4 データベースオプション`__
*Default:* None

.. __: http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_options


.. When using SQLAlchemy 0.4 and above, all options prefixed with ``sa.``
.. are passed to the SQLAlchemy database engine. Common parameters are
.. ``pool_size``, ``pool_recycle``, etc.

SQLAlchemy 0.4 以上を使用するとき、プリフィックスに ``sa.`` を持つすべ
てのオプションが SQLAlchemyデータベースエンジンに渡されます。 一般的な
パラメータは ``pool_size``, ``pool_recycle`` などです。


.. Memcached Options

memcached オプション
---------------------

url (required)
^^^^^^^^^^^^^^

*Accepts:* string
*Default:* None


.. The url should be a single IP address, or list of semi-colon separated
.. IP addresses that should be used for memcached.

url は memcached のための 単一の IP アドレスか、セミコロンで区切られた
IP アドレスのリストです。


.. Beaker can use either py-memcached or cmemcache to communicate with
.. memcached, but it should be noted that cmemcache can cause Python to
.. segfault should memcached become unreachable.

Beaker は memcached と通信するのに py-memcached または cmemcache のどち
らかを使用できますが、 cmemcache は memcached に接続できなくなったとき
に Python を segfault させることがあることに注意してください。


.. Session Options

セッションオプション
---------------------

cookie_expires
^^^^^^^^^^^^^^

*Accepts:* boolean, datetime, timedelta
*Default:* True


.. The expiration time to use on the session cookie. Defaults to "True"
.. which means, don't specify any expiration time (the cookie will expire
.. when the browser is closed). A value of "False" means, never expire
.. (specifies the maximum date that can be stored in a datetime object
.. and uses that). The value can also be a ``datetime.timedelta()``
.. object which will be added to the current date and time, or a
.. ``datetime.datetime()`` object.

セッションクッキーの有効期限。デフォルトは "True" で、有効期限を設定し
ません (ブラウザが閉じられたときにクッキーの期限が切れます)。 "False"
値は無期限を意味します (datetime オブジェクトに格納できる最大の日時を指
定して、それを使用します)。この値は現在時刻に加算される
``datetime.timedelta()`` オブジェクトまたは ``datetime.datetime()`` オ
ブジェクトにすることもできます。


cookie_domain
^^^^^^^^^^^^^

*Accepts:* string
*Default:* The entire domain name being used, including sub-domain, etc.


.. By default, Beaker's sessions are set to the cookie domain of the
.. entire hostname. For sub-domains, this should be set to the top domain
.. the cookie should be valid for.

デフォルトでは Beaker のセッションはクッキードメインとして完全なホスト
名が設定されます。サブドメインにおいてはこの値をクッキーを有効にしたい
トップドメインに設定する必要があります。


id
^^

*Accepts:* string
*Default:* None


.. Session id for this session. When using sessions with cookies, this
.. parameter is not needed as the session automatically creates, writes
.. and retrieves the value from the request. When using a URL-based
.. method for the session, the id should be retrieved from the id data
.. member when the session is first created, and then used in writing new
.. URLs.

このセッションのためのセッション id。 クッキーとともにセッションを使用
する場合、セッションはリクエストから自動的に値を作成、保存、取得するの
で、このパラメータは必要ありません。セッションに URL ベースの方法を使用
する場合、セッションが最初に作成されるときに id は id データメンバーか
ら取得され、次に新しい URL を出力する際に使用されます。


key
^^^

*Accepts:* string
*Default:* beaker_session_id


.. The key that will be used as a cookie key to identify
.. sessions. Changing this could allow several different applications to
.. have different sessions underneath the same hostname.

セッションを特定するためにクッキーのキーとして使用されるキー。これを変
えることで、いくつかの異なったアプリケーションが同じホスト名の下で異な
るセッションを持つことができます。


secret
^^^^^^

*Accepts:* string
*Default:* None


.. Secret key to enable encrypted session ids. When non-None, the session
.. ids are generated with an MD5-signature created against this value.

暗号化セッション id を有効にする秘密鍵。 None でないときに、セッション
id はこの値に対して作成された MD5 署名で生成されます。


.. When used with the "cookie" Session type, the secret is used for
.. encrypting the contents of the cookie, and should be a reasonably
.. secure randomly generated string of characters no more than 54
.. characters.

"cookie" セッションタイプで使用されると、 secret はクッキーの内容を暗号
化するために使用されます。十分にセキュアな、少なくとも 54 文字以上のラ
ンダムに生成された文字列にすべきです。


timeout
^^^^^^^

*Accepts:* integer
*Default:* None


.. Time in seconds before the session times out. A timeout occurs when
.. the session has not been loaded for more than timeout seconds.

セッションがタイムアウトするまでの秒数。セッションが timeout 秒以上ロー
ドされなかった場合、タイムアウトが起こります。


.. Session Options (For use with cookie-based Sessions)

セッションオプション (クッキーベースセッションを使う場合)
----------------------------------------------------------

encrypt_key
^^^^^^^^^^^

*Accepts:* string
*Default:* None


.. The key to use for the session encryption, if not provided the session
.. will not be encrypted. This will only work if a strong hash scheme is
.. available, such as pycryptopp's or Python 2.5's hashlib.sha256.

セッション暗号化に使用するキー。指定しなければセッションは暗号化されま
せん。これは pycryptopp や Python 2.5 の hashlib.sha256 のような強いハッ
シュスキームが利用可能である場合にだけ働きます。


validate_key
^^^^^^^^^^^^

*Accepts:* string
*Default:* None


.. The key used to sign the encrypted session, this is used instead of a
.. secret option.

暗号化されたセッションに署名するために使用されるキー。これは secret オ
プションの代わりに使用されます。


.. Custom and caching middleware

カスタムミドルウェア
=============================

.. Care should be taken when deciding in which layer to place custom
.. middleware. In most cases middleware should be placed between the
.. Pylons WSGI application instantiation and the Routes middleware;
.. however, if the middleware should run *before* the session object or
.. routing is handled::

カスタムミドルウェアをどのレイヤーに置くかを決める際には注意が必要です。
多くの場合、ミドルウェアは Pylons WSGI アプリケーションインスタンスと
Routes ミドルウェアの間に置かれるべきです。しかし、ミドルウェアがセッショ
ンオブジェクトやルーティングが扱われるより *前で* 実行する必要があるな
ら:


.. code-block:: python

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    
    # MyMiddleware can only see the cache object, nothing *above* here
    app = MyMiddleware(app)
    
    app = CacheMiddleware(app, config)


.. Some of the Pylons middleware layers such as the ``Session``,
.. ``Routes``, and ``Cache`` middleware, only add objects to the
.. `environ` dict, or add HTTP headers to the response (the Session
.. middleware for example adds the session cookie header). Others, such
.. as the ``Status Code Redirect``, and the ``Error Handler`` may fully
.. intercept the request entirely, and change how its responded to.

``Session``, ``Routes``, ``Cache`` ミドルウェアなどのいくつかの Pylons
ミドルウェア層は、単に `environ` 辞書にオブジェクトを加えるか、またはレ
スポンスに HTTP ヘッダを加えるだけです (例えば Session ミドルウェアはセッ
ションクッキーヘッダーを加えます)。一方、 ``Status Code Redirect`` や
``Error Handler`` は、リクエスト全体を完全に横取りして、そのレスポンス
を変えるかもしれません。


.. Bulk deletion of expired db-held sessions

db に保持されたセッションの bulk 削除
=========================================

.. The db schema for Session stores a "last accessed time" for each
.. session. This enables bulk deletion of expired sessions through the
.. use of a simple SQL command, run every day, that clears those sessions
.. which have a "last accessed" timestamp > 2 days, or whatever is
.. required.

Session のための db スキーマは、各セッションについて「最後にアクセスさ
れた時間」を格納します。これによって、簡単な SQL コマンドを使用すること
で期限切れのセッションの bulk 削除が可能になります。 SQL コマンドは毎日
実行され、「最後にアクセスされた」タイムスタンプが 2 日より前 (あるいは
その他の任意の条件で) 期限切れのセッションをクリアします。


.. Using `Session` in Internationalization

国際化に `Session` を使用する
=======================================

.. How to set the language used in a controller on the fly. 

コントローラで使用される言語を動的に (on the fly) 設定する方法。


.. For example this could be used to allow a user to set which language they 
.. wanted your application to work in. Save the value to the session object: 

例えばこれを使えば、ユーザがアプリケーションをどの言語で動かしたいか
設定できるようになります。セッションオブジェクトに値を保存してください:


.. code-block:: python 

    session['lang'] = 'en' 
    session.save() 


.. then on each controller call the language to be used could be read
.. from the session and set in the controller's ``__before__()`` method
.. so that the pages remained in the same language that was previously
.. set:

そうすると、各コントローラが呼び出された時にコントローラの
``__before__()`` メソッドでセッションから言語を読み込んで設定することに
よって、継続して設定された言語でページが表示されるようになります。

.. code-block:: python 

    def __before__(self): 
        if 'lang' in session: 
            set_lang(session['lang']) 


.. Using `Session` in Secure Forms

Secure Form で `Session` を使用する
===================================

.. Authorization tokens are stored in the client's session. The web app can then
.. verify the request's submitted authorization token with the value in the
.. client's session.

権限トークンはクライアントのセッションに格納されます。そして、ウェブア
プリは、送信されたリクエストの権限トークンをクライアントのセッションに
保存された値に対して検証することができます。


.. This ensures the request came from the originating page. See the
.. wikipedia entry for `Cross-site request forgery`__ for more
.. information.

これはリクエストが originating ページから来たことを保証します。 `クロス
サイト・リクエスト・フォージュリ`__ に関して詳しい情報は wikipedia のエ
ントリーを見てください。

.. http://en.wikipedia.org/wiki/Cross-site_request_forgery

.. __: http://ja.wikipedia.org/wiki/%E3%82%AF%E3%83%AD%E3%82%B9%E3%82%B5%E3%82%A4%E3%83%88%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%83%95%E3%82%A9%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%AA

.. Pylons provides an ``authenticate_form`` decorator that does this
.. verification on the behalf of controllers.

Pylons はコントローラに代わってこの検証を行う ``authenticate_form`` デ
コレータを提供しています。


.. These helpers depend on Pylons' ``session`` object.  Most of them can
.. be easily ported to another framework by changing the API calls.

これらの helpers は Pylons の ``session`` オブジェクトに依存しています。
それらの大部分は、 API 呼び出しを変えることによって容易に別のフレームワー
クに移植できるでしょう。


.. Hacking the session for no cookies

クッキーを使用しないセッションの hack
======================================

(From a `paste #441 <http://pylonshq.com/pasties/441>`_ baked by Ben Bangert)


.. Set the session to not use cookies in the dev.ini file

dev.ini ファイルでセッションにクッキーを使用しないように設定してください。


.. code-block:: ini 

    beaker.session.use_cookies = False


.. with this as the *mode d'emploi* in the controller action

そしてコントローラアクションの中で *mode d'emploi* (使用法、取扱説明書)
としてこのようにします:


.. code-block:: python

    from beaker.session import Session as BeakerSession

    # Get the actual session object through the global proxy
    real_session = session._get_current_obj()

    # Duplicate the session init options to avoid screwing up other sessions in 
    # other threads
    params = real_session.__dict__['_params']

    # Now set the id param used to make a session to our session maker, 
    # if id is None, a new id will be made automatically
    params['id'] = find_id_func()
    real_session.__dict__['_sess'] = BeakerSession({}, **params)

    # Now we can use the session as usual
    session['fred'] = 42
    session.save()

    # At the end, we need to see if the session was used and handle its id
    if session.is_new:
        # do something with session.id to make sure its around next time
        pass


.. Using middleware (Beaker) with a composite app

(Beaker) ミドルウェアを composite app と共に使用する
====================================================

.. How to allow called WSGI apps to share a common session management
.. utility.

呼び出された WSGI アプリケーションが共通のセッション管理ユーティリティ
を共有するのを許可する方法。


(From a `paste #616 <http://pylonshq.com/pasties/616>`_ baked by Mark Luffel)


.. code-block:: ini 

    # Here's an example of configuring multiple apps to use a common 
    # middleware filter
    # The [app:home] section is a standard pylons app
    # The ``/servicebroker`` and ``/proxy`` apps both want to be able 
    # to use the same session management

    [server:main]
    use = egg:Paste#http
    host = 0.0.0.0
    port = 5000

    [filter-app:main]
    use = egg:Beaker#beaker_session
    next = sessioned
    beaker.session.key = my_project_key
    beaker.session.secret = i_wear_two_layers_of_socks

    [composite:sessioned]
    use = egg:Paste#urlmap
    / = home
    /servicebroker = servicebroker
    /proxy = cross_domain_proxy

    [app:servicebroker]
    use = egg:Appcelerator#service_broker

    [app:cross_domain_proxy]
    use = egg:Appcelerator#cross_domain_proxy

    [app:home]
    use = egg:my_project
    full_stack = true
    cache_dir = %(here)s/data


.. storing SA mapped objects in Beaker sessions

SA マップされたオブジェクトを Beaker セッションに保存する
==========================================================

.. Taken from pylons-discuss Google group discussion:

pylons-discuss Google グループの議論から:


.. code-block:: text 

    > I wouldn't expect a SA object to be serializable.  It just doesn't
    > make sense to me.  I don't even want to think about complications with
    > the database and ACID, nor do I want to consider the scalability
    > concerns (the SA object should be tied to a particular SA session,
    > right?).

    (直訳)
    私は SA オブジェクトがシリアライズ可能とは思っていません。それは単
    に私には理解できません。私はデータベースと ACID の複雑さについて考
    えたくありませんし、スケーラビリティについても関心を持ちたくありま
    せん。 (SA オブジェクトは特定の SA セッションに結びつけられるべきで
    すよね?)


.. SA objects are serializable (as long as you aren't using
.. :func:`assign_mapper`, which can complicate things unless you define a
.. custom :func:`__getstate__` method).

SA オブジェクトはシリアライズ可能です。 (:func:`assign_mapper` を使って
いない場合。それは :func:`__getstate__` を定義しないと物事を複雑にします)


.. The error above is because the entity is not being detached from its
.. original session. If you are going to serialize, you have to manually
.. shuttle the object to and from the appropriate sessions.

上記のエラーは entity が元のセッションから detach されていないことが原
因です。シリアライズする際は、オブジェクトを手動で適切なセッションの間
を往復させなければなりません。


.. Three ways to get an object out of serialization and back into an SA  
.. Session are:

シリアライズしたオブジェクトを SA Session に戻すには、以下の 3 通りの方
法があります:


.. 1. A mapped class that has a :func:`__getstate__` which only copies
..    desired properties and won't copy SA session pointers:

1. :func:`__getstate__` を持っているマップされたクラスは desired プロパ
   ティだけをコピーして、SA セッションポインタをコピーしません。


    .. code-block:: python

         beaker.put(key, obj)
         ...
         obj = beaker.get(key)
         Session.add(obj)


.. 2. A regular old mapped class.  Add an :func:`expunge` step.

2. 通常の古いマップされたクラス。 :func:`expunge` ステップを加えてください。


    .. code-block:: python

         Session.expunge(obj)
         beaker.put(key, obj)
         ...
         obj = beaker.get(key)
         Session.add(obj)


.. 3. Don't worry about :func:`__getstate__` or :func:`expunge` on the
..    original object, use :func:`merge`. This is "cleaner" than the
..    :func:`expunge` method shown above but will usually force a load of
..    the object from the database and therefore is not necessarily as
..    "efficient", also it copies the state of the given object to the
..    target object which may be error-prone.

3. オリジナルのオブジェクトについては :func:`__getstate__` や
   :func:`expunge` について気にする必要はありません。 :func:`merge` を
   使用してください。これは上で示した :func:`expunge` メソッドよりクリー
   ンな方法ですが、通常はデータベースからオブジェクトをロードすることを
   強制するので、必ずしも「効率的」ではないかもしれません。またそれは与
   えられたオブジェクトの状態を対象のオブジェクトにコピーしますが、これ
   は間違いの元かもしれません。


    .. code-block:: python

        beaker.put(key, obj)
        ...
        obj = beaker.get(key)
        obj = Session.merge(obj)
