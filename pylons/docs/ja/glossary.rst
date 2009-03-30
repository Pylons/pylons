.. _glossary:

用語集
========

.. glossary::

    .. action
    ..     The class method in a Pylons applications' controller that
    ..     handles a request.

    action
        (**アクション**)

        リクエストを扱う Pylons アプリケーションのコントローラのクラス
        メソッド。


    .. API
    ..     Application Programming Interface. The means of
    ..     communication between a programmer and a software program
    ..     or operating system.

    API
       アプリケーション・プログラミング・インターフェース。 プログラマ
       とソフトウェアプログラムまたはオペレーティングシステムとの間のコ
       ミュニケーション手段。


    .. app_globals
    ..     The ``app_globals`` object is created on application
    ..     instantiation by the :class:`Globals` class in a projects
    ..     :file:`lib/app_globals.py` module.
    ..
    ..     This object is created once when the application is loaded
    ..     by the projects :file:`config/environment.py` module (See
    ..     :ref:`environment-config`). It remains persistent during
    ..     the lifecycle of the web application, and is *not*
    ..     thread-safe which means that it is best used for global
    ..     options that should be *read-only*, or as an object to
    ..     attach db connections or other objects which ensure their
    ..     own access is thread-safe.

    app_globals
        ``app_globals`` オブジェクトは、 :file:`lib/app_globals.py` モ
        ジュールの :class:`Globals` クラスからアプリケーションインスタ
        ンス化によって作られます。

        このオブジェクトは、プロジェクトの
        :file:`config/environment.py` モジュール
        (:ref:`environment-config` 参照) でアプリケーションがロードされ
        るときに一度だけ作成されます。それは Web アプリケーションのライ
        フサイクルの間を通して永続化され、スレッド・セーフでは *ありま
        せん* 。つまり、その使い方として最も良いのは、 *読み取り専用*
        なグローバルオプションのため、またはデータベース接続やそれ自身
        のアクセスがスレッド・セーフであることを保証する他のオブジェク
        トを取り付けるオブジェクトとして使用することです。


    .. c
    ..     Commonly used alias for :term:`tmpl_context` to save on the
    ..     typing when using lots of controller populated variables in
    ..     templates.

    c
        :term:`tmpl_context` の別名。テンプレート内でコントローラから渡
        される多数の変数を使用するときにタイプ量を減らすために一般的に
        使用されます。


    .. caching
    ..     The storage of the results of expensive or length
    ..     computations for later re-use at a point more quickly
    ..     accessed by the end user.

    caching
        (**キャッシュ**)

        計算量が多いか長時間かかる計算の結果を保存して、その後エンド
        ユーザによって短時間でアクセスされた場合に計算結果を再利用す
        るために使用されるストレージ。


    .. CDN
    ..     Content Delivery Networks (CDN's) are generally globally
    ..     distributed content delivery networks optimized for low
    ..     latency for static file distribution. They can
    ..     significantly increase page-load times by ensuring that the
    ..     static resources on a page are delivered by servers
    ..     geographically close to the client in addition to
    ..     lightening the load placed on the application server.

    CDN
        コンテンツ配信ネットワーク (CDN) は、静的ファイルを小さなレイテ
        ンシー (遅延) で配布するために最適化された、一般にグローバルに
        分散されたコンテンツ配信のためのネットワークです。 CDN は、アプ
        リケーション・サーバーにかかる負荷を軽減することに加えて、ペー
        ジ上の静的なリソースを地理的にクライアントの近くのサーバから提
        供することによって、ページロード回数を大幅に増やすことができま
        す。


    .. ColdFusion Components
    ..     CFCs represent an attempt by Macromedia to bring ColdFusion
    ..     closer to an Object Oriented Programming (OOP)
    ..     language. ColdFusion is in no way an OOP language, but
    ..     thanks in part to CFCs, it does boast some of the
    ..     attributes that make OOP languages so popular.

    ColdFusion Components
        CFC は、 ColdFusion をオブジェクト指向プログラミング (OOP) 言語
        により近づけようとする Macromedia による試みを表します。
        ColdFusion はまったく OOP 言語ではありませんが、多少は CFC のお
        かげで、 OOP 言語をとてもポピュラーにしている属性のいくつかを持っ
        ています。


    .. controller
    ..     The 'C' in MVC. The controller is given a request, does the
    ..     necessary logic to prepare data for display, then renders a
    ..     template with the data and returns it to the user. See
    ..     :ref:`controllers`.

    controller
        (**コントローラ**)

        MVC の 'C' です。コントローラは、リクエストを与えられて、表示に
        必要なデータを準備するために必要なロジックを行い、そしてそのデー
        タを使ってテンプレートをレンダリングして、結果をユーザに返します。
        :ref:`controllers` を参照してください。


    .. easy_install
    ..     A tool that lets you download, build, install and manage
    ..     Python packages and their dependencies. `easy_install`_ is
    ..     the end-user facing component of :term:`setuptools`.
    ..
    ..     Pylons can be installed with ``easy_install``, and
    ..     applications built with Pylons can easily be deployed this
    ..     way as well.
    ..
    ..     .. seealso::
    ..         Pylons :ref:`deployment`
    ..
    ..     .. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall

    easy_install
        Python パッケージとその依存パッケージのダウンロード、ビルド、イ
        ンストール、管理を行うことのできるツール。 `easy_install`_ は
        :term:`setuptools` のエンドユーザ向けコンポーネントです。

        Pylons は ``easy_install`` を使ってインストールすることができま
        す。そして、 Pylons を用いて組み立てられたアプリケーションも、
        同様に easy_install によって容易に配布することができます。

        .. seealso::
            Pylons :ref:`deployment`

        .. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall


    .. egg
    ..     Python egg's are bundled Python packages, generally
    ..     installed by a package called :term:`setuptools`. Unlike
    ..     normal Python package installs, egg's allow a few
    ..     additional features, such as package dependencies, and
    ..     dynamic discovery.
    ..
    ..     .. seealso::
    ..         `The Quick Guide to Python Eggs
    ..         <http://peak.telecommunity.com/DevCenter/PythonEggs>`_

    egg
        Python egg は、ひとまとめにされた Python パッケージで、一般に
        :term:`setuptools` と呼ばれるパッケージによってインストールされ
        ます。通常の Python パッケージのインストールとは異なり、 egg に
        よるインストールでは、パッケージの依存性や動的な検索など、いく
        つかの付加的な機能が提供されます。

        .. seealso::
            `The Quick Guide to Python Eggs
            <http://peak.telecommunity.com/DevCenter/PythonEggs>`_


    .. EJBs
    ..     Enterprise JavaBeans (EJB) technology is the server-side
    ..     component architecture for Java Platform, Enterprise
    ..     Edition (Java EE). EJB technology enables rapid and
    ..     simplified development of distributed, transactional,
    ..     secure and portable applications based on Java technology.

    EJBs
        Enterprise JavaBeans (EJB) テクノロジーは、 Java Platform
        Enterprise Edition (Java EE) のためのサーバサイドコンポーネント
        アーキテクチャです。 EJB テクノロジーは Java テクノロジーに基づ
        く分散トランザクション型でセキュアかつポータブルなアプリケーショ
        ンの迅速で簡易的な開発を可能にします。


    .. environ
    ..     environ is a dictionary passed into all :term:`WSGI`
    ..     application. It generally contains unparsed header
    ..     information, CGI style variables and other objects inserted
    ..     by :term:`WSGI Middleware`.

    environ
        environ はすべての :term:`WSGI` アプリケーションに渡される辞書
        です。一般に、解析前のヘッダー情報と、 CGI スタイルの変数、およ
        び :term:`WSGI Middleware` によって挿入されたその他のオブジェク
        トが含まれます。


    .. ETag
    ..     An ETag (entity tag) is an HTTP response header returned by
    ..     an HTTP/1.1 compliant web server used to determine change
    ..     in content at a given URL. See
    ..     http://wikipedia.org/wiki/HTTP_ETag

    ETag
        ETag (エンティティタグ) は HTTP/1.1 互換の Web サーバーによって
        返される HTTP レスポンスヘッダで、ある URL の内容に変化があった
        かどうかを決定するために使用されます。
        http://wikipedia.org/wiki/HTTP_ETag を見てください。


    .. g
    ..     Alias used in prior versions of Pylons for
    ..     :term:`app_globals`.

    g
        Pylons の以前のバージョンで使用されていた :term:`app_globals`
        の別名。


    .. Google App Engine
    ..     A cloud computing platform for hosting web applications
    ..     implemented in Python. Building Pylons applications for App
    ..     Engine is facilitated by Ian Bicking's `appengine-monkey
    ..     project <http://code.google.com/p/appengine-monkey/>`_.
    ..
    ..     .. seealso::
    ..         `What is Google App Engine? - Official Doc
    ..         <http://code.google.com/appengine/docs/whatisgoogleappengine.html>`_

    Google App Engine
        Python で実装された Web アプリケーションをホスティングするため
        のクラウドコンピューティング・プラットホーム。 Ian Bicking の
        `appengine-monkey プロジェクト
        <http://code.google.com/p/appengine-monkey/>`_ によって、
        Pylons アプリケーションを App Engine で動かすことが容易になりま
        す。

        .. seealso::
            `Google App Engine について
            <http://code.google.com/intl/ja/appengine/docs/whatisgoogleappengine.html>`_


    .. h
    ..     The helpers reference, ``h``, is made available for use
    ..     inside templates to assist with common rendering
    ..     tasks. ``h`` is just a reference to the
    ..     :file:`lib/helpers.py` module and can be used in the same
    ..     manner as any other module import.

    h
        ヘルパー参照 ``h`` は、一般的なレンダリングタスクの手助けのため
        にテンプレートの中で使用されます。 ``h`` は単に
        :file:`lib/helpers.py` モジュールへの参照であり、他のモジュール
        インポートとまったく同じように使用できます。


    .. Model-View-Controller
    ..     An architectural pattern used in software engineering. In
    ..     Pylons, the MVC paradigm is extended slightly with a
    ..     pipeline that may transform and extend the data available
    ..     to a controller, as well as the Pylons :term:`WSGI` app
    ..     itself that determines the appropriate Controller to call.
    ..
    ..     .. seealso::
    ..         `MVC at Wikipedia
    ..         <http://wikipedia.org/wiki/Model-View-Controller>`_

    Model-View-Controller
        (**モデル-ビュー-コントローラ**)

        ソフトウェア工学で使用されるアーキテクチャパターン。 Pylons で
        は MVC パラダイムはわずかに拡張されていて、それはコントローラで
        利用可能なデータの変形と拡張を行うパイプラインを持つと同時に、
        Pylons :term:`WSGI` アプリ自身が呼び出すべき適切なコントローラ
        を決定します。

        .. seealso::
            `Model View Controller - Wikipedia
            <http://ja.wikipedia.org/wiki/Model_View_Controller>`_


    .. MVC
    ..     See :term:`Model-View-Controller`

    MVC
        :term:`Model-View-Controller` を参照。


    .. ORM
    ..     (Object-Relational Mapper) Maps relational databases such
    ..     as MySQL, Postgres, Oracle to objects providing a cleaner
    ..     API.  Most ORM's also make it easier to prevent SQL
    ..     Injection attacks by binding variables, and can handle
    ..     generating sometimes extensive SQL.

    ORM
        オブジェクト・リレーショナル・マッパーは、 MySQL, Postgres,
        Oracle などのリレーショナルデータベースを、よりクリーンな API
        を提供するオブジェクトにマップします。また、ほとんどの ORM では、
        変数のバインディングによって SQL Injection 攻撃を防ぐことが簡単
        になり、ときには非常に長いこともある SQL 文の生成を扱うことがで
        きます。


    .. Pylons
    ..     A Python-based WSGI oriented web framework.

    Pylons
        Python ベースの WSGI 指向 Web フレームワーク。


    .. Rails
    ..     Abbreviated as RoR, Ruby on Rails (also referred to as just
    ..     Rails) is an open source Web application framework, written
    ..     in Ruby

    Rails
        RoR と略されます。 Ruby on Rails (単に Rails と呼ばれることもあ
        る) は、 Ruby によって書かれたオープンソースの Web アプリケーショ
        ン・フレームワークです。


    .. request
    ..     Refers to the current request being processed. Available to
    ..     import from :mod:`pylons` and is available for use in
    ..     templates by the same name. See
    ..     :class:`~pylons.controllers.util.Request`.

    request
        (**リクエスト**)

        現在処理されているリクエストを指します。 :mod:`pylons` からイン
        ポートすることで、またはテンプレートの中では同じ名前によって利
        用可能です。 :class:`~pylons.controllers.util.Request` を参照し
        てください。


    .. response
    ..     Refers to the response to the current request. Available to
    ..     import from :mod:`pylons` and is available for use in
    ..     template by the same name. See
    ..     :class:`~pylons.controllers.util.Response`.

    response
        (**レスポンス**)

        現在のリクエストに対するレスポンスを指します。 :mod:`pylons` か
        らインポートすることで、またはテンプレート中では同じ名前によっ
        て利用可能です。 :class:`~pylons.controllers.util.Response` を
        見てください。


    .. route
    ..     Routes determine how the URL's are mapped to the
    ..     controllers and which URL is generated. See
    ..     :ref:`url-config`

    route
        Routes は、 URL がどのようにコントローラにマップされるか、そし
        てどの URL が生成されるかを決定します。 :ref:`url-config` を参
        照してください。


    .. setuptools
    ..     An extension to the basic distutils, setuptools allows
    ..     packages to specify package dependencies and have dynamic
    ..     discovery of other installed Python packages.
    ..
    ..     .. seealso::
    ..         `Building and Distributing Packages with setuptools
    ..         <http://peak.telecommunity.com/DevCenter/setuptools>`_

    setuptools
        基本的な distutils に対する拡張。 setuptools によって、パッケー
        ジは依存するパッケージを指定したり、インストールされた他の
        Python パッケージを動的に検索することができます。

        .. seealso::
            `Building and Distributing Packages with setuptools
            <http://peak.telecommunity.com/DevCenter/setuptools>`_


    .. SQLAlchemy
    ..     One of the most popular Python database object-relation
    ..     mappers (:term:`ORM`). `SQLAlchemy
    ..     <http://www.sqlalchemy.org/>`_ is the default ORM
    ..     recommended in Pylons. SQLAlchemy at the ORM level can look
    ..     similar to Rails ActiveRecord, but uses the `DataMapper
    ..     <http://www.martinfowler.com/eaaCatalog/dataMapper.html>`_
    ..     pattern for additional flexibility with the ability to map
    ..     simple to extremely complex databases.

    SQLAlchemy
        最もポピュラーな Python データベース・オブジェクト・リレーショ
        ン・マッパー (:term:`ORM`) の 1 つ。 `SQLAlchemy
        <http://www.sqlalchemy.org/>`_ は Pylons が推奨するデフォルトの
        ORM です。 ORM レベルにおける SQLAlchemy は Rails の
        ActiveRecord と同様に見えますが、簡単なデータベースから非常に複
        雑なものまでマップすることのできる追加の柔軟性のために
        `DataMapper
        <http://www.martinfowler.com/eaaCatalog/dataMapper.html>`_ パター
        ンを使用します。


    .. tmpl_context
    ..     The ``tmpl_context`` is available in the :mod:`pylons`
    ..     module, and refers to the template context. Objects
    ..     attached to it are available in the template namespace as
    ..     either ``tmpl_context`` or ``c`` for convenience.

    tmpl_context
        ``tmpl_context`` は :mod:`pylons` モジュールから利用可能で、テ
        ンプレートコンテキストを参照します。 テンプレートコンテキストに
        取り付けられたオブジェクトは、テンプレート名前空間では
        ``tmpl_context`` として、または利便性のために ``c`` という名前
        で利用可能です。


    .. UI
    ..     User interface. The means of communication between a person
    ..     and a software program or operating system.

    UI
        ユーザーインタフェース。 人とソフトウェアプログラム、またはオペ
        レーティングシステムとの間のコミュニケーション手段。


    .. virtualenv
    ..     A tool to create isolated Python environments, designed to
    ..     supersede the ``workingenv`` package and `virtual python`_
    ..     configurations. In addition to isolating packages from
    ..     possible system conflicts, `virtualenv`_ makes it easy to
    ..     install Python libraries using :term:`easy_install` without
    ..     dumping lots of packages into the system-wide Python.
    ..
    ..     The other great benefit is that no root access is required
    ..     since all modules are kept under the desired
    ..     directory. This makes it easy to setup a working Pylons
    ..     install on shared hosting providers and other systems where
    ..     system-wide access is unavailable.
    ..
    ..     ``virtualenv`` is employed automatically by the
    ..     ``go-pylons.py`` script described in
    ..     :ref:`getting_started`. The Pylons wiki has more
    ..     information on `working with virtualenv`_.
    ..
    ..     .. _virtual python: http://peak.telecommunity.com/DevCenter/EasyInstall#creating-a-virtual-python
    ..     .. _virtualenv: http://pypi.python.org/pypi/virtualenv
    ..     .. _working with virtualenv: http://wiki.pylonshq.com/display/pylonscookbook/Using+a+Virtualenv+Sandbox

    virtualenv
        ``workingenv`` パッケージと `virtual python`_ 構成に取って代わ
        るように設計された、独立した Python 環境を作成するためのツール。
        潜在的なシステム衝突の可能性からパッケージを隔離することに加え、
        `virtualenv`_ は多くのパッケージを system-wide の Python の中に
        ばらまくことなく、 :term:`easy_install` を使用して Python ライ
        ブラリを簡単にインストールできるようにします。

        もう一つのすばらしい利点は、すべてのモジュールを好きなディレク
        トリの下に置くことができるので、 root アクセスは全く必要でない
        ということです。これによって、共有ホスティングプロバイダーや、
        system-wide へのアクセスが入手できない他のシステムに、動作する
        Pylons インストールをセットアップすることが簡単になります。

        ``virtualenv`` は :ref:`getting_started` で説明された
        ``go-pylons.py`` スクリプトによって自動的に使われます。 Pylons
        wiki には、 `working with virtualenv`_ に関するより詳しい情報が
        あります。

        .. _virtual python: http://peak.telecommunity.com/DevCenter/EasyInstall#creating-a-virtual-python
        .. _virtualenv: http://pypi.python.org/pypi/virtualenv
        .. _working with virtualenv: http://wiki.pylonshq.com/display/pylonscookbook/Using+a+Virtualenv+Sandbox


    .. web server gateway interface
    ..     A specification for web servers and application servers to
    ..     communicate with web applications. Also referred to by its
    ..     initials, as :term:`WSGI`.

    web server gateway interface
        ウェブサーバーおよびアプリケーション・サーバーが、ウェブアプリ
        ケーションとコミュニケーションするための仕様。その頭文字を取っ
        て :term:`WSGI` とも呼ばれます。


    .. WSGI
    ..     The `WSGI Specification
    ..     <http://www.python.org/dev/peps/pep-0333/>`_, also commonly
    ..     referred to as PEP 333 and described by :pep:`333`.

    WSGI
        `WSGI 仕様
        <http://wiki.pylonshq.com/display/pylonsja/PEP333-ja>`_ は PEP
        333 とも呼ばれ、 :pep:`333` で記述されています。


    .. WSGI Middleware
    ..     :term:`WSGI` Middleware refers to the ability of WSGI
    ..     applications to modify the environ, and/or the content of
    ..     other WSGI applications by being placed in between the
    ..     request and the other WSGI application.
    ..
    ..     .. seealso::
    ..         :ref:`WSGI Middleware in Concepts of Pylons <wsgi-middleware>`
    ..         :ref:`WSGI Middleware Configuration <middleware-config>`

    WSGI Middleware
        :term:`WSGI` Middleware は、リクエストと他の WSGI アプリケーショ
        ンの間に置かれることによって、 environ と他の WSGI アプリケーショ
        ンのコンテンツのどちらかまたは両方を変更する WSGI アプリケーショ
        ンの能力のことを指します。

        .. seealso::

            * :ref:`Pylons のコンセプトにおける WSGI Middleware <wsgi-middleware>`
            * :ref:`WSGI Middleware 設定 <middleware-config>`
