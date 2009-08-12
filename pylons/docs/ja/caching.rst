.. _caching:

===========
キャッシュ
===========

.. Inevitably, there will be occasions during applications development or
.. deployment when some task is revealed to be taking a significant
.. amount of time to complete. When this occurs, the best way to speed
.. things up is with :term:`caching`.

必然的に (Inevitably)、アプリケーション開発やデプロイの際に何らかのタス
クが完了するのに非常に時間がかかることがあります。このような場合、処理
を速くする最も良い方法が :term:`caching` です。


.. Pylons comes with caching middleware enabled that is part of the same
.. package that provides the session handling, `Beaker
.. <http://beaker.groovie.org>`_. Beaker supports a variety of caching
.. backends: memory-based, filesystem-based and the specialised
.. `memcached` library.

Pylons にはキャッシュミドルウェアが有効な状態で付属しています。それはセッ
ションの取り扱いを提供するのと同じパッケージである `Beaker
<http://beaker.groovie.org>`_. の一部です。 Beaker はいくつかの異なる種
類のキャッシュバックエンドをサポートします: メモリベース, ファイルシス
テム, そして特別な `memcached` です。


.. There are several ways to cache data under Pylons, depending on where
.. the slowdown is occurring:

Pylons では、速度低下が起こる場所に応じて、データをキャッシュするいくつ
かの方法があります:


.. * Browser-side Caching - HTTP/1.1 supports the :term:`ETag` caching
..   system that allows the browser to use its own cache instead of
..   requiring regeneration of the entire page. ETag-based caching avoids
..   repeated generation of content but if the browser has never seen the
..   page before, the page will still be generated. Therefore using ETag
..   caching in conjunction with one of the other types of caching listed
..   here will achieve optimal throughput and avoid unnecessary calls on
..   resource-intensive operations.

* ブラウザサイドのキャッシング - HTTP/1.1 は丸ごと 1 ページの再生成を必
  要とする代わりにブラウザが自身のキャッシュを使用できるようにする
  :term:`ETag` キャッシングシステムをサポートしています。 ETag ベースの
  キャッシュは、コンテンツを繰り返し生成することを避けますが、それでも
  ブラウザがそれまでに一度もページを参照したことがないと、ページが生成
  されます。したがって、 ETag キャッシュをここに記述された他のキャッシュ
  タイプのひとつと組み合わせて使用することで、最適のスループットを達成
  して、資源集約的な操作での不必要な呼び出しを避けることができるでしょう。


.. note::

    .. the latter only helps if the entire page can be cached.

    後者はまるまる 1 ページをキャッシュできる場合にだけ有効です。
    (訳注: 後者が何を指しているのか不明)


.. * Controllers - The `cache` object is available in controllers and
..   templates for use in caching anything in Python that can be pickled.

 * コントローラ - `cache` オブジェクトは、 Python で pickle 可能なあら
   ゆるものをキャッシュするのに使用するために、コントローラとテンプレー
   トで利用可能です。


.. * Templates - The results of an entire rendered template can be cached
..   using the `3 cache keyword arguments to the render calls
..   <http://pylonshq.com/docs/class-pylons.templating.Buffet.html#render>`_.
..   These render commands can also be used inside templates.

* テンプレート - レンダリングされたテンプレートの結果全体は `render 呼
  び出しに対する 3 種類のキャッシュキーワード引数
  <http://pylonshq.com/docs/class-pylons.templating.Buffet.html#render>`_
  を使ってキャッシュすることができます。これらの render コマンドは、テ
  ンプレートの中で使用できます。


.. * Mako/Myghty Templates - Built-in caching options are available for
..   both `Mako <http://www.makotemplates.org/docs/caching.html>`_ and
..   `Myghty <http://www.myghty.org/docs/cache.myt>`_ template
..   engines. They allow fine-grained caching of only certain sections of
..   the template as well as caching of the entire template.

* Mako/Myghty テンプレート - `Mako
  <http://www.makotemplates.org/docs/caching.html>`_ と `Myghty
  <http://www.myghty.org/docs/cache.myt>`_ テンプレートエンジンの両方で
  内蔵のキャッシュオプションが利用可能です。それらはテンプレート全体の
  キャッシュだけでなく、テンプレートのある一定のセクションだけの粒度の
  細かいキャッシュを許します。


.. The two primary concepts to bear in mind when caching are i) caches
.. have a *namespace* and ii) caches can have *keys* under that
.. namespace. The reason for this is that, for a single template, there
.. might be multiple versions of the template each requiring its own
.. cached version. The keys in the namespace are the ``version`` and the
.. name of the template is the ``namespace``. **Both of these values must
.. be Python strings.**

キャッシュを行うときに覚えておくべき 2 つの基本概念は i) キャッシュには
*名前空間* があり、 ii) 名前空間の下でキャッシュは *キー* を持つことが
できるということです。この理由は、単一のテンプレートに対して複数のテン
プレートのバージョンがそれぞれ自身のキャッシュされたバージョンを必要と
するかもしれないからです。名前空間におけるキーは ``バージョン`` です。
そしてテンプレートの名前は ``名前空間`` です。 **これらの値の両方とも、
Python 文字列でなければなりません。**


.. In templates, the cache ``namespace`` will automatically be set to the
.. name of the template being rendered. Nothing else is required for
.. basic caching, unless the developer wishes to control for how long the
.. template is cached and/or maintain caches of multiple versions of the
.. template.

テンプレート中では、キャッシュの「名前空間」はレンダリングされるテンプ
レートの名前に自動的に設定されるでしょう。基本的なキャッシュに対して他
には何も必要ありません。例外は、テンプレートがどれくらい長い間キャッシュ
されるかを開発者が制御したい場合、かつ/または、テンプレートの複数のバー
ジョンのキャッシュを維持したい場合です。


.. see also Stephen Pierzchala's `Caching for Performance
.. <http://web.archive.org/web/20060424171425/http://www.webperformance.org/caching/caching_for_performance.pdf>`_
.. (stephen@pierzchala.com)

Stephen Pierzchala の `Caching for Performance
<http://web.archive.org/web/20060424171425/http://www.webperformance.org/caching/caching_for_performance.pdf>`_
(stephen@pierzchala.com) も読んでください。


.. Using the Cache object

cache オブジェクトを使う
------------------------

.. Inside a controller, the `cache` object will be available for use. If
.. an action or block of code makes heavy use of resources or take a long
.. time to complete, it can be convenient to cache the result. The
.. `cache` object can cache any Python structure that can be `pickled
.. <http://docs.python.org/lib/module-pickle.html>`_.

コントローラの中では、 `cache` オブジェクトが利用可能です。リソースや時
間を集中的に使用するアクションまたはブロックがコード中にあれば、結果を
キャッシュすることは有効な場合があります。 `cache` オブジェクトは
`pickle <http://www.python.jp/doc/release/lib/module-pickle.html>`_ 可
能などんな Python 構造もキャッシュすることができます。


.. Consider an action where it is desirable to cache some code that does
.. a time-consuming or resource-intensive lookup and returns an object
.. that can be pickled (list, dict, tuple, etc.):

あるアクションについて、時間を費やしたりリソースの集中的な参照をしたり
して pickle できるオブジェクト (リスト, 辞書, タプルなど) を返す何らか
のコードをキャッシュしたいとします:


.. code-block:: python
    
    # Add to existing imports
    from pylons import cache
    
    
    # Under the controller class
    def some_action(self, day):
        # hypothetical action that uses a 'day' variable as its key

        def expensive_function():
            # do something that takes a lot of cpu/resources
            return expensive_call()

        # Get a cache for a specific namespace, you can name it whatever
        # you want, in this case its 'my_function'
        mycache = cache.get_cache('my_function', type="memory")

        # Get the value, this will create the cache copy the first time
        # and any time it expires (in seconds, so 3600 = one hour)
        c.myvalue = mycache.get_value(key=day, createfunc=expensive_function,
                                      expiretime=3600)

        return render('/some/template.myt')


.. The `createfunc` option requires a callable object or a function which
.. is then called by the cache whenever a value for the provided key is
.. not in the cache, or has expired in the cache.

`createfunc` オプションには callable オブジェクトまたは関数を渡します。
引数に対する値がキャッシュ中に存在しないか有効期限を過ぎていた場合は、
常にキャッシュによってそれが呼び出されます。


.. Because the `createfunc` is called with no arguments, the resource- or
.. time-expensive function must correspondingly also not require any
.. arguments.

`createfunc` は引数なしで呼ばれるので、リソースまたは時間を大量消費する
関数もそれに対応して引数をとることはできません。


.. Other Cache Options

その他のキャッシュオプション
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. The cache also supports the removal values from the cache, using the
.. key(s) to identify the value(s) to be removed and it also supports
.. clearing the cache completely, should it need to be reset.

キャッシュはキーを指定してキャッシュされた値を削除することをサポートし
ます。また、リセットする際に必要となる、キャッシュの完全なクリアもサポー
トします。


.. code-block:: python

    # Clear the cache
    mycache.clear()

    # Remove a specific key
    mycache.remove_value('some_key')


.. Using Cache keywords to `render`

`render` に対するキャッシュキーワードを使う
-------------------------------------------

.. warning::

    Needs to be extended to cover the specific render_* calls
    introduced in Pylons 0.9.7


.. All :func:`render <pylons.templating.render_mako>` commands have
.. caching functionality built in. To use it, merely add the appropriate
.. cache keyword to the render call.

すべての :func:`render <pylons.templating.render_mako>` コマンドは、
キャッシュ機能を内蔵しています。それを使用するには、単に render 呼び出
しに適切なキャッシュキーワードを加えてください。


.. code-block:: python

    class SampleController(BaseController):

        def index(self):
            # Cache the template for 10 mins
            return render('/index.myt', cache_expire=600)

        def show(self, id):
            # Cache this version of the template for 3 mins
            return render('/show.myt', cache_key=id, cache_expire=180)

        def feed(self):
            # Cache for 20 mins to memory
            return render('/feed.myt', cache_type='memory', cache_expire=1200)

        def home(self, user):
            # Cache this version of a page forever (until the cache dir
            # is cleaned)
            return render('/home.myt', cache_key=user, cache_expire='never')


.. Using the Cache Decorator

キャッシュデコレータを使う
--------------------------

.. Pylons also provides the :func:`~pylons.decorators.cache.beaker_cache`
.. decorator for caching in `pylons.cache` the results of a completed
.. function call (memoizing).

Pylons はまた、関数呼び出し全体の結果をキャッシュする (memoizing) ため
に、 `pylons.cache` で :func:`~pylons.decorators.cache.beaker_cache` デ
コレータを提供します。


.. The cache decorator takes the same cache arguments (minus their
.. `cache_` prefix), as the `render` function does.

beaker_cache デコレータは、 `render` 関数と同じ (それらから `cache_` プ
リフィックスを除いた) キャッシュ引数を取ります。


.. code-block:: python

    from pylons.decorators.cache import beaker_cache

    class SampleController(BaseController):

        # Cache this controller action forever (until the cache dir is
        # cleaned)
        @beaker_cache()
        def home(self):
            c.data = expensive_call()
            return render('/home.myt')

        # Cache this controller action by its GET args for 10 mins to memory
        @beaker_cache(expire=600, type='memory', query_args=True)
        def show(self, id):
            c.data = expensive_call(id)
            return render('/show.myt')


.. By default the decorator uses a composite of all of the decorated
.. function's arguments as the cache key. It can alternatively use a
.. composite of the `request.GET` query args as the cache key when the
.. `query_args` option is enabled.

デフォルトでは、 beaker_cache デコレータはキャッシュキーとしてデコレー
ト対象の関数のすべての引数を合成したものを使用します。 `query_args` オ
プションが有効なときは、代わりにキャッシュキーとして `request.GET` クエ
リ引数を合成したものを使用することができます。


.. The cache key can be further customized via the `key` argument.

`key` 引数でさらにキャッシュキーをカスタマイズすることができます。


Caching Arbitrary Functions
---------------------------

.. Arbitrary functions can use the
.. :func:`~pylons.decorators.cache.beaker_cache` decorator, but should
.. include an additional option. Since the decorator caches the
.. :term:`response` object, it's unlikely the status code and headers for
.. non-controller methods should be cached. To avoid caching that data,
.. the cache_response keyword argument should be set to false.

任意の関数で :func:`~pylons.decorators.cache.beaker_cache` デコレータを
使用できますが、追加のオプションを渡す必要があります。デコレーターは
:term:`response` オブジェクトをキャッシュするため、非コントローラメソッ
ドでステータスコードやヘッダーをキャッシュしなければならないことはほと
んどありません。そのようなデータをキャッシュするのを避けるために、
cache_response キーワード引数は false に設定されるべきです。


.. code-block:: python
    
    from pylons.decorators.cache import beaker_cache
    
    @beaker_cache(expire=600, cache_response=False)
    def generate_data():
        # do expensive data generation
        return data

.. warning::
    
    When caching arbitrary functions, the ``query_args`` argument should not
    be used since the result of arbitrary functions shouldn't depend on
    the request parameters.

 
.. ETag Caching

ETag キャッシュ
----------------

.. Caching via ETag involves sending the browser an ETag header so that
.. it knows to save and possibly use a cached copy of the page from its
.. own cache, instead of requesting the application to send a fresh copy.

ETag によるキャッシュは、 ETag ヘッダーをブラウザに送ることでブラウザが
ページのキャッシュされたコピーを保存し、(アプリケーションがそれを送る代
わりに) ブラウザ自身のキャッシュが使用できると知らせることを含みます。


.. Because the ETag cache relies on sending headers to the browser, it
.. works in a slightly different manner to the other caching mechanisms
.. described above.

ETag キャッシュはブラウザにヘッダーを送ることに頼っているので、上述した
他のキャッシュ機構とはやや異なる方法で働きます。


.. The :func:`~pylons.controllers.util.etag_cache` function will set the
.. proper HTTP headers if the browser doesn't yet have a copy of the
.. page. Otherwise, a 304 HTTP Exception will be thrown that is then
.. caught by Paste middleware and turned into a proper 304 response to
.. the browser. This will cause the browser to use its own locally-cached
.. copy.

ブラウザにページのコピーがまだなければ、
:func:`~pylons.controllers.util.etag_cache` 関数は適切な HTTP ヘッダが
セットされた Response オブジェクトを返します。そうでなければ 304 HTTP
Exception が投げられ、これは Paste ミドルウェアによって捕捉されてブラウ
ザへの適切な 304 レスポンスになります。これにより、ブラウザはそれ自身の
持つコピーを使用するようになります。


.. :func:`~pylons.controllers.util.etag_cache` returns
.. :class:`~pylons.controllers.util.Response` for legacy purposes
.. (:class:`~pylons.controllers.util.Response` should be used directly
.. instead).

:func:`~pylons.controllers.util.etag_cache` は レガシー目的のために
:class:`~pylons.controllers.util.Response` を返します (代わりに
:class:`~pylons.controllers.util.Response` を直接使用すべきです)。


.. ETag-based caching requires a single key which is sent in the ETag
.. HTTP header back to the browser. The `RFC specification for HTTP
.. headers <http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html>`_
.. indicates that an ETag header merely needs to be a string. This value
.. of this string does not need to be unique for every URL as the browser
.. itself determines whether to use its own copy, this decision is based
.. on the URL and the ETag key.

ETag ベースのキャッシュは ETag HTTP ヘッダでブラウザに送られる単一のキー
を必要とします。 `HTTP ヘッダの RFC 仕様
<http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html>`_ では、 ETag
ヘッダーは文字列であることだけが要求されています。ブラウザ自身がキャッ
シュを使用するかどうかを決定するため、この値はあらゆる URL でユニークで
ある必要はありません。その決定は URL と ETag キーに基づいて行われます。


.. code-block:: python

    def my_action(self):
        etag_cache('somekey')
        return render('/show.myt', cache_expire=3600)


.. Or to change other aspects of the response:

または、response の他の側面を変える場合:


.. code-block:: python

    def my_action(self):
        etag_cache('somekey')
        response.headers['content-type'] = 'text/plain'
        return render('/show.myt', cache_expire=3600)


.. note::

    .. In this example that we are using template caching in addition to
    .. ETag caching. If a new visitor comes to the site, we avoid
    .. re-rendering the template if a cached copy exists and repeat hits
    .. to the page by that user will then trigger the ETag cache. This
    .. example also will never change the ETag key, so the browsers cache
    .. will always be used if it has one.

    この例では ETag キャッシュに加えてテンプレートキャッシュも使用して
    います。新しい訪問者がサイトを訪れた場合、キャッシュされたコピーが
    存在しているならテンプレートを再レンダリングすることを避けます。そ
    して、そのユーザが再びそのページに訪れたなら ETag キャッシュの引き
    金となるでしょう。さらにこの例では ETag キーは決して変わらないので、
    ブラウザがキャッシュを持っているなら常に使用されるでしょう。


.. The frequency with which an ETag cache key is changed will depend on
.. the web application and the developer's assessment of how often the
.. browser should be prompted to fetch a fresh copy of the page.

ETag キャッシュキーを変更する頻度は、 Web アプリケーションによって、そ
してブラウザに対してどのぐらい頻繁にページの新しいコピーを取得させたい
かに関する開発者の判断によって決まるでしょう。


.. warning::

    Stolen from Philip Cooper's `OpenVest wiki
    <http://www.openvest.com/trac/wiki/BeakerCache>`_ after which it
    was updated and edited ...


.. Inside the Beaker Cache

Beaker Cache の内部
-----------------------

Caching
^^^^^^^

.. First let's start out with some **slow** function that we would
.. like to cache.  This function is not slow but it will show us when
.. it was cached so we can see things are working as we expect:

最初に、キャッシュしたいと思う何らかの **遅い** 関数と共に始めましょう。
この関数は遅くありませんが、それがいつキャッシュされたかが分かるので、
期待通りにいろいろなことが働いているのを見ることができるでしょう:


.. code-block:: python

    import time
    def slooow(myarg):
      # some slow database or template stuff here
      return "%s at %s" % (myarg,time.asctime())


.. When we have the cached function, multiple calls will tell us whether
.. are seeing a cached or a new version.

キャッシュされた関数があるとき、複数の呼び出しを行うことでキャッシュさ
れたバージョンか新しいバージョンのどちらを見ているかが分かります。


.. DBMCache

DBM キャッシュ
^^^^^^^^^^^^^^

.. The DBMCache stores (actually pickles) the response in a dbm style database.

DBM キャッシュはレスポンスを dbm スタイルのデータベースに保存します (実
際には pickle します)。


.. What may not be obvious is that there are two levels of keys.  They
.. are essentially created as one for the function or template name
.. (called the namespace) and one for the ''keys'' within that (called
.. the key).  So for `Some_Function_name`, there is a cache created as
.. one dbm file/database.  As that function is called with different
.. arguments, those arguments are keys within the dbm file. First let's
.. create and populate a cache.  This cache might be a cache for the
.. function `Some_Function_name` called three times with three different
.. arguments: `x`, `yy`, and `zzz`:

必ずしも明白でないことは、キーに 2 つのレベルがあるということです。それ
らは原則として、一つは関数またはテンプレート名のために (名前空間と呼ば
れます)、一つは名前空間の中での「キー」のために (キーと呼ばれます) 作成
されます。そのため `Some_Function_name` に対しては 1つの dbm ファイル/
データベースとして作成されたキャッシュが存在します。その関数が異なった
引数で呼ばれるなら、それらの引数は dbm ファイルの中のキーになります。
最初にキャッシュを作成してデータを投入してみます。このキャッシュは 3 つ
の異なる引数 `x`, `yy`, `zzz` によって3 回呼び出された
`Some_Function_name` 関数のためのキャッシュとみなすことができます:


.. code-block:: python

    from beaker.cache import CacheManager
    cm = CacheManager(type='dbm', data_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)


.. Nothing much new yet.  After getting the cache we can use the cache as
.. per the Beaker Documentation.

まだそんなに新しいことはありません。キャッシュを作成した後は、 Beaker
ドキュメントに従ってキャッシュを使用できます。


.. code-block:: python

    import beaker.container as container
    cc = container.ContainerContext()
    nsm = cc.get_namespace_manager('Some_Function_name',
                                   container.DBMContainer,data_dir='beaker.cache')
    filename = nsm.file


.. Now we have the file name.  The file name is a `sha` hash of a string
.. which is a join of the container class name and the function name
.. (used in the `get_cache` function call).  It would return something
.. like:

ファイル名を取得しました。ファイル名は(`get_cache` 関数呼び出しで使われ
た) コンテナクラス名と関数名を繋げた文字列の `sha` ハッシュです。その戻
り値は以下のようになるでしょう。


.. code-block:: python

    'beaker.cache/container_dbm/a/a7/a768f120e39d0248d3d2f23d15ee0a20be5226de.dbm'


.. With that file name you could look directly inside the cache database
.. (but only for your education and debugging experience, **not** your
.. cache interactions!)

そのファイル名を使って、キャッシュデータベースの中身を直接見ることがで
きます (ただし教育目的とデバッグ経験のために限ります。 **not** your
cache interactions!)


.. code-block:: python

    ## this file name can be used directly (for debug ONLY)
    import anydbm
    import pickle
    db = anydbm.open(filename)
    old_t, old_v = pickle.loads(db['zzz'])


.. The database only contains the old time and old value.  Where did the
.. expire time and the function to create/update the value go?.  They
.. never make it to the database.  They reside in the `cache` object
.. returned from `get_cache` call above.

データベースは単に古い時刻と値を含むだけです。有効期限や、値を作成したり
アップデートしたりする機能はどこにあるのでしょうか?  それらはデータベー
スまで到達することはありません。それらは上の `get_cache` 呼び出しから返
された `cache` オブジェクトに備わっています。


.. Note that the createfunc, and expiretime values are stored during the
.. first call to `get_value`. Subsequent calls with (say) a different
.. expiry time will **not** update that value.  This is a tricky part of
.. the caching but perhaps is a good thing since different processes may
.. have different policies in effect.

createfunc と expiretime の値が `get_value` の最初の呼び出しの時に保存
されることに注意してください。その後の呼び出しで (例えば) 異なる有効期
限を渡しても、その値は更新 **されません** 。これは、キャッシュの
tricky な部分ですが、異なるプロセスは事実上異なるポリシーを持つことにな
るので、おそらく良いことです。


.. If there are difficulties with these values, remember that one call to
.. :func:`cache.clear` resets everything.

これらの値に関して困難があれば、 :func:`cache.clear` を呼び出せばすべて
がリセットされることを覚えておいてください。


.. Database Cache

Database キャッシュ
^^^^^^^^^^^^^^^^^^^

.. Using the `ext:database` cache type.

`ext:database` キャッシュタイプの使い方。


.. code-block:: python

    from beaker.cache import CacheManager
    #cm = CacheManager(type='dbm', data_dir='beaker.cache')
    cm = CacheManager(type='ext:database',
                      url="sqlite:///beaker.cache/beaker.sqlite",
                      data_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)


.. This is identical to the cache usage above with the only difference
.. being the creation of the `CacheManager`.  It is much easier to view
.. the caches outside the beaker code (again for edification and
.. debugging, not for api usage).

これは `CacheManager` の作成における唯一の違いを除き、上述のキャッシュ
の使用法と同じです。 beaker コードの外でキャッシュを見るのは非常に簡単
です (繰り返しますが、これは啓発とデバッグのためであり、api の使用法で
はありません)。


.. SQLite was used in this instance and the SQLite data file can be
.. directly accessed using the SQLite command-line utility or the Firefox
.. plug-in:

この場合は SQLite を使用しました。 SQLite データファイルは SQLite コマ
ンドラインユーティリティか Firefox プラグインを使用することで直接アクセ
スできます:


.. code-block:: text

    sqlite3 beaker.cache/beaker.sqlite
    # from inside sqlite:
    sqlite> .schema
    CREATE TABLE beaker_cache (
            id INTEGER NOT NULL,
            namespace VARCHAR(255) NOT NULL,
            key VARCHAR(255) NOT NULL,
            value BLOB NOT NULL,
            PRIMARY KEY (id),
             UNIQUE (namespace, key)
    );
    select * from beaker_cache;


.. warning::

    .. The data structure is different in Beaker 0.8 ...

    データ構造は Beaker 0.8 では異なっています ...


.. code-block:: python

    cache = sa.Table(table_name, meta,
                     sa.Column('id', types.Integer, primary_key=True),
                     sa.Column('namespace', types.String(255), nullable=False),
                     sa.Column('accessed', types.DateTime, nullable=False),
                     sa.Column('created', types.DateTime, nullable=False),
                     sa.Column('data', types.BLOB(), nullable=False),
                     sa.UniqueConstraint('namespace')
    )


.. It includes the access time but stores rows on a one-row-per-namespace
.. basis, (storing a pickled dict) rather than
.. one-row-per-namespace/key-combination. This is a more efficient
.. approach when the problem is handling a large number of namespaces
.. with limited keys --- like sessions.

これは、アクセスタイムを含んでいますが、名前空間/キーの組み合わせ 1 つ
に対して 1 列ではなく、名前空間 1 つに対して 1 列ベースで列を格納します
(pickle された辞書を格納します)。これは、問題が限られたキーと多くの名前
空間を扱っているとき、より効率的なアプローチです --- セッションのように。


.. Memcached Cache

memcached キャッシュ
^^^^^^^^^^^^^^^^^^^^

.. For large numbers of keys with expensive pre-key lookups memcached is
.. the way to go.

キーの数が多く、事前にキーをルックアップするのにコストがかかる
(expensive pre-key lookups) 場合、 memcached は良い方法です。


.. If memcached is running on the the default port of 11211:

memcached がデフォルトの 11211 ポートで動いているなら:


.. code-block:: python

    from beaker.cache import CacheManager
    cm = CacheManager(type='ext:memcached', url='127.0.0.1:11211',
                      lock_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)
