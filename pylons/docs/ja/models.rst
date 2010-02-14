.. _models:

======
モデル
======

.. About the model

モデルについて
===============

.. image:: _static/pylon3.jpg
   :alt: 
   :align: left
   :height: 450px
   :width: 368px

.. In the MVC paradigm the *model* manages the behavior and data of
.. the application domain, responds to requests for information about
.. its state and responds to instructions to change state.

MVC パラダイムでは、 *モデル* はアプリケーションドメインに関する振舞い
とデータを管理します。そして、状態に関する情報のリクエストに応じて、状
態を変えるための指示に応じます。


.. The model represents enterprise data and business rules. It is
.. where most of the processing takes place when using the MVC design
.. pattern. Databases are in the remit of the model, as are component
.. objects such as :term:`EJBs` and :term:`ColdFusion Components`.

モデルはエンタープライズデータとビジネスルールを表します。 MVC デザイン
パターンを使用するとき、大部分の処理はモデルで行われるます。データベー
スは in the remit of the model 。それは :term:`EJBs` や
:term:`ColdFusion Components` のようなコンポーネントオブジェクトです。


.. The data returned by the model is display-neutral, i.e. the model
.. applies no formatting. A single model can provide data for any
.. number of display interfaces. This reduces code duplication as
.. model code is written only once and is then reused by all of the
.. views.

モデルの返すデータは表示中立です。すなわち、モデルはどんなフォーマット
も適用されません。単一のモデルが任意の数の表示インタフェースに対してデー
タを提供できます。 モデルコードは一度だけ書かれるので、これはコードの重
複を抑えて、すべてのビューで再利用されます。


.. Because the model returns data without applying any formatting, the
.. same components can be used with any interface. For example, most
.. data is typically formatted with HTML but it could also be
.. formatted with Macromedia Flash or WAP.

モデルは何のフォーマットも適用しない状態でデータを返すので、同じコンポー
ネントをあらゆるインタフェースで使うことができます。例えば、ほとんどの
データは通常 HTML でフォーマットされますが、 Macromedia Flash や WAP で
フォーマットすることもできます。


.. The model also isolates and handles state management and data
.. persistence. For example, a Flash site or a wireless application
.. can both rely on the same session-based shopping cart and
.. e-commerce processes.

モデルはまた、状態管理とデータ永続を分割し、扱います。例えば、 Flash サ
イトとワイヤレスアプリケーションが、ともに同じセッションベースのショッ
ピングカートと電子商取引プロセスに依存することができます。


.. Because the model is self-contained and separate from the
.. controller and the view, changing the data layer or business rules
.. is less painful. If it proves necessary to switch databases,
.. e.g. from MySQL to Oracle, or change a data source from an RDBMS to
.. LDAP, the only required task is that of altering the model. If the
.. view is written correctly, it won’t care at all whether a list of
.. users came from a database or an LDAP server.

モデルは自己完結的であって、コントローラとビューからは独立しているので、
データ層やビジネスルールを変えるのはそれほど苦痛ではありません。 例えば、
データベースを MySQL から Oracle に切り換えたり、データソースを RDBMS
から LDAP に変えたりする必要があると判明したら、唯一の必要なタスクはモ
デルを変更することです。ビューが正しく書かれていれば、ユーザーリストが
データベースから来たのか、それとも LDAP サーバから来たのか、それは全く
気にしないでしょう。


.. This freedom arises from the way that the three parts of an
.. MVC-based application act as `black boxes`, the inner workings of
.. each one are hidden from, and are independent of, the other
.. two. The approach promotes well-defined interfaces and
.. self-contained components.

この自由度は、 MVC ベースのアプリケーションの 3 つの部分が `ブラックボッ
クス` として振る舞い、それぞれの内部の作業が他から隠されていて、他の 2
つから独立していることから生じます。このアプローチは明確なインタフェー
スと自己完結的なコンポーネントを促進します。


.. note::

    *adapted from an Oct 2002 TechRepublic article by by Brian Kotek:
    "MVC design pattern brings about better organization and code
    reuse"* -
    http://articles.techrepublic.com.com/5100-10878_11-1049862.html


.. Model basics

モデルの基本
============

.. Pylons provides a :data:`model` package to put your database code
.. in but does not offer a database engine or API.  Instead there are
.. several third-party APIs to choose from.

Pylons は、データベースコードを置くために :data:`model` パッケージを提
供していますが、データベースエンジンや API は提供しません。 代わりに、
選択できるいくつかのサードパーティ製 API があります。


.. SQL databases

SQL データベース
-----------------

SQLAlchemy
^^^^^^^^^^

.. `SQLAlchemy <http://www.sqlalchemy.org/>`_ is by far the most
.. common approach for Pylons databases.  It provides a connection
.. pool, a SQL statement builder, an object-relational mapper (ORM),
.. and transaction support.  SQLAlchemy works with several database
.. engines (MySQL, PostgreSQL, SQLite, Oracle, Firebird, MS-SQL,
.. Access via ODBC, etc) and understands the peculiar SQL dialect of
.. each, making it possible to port a program from one engine to
.. another by simply changing the connection string.  Although its API
.. is still changing gradually, SQLAlchemy is well tested, widely
.. deployed, has excellent documentation, and its mailing list is quick
.. with answers.  :ref:`Using SQLAlchemy
.. <working_with_sqlalchemy>` describes the recommended way to
.. configure a Pylons application for SQLAlchemy.

`SQLAlchemy <http://www.sqlalchemy.org/>`_ は Pylons データベースのため
の極めて一般的なアプローチです。 それはコネクションプール、 SQL 文ビル
ダー、オブジェクト・リレーション・マッパー (ORM) 、およびトランザクショ
ンサポートを提供します。 SQLAlchemy はいくつかのデータベースエンジン
(MySQL 、 PostgreSQL 、 SQLite 、 Oracle 、 Firebird 、 MS-SQL 、 ODBC
経由の Access など) とともに働きます。そして、それぞれの独自の SQL 方言
を理解します。これにより、単にコネクション文字列を変えることによって、
あるエンジンから別のエンジンにプログラムを移植することが可能になります。
そのAPI はまだ徐々に変化していますが、 SQLAlchemy は十分テストされ、広
く普及しており、素晴らしいドキュメンテーションがあります。そして、メー
リングリストでは素早く答えが返ってきます。 :ref:`Using SQLAlchemy
<working_with_sqlalchemy>` は、 Pylons アプリケーションを構成するお勧め
の方法を述べます。


.. SQLAlchemy lets you work at three different levels, and you can
.. even use multiple levels in the same program:

SQLAlchemy は次のような 3 つの異なったレベルで動かすことができ、しかも
同じアプリケーションの中で複数のレベルを混在させることもできます:


.. * The object-relational mapper (ORM) lets you interact with the
..   database using your own object classes rather than writing SQL code.
.. * The SQL expression language has many methods to create customized
..   SQL statements, and the result cursor is more friendly than DBAPI's.
.. * The low-level execute methods accept literal SQL strings if you find
..   something the SQL builder can't do, such as adding a column to an
..   existing table or modifying the column's type. If they return
..   results, you still get the benefit of SQLAlchemy's result cursor.

* オブジェクトリレーションマッパー (ORM) は、 SQL コードを書く代わりに
  オブジェクトクラスを使用してデータベースと対話することを可能にします。
* SQL 式言語には、カスタマイズされた SQL 文を作成するための多くのメソッ
  ドがあり、結果のカーソルは DBAPI のものより使いやすいです。
* 低レベル execute メソッドは、 SQL ビルダーができないこと(既存のテーブ
  ルにカラムを追加することや、カラムの型を変更することなど) が見つかっ
  た場合に、リテラルの SQL 文字列を受け付けます。それらが結果を返すなら、
  あなたはまだ SQLAlchemy の結果カーソルの利益を得ています。


.. The first two levels are *database neutral*, meaning they hide the
.. differences between the databases' SQL dialects. Changing to a
.. different database is merely a matter of supplying a new connection
.. URL. Of course there are limits to this, but SQLAlchemy is 90%
.. easier than rewriting all your SQL queries.

最初の 2 つのレベルは *データベース中立* です。その意味は、それらはデー
タベースの SQL 方言の違いを隠すということです。異なるデータベースに変更
するのは、単に新しいコネクション URL を与えるだけです。 これに対する限
界がもちろんありますが、 SQLAlchemy はすべての SQL クエリを書き直すより
90% 簡単です。


.. The `SQLAlchemy manual <http://www.sqlalchemy.org/docs/>`_ should be
.. your next stop for questions not covered here. It's very well written
.. and thorough.

`SQLAlchemy マニュアル <http://www.sqlalchemy.org/docs/>`_ はここで
カバーされなかった質問のために次に読むべきです。 それは、非常に良く書か
れており網羅的です。

 
.. SQLAlchemy add-ons

SQLAlchemy 拡張
^^^^^^^^^^^^^^^^^^

.. Most of these provide a higher-level ORM, either by combining the
.. table definition and ORM class definition into one step, or
.. supporting an "active record" style of access.  *Please take the
.. time to learn how to do things "the regular way" before using these
.. shortcuts in a production application*.  Understanding what these
.. add-ons do behind the scenes will help if you have to troubleshoot
.. a database error or work around a limitation in the add-on later.

これらの大部分は、テーブル定義と ORM クラス定義をワンステップで結合する
か、 "active record" スタイルのアクセスをサポートすることで、より高レベ
ルの ORM を提供します。 *製品アプリケーションでこれらのショートカットを
使用する前に、「通常のやり方」で物事を行う方法を学ぶ時間を取ってくださ
い* 。これらの add-ons が舞台裏で何をしているのかを理解することで、デー
タベースエラーの障害調査をしなければならない場合や、または add-on の層
での制限に対処しなければならない場合に役に立つでしょう。


.. `SQLSoup
.. <http://www.sqlalchemy.org/docs/05/plugins.html#plugins_sqlsoup>`_,
.. an extension to SQLAlchemy, provides a quick way to generate ORM
.. classes based on existing database tables.

`SQLSoup
<http://www.sqlalchemy.org/docs/05/plugins.html#plugins_sqlsoup>`_ は
SQLAlchemy の拡張で、既存のデータベースのテーブルに基づいて ORM クラス
を生成する迅速な方法を提供します。


.. If you're familiar with ActiveRecord, used in Ruby on Rails, then
.. you may want to use the `Elixir <http://elixir.ematia.de/>`_ layer
.. on top of SQLAlchemy.

Ruby on Rails で使われている ActiveRecord になじみ深いなら、
SQLAlchemy の上で `Elixir <http://elixir.ematia.de/>`_ 層を使用するとよ
いかもしれません。


.. `Tesla <http://code.google.com/p/tesla-pylons-elixir/>`_ is a
.. framework built on top of Pylons and Elixir/SQLAlchemy.

`Tesla <http://code.google.com/p/tesla-pylons-elixir/>`_ は Pylons と
Elixir/SQLAlchemy の上に築き上げられたフレームワークです。


.. Non-SQLAlchemy libraries

SQLAlchemy 以外のライブラリ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Most of these expose only the object-relational mapper; their SQL
.. builder and connection pool are not meant to be used directly.

これらの大部分は object-relation マッパーだけを露出します。それらの
SQL ビルダーとコネクションプールは直接使用されることは想定されていませ
ん。


`Storm <http://storm.canonical.com>`_

DB-API
++++++

.. All the SQL libraries above are built on top of Python's DB-API,
.. which provides a common low-level interface for interacting with
.. several database engines: MySQL, PostgreSQL, SQLite, Oracle,
.. Firebird, MS-SQL, Access via ODBC, etc.  Most programmers do not
.. use DB-API directly because its API is low-level and repetitive and
.. does not provide a connection pool.  There's no "DB-API package" to
.. install because it's an abstract interface rather than software.
.. Instead, install the Python package for the particular engine
.. you're interested in.  Python's `Database Topic Guide
.. <http://www.python.org/topics/database/>`_ describes the DB-API and
.. lists the package required for each engine.  The `sqlite3
.. <http://docs.python.org/lib/module-sqlite3.html>`_ package for
.. SQLite is included in Python 2.5.

上記のすべての SQL ライブラリは、 Python の DB-API の上に構築されていま
す。 DB-API は MySQL 、 PostgreSQL 、 SQLite 、 Oracle 、Firebird 、
MS-SQL 、 ODBC 経由の Access など、いくつかのデータベースエンジンと対話
するための共通の低レベルインタフェースを提供します。 DB-API は低レベル
で繰り返しが多く、コネクションプールを提供しないので、ほとんどのプログ
ラマは DB-API を直接使用しません。それはソフトウェアというよりむしろ抽
象的なインタフェースなので、インストールするための「DB-APIパッケージ」
というものはありません。代わりに、あなたが興味のある特定のエンジンのた
めの Python パッケージをインストールしてください。 Python `Database
Topic Guide <http://www.python.org/topics/database/>`_ は、 DB-API につ
いて説明し、各エンジンのために必要とされるパッケージをリストします。
SQLite のための `sqlite3
<http://docs.python.org/lib/module-sqlite3.html>`_ パッケージは Python
2.5 に含まれています。


.. Object databases

オブジェクトデータベース
------------------------

.. Object databases store Python dicts, lists, and classes in pickles,
.. allowing you to access hierarchical data using normal Python
.. statements rather than having to map them to tables, relations, and
.. a foreign language (SQL).

オブジェクトデータベースは、 Python 辞書、リスト、およびクラスを
pickle 形式で保存できます。階層データをテーブル、リレーション、および外
国語 (SQL) に写像する代わりに、通常の Python 文を使用してそれらにアクセ
スすることができます。


`ZODB <http://wiki.zope.org/ZODB/FrontPage>`_

`Durus <http://www.mems-exchange.org/software/durus/>`_ [#]_

.. .. [#] Durus is not thread safe, so you should use its server mode
..    if your application writes to the database.  Do not share
..    connections between threads.  ZODB is thread safe, so it may be
..    a more convenient alternative.

.. [#] Durus はスレッド・セーフではないので、アプリケーションがデータベー
   スに書き込むなら Durus のサーバモードを使用するべきです。スレッド間
   でコネクションを共有してはいけません。 ZODB はスレッド・セーフなので、
   それはより便利な代替手段になるかもしれません。


.. Other databases

その他のデータベース
---------------------

.. Pylons can also work with other database systems, such as the
.. following:

Pylons は以下のような他のデータベース・システムとも動かすことができます:


.. `Schevo <http://schevo.org/>`_ uses Durus to combine some features
.. of relational and object databases.  It is written in Python.

`Schevo <http://schevo.org/>`_ は、リレーショナルデータベースとオブジェ
クトデータベースのいくつかの特徴を結合するために Durus を使用します。
それは Python で書かれています。


.. `CouchDb <http://couchdb.org/>`_ is a document-based database.  It
.. features a `Python API
.. <http://code.google.com/p/couchdb-python/>`_.

`CouchDb <http://couchdb.org/>`_ はドキュメントベースのデータベースです。
それは `Python API <http://code.google.com/p/couchdb-python/>`_ を特徴
としています。


.. The Datastore database in Google App Engine.

Google App Engine の Datastore データベース。


.. Working with SQLAlchemy

.. _working_with_sqlalchemy:

SQLAlchemy を使う
=======================

.. Install SQLAlchemy

SQLAlchemy のインストール
--------------------------


.. We'll assume you've already installed Pylons and have the
.. `easy_install` command. At the command line, run:

あなたが既に Pylons をインストールして、 `easy_install` コマンドを持っ
ていると仮定します。 コマンドラインで、以下を実行してください:


.. code-block:: bash

    easy_install SQLAlchemy 


.. Next you'll have to install a database engine and its Python
.. bindings. If you don't know which one to choose, SQLite is a good
.. one to start with. It's small and easy to install, and Python 2.5
.. includes bindings for it. Installing the database engine is beyond
.. the scope of this article, but here are the Python bindings you'll
.. need for the most popular engines:

次に、データベースエンジンとその Python バインディングをインストールし
なければなりません。 どれを選んだらよいか分からなければ、 SQLite は最初
に選択するのに良いものです。それは小さくて、インストールするのが簡単で
あり、Python 2.5 はそのためのバインディングを含んでいます。 データベー
スエンジンをインストールすることはこの記事の範囲を超えていますが、これ
らは最もポピュラーなエンジンに必要とされる Python バインディングです:


.. code-block:: bash

    easy_install pysqlite # If you use SQLite and Python 2.4 (not needed for Python 2.5) 
    easy_install MySQL-python # If you use MySQL 
    easy_install psycopg2 # If you use PostgreSQL 


.. See the `Python Package Index <http://pypi.python.org/>`_ (formerly
.. the Cheeseshop) for other database drivers.

他のデータベースドライバーは `Python Package Index
<http://pypi.python.org/>`_ (以前の Cheeseshop)を見てください。



.. Check Your Version 

バージョンをチェックする
^^^^^^^^^^^^^^^^^^^^^^^^

.. To see which version of SQLAlchemy you have, go to a Python shell
.. and look at sqlalchemy.\_\_version\_\_ :

SQLAlchemy のどのバージョンがインストールされているかを確認するために、
Python シェルに行き、 sqlalchemy.__version__ を見てください:


.. code-block:: python

    >>> import sqlalchemy 
    >>> sqlalchemy.__version__ 
    0.5.0


Defining tables and ORM classes
-------------------------------

.. When you answer "yes" to the SQLAlchemy question when creating a
.. Pylons project, it configures a simple default model.  The model
.. consists of two files: *__init__.py* and *meta.py*.  *__init__.py*
.. contains your table definitions and ORM classes, and an
.. ``init_model()`` function which must be called at application
.. startup.  *meta.py* is merely a container for SQLAlchemy's
.. housekeeping objects (``Session``, ``metadata``, and ``engine``),
.. which not all applications will use.  If your application is small,
.. you can put your table definitions in *__init__.py* for simplicity.
.. If your application has many tables or multiple databases, you may
.. prefer to split them up into multiple modules within the model.

Pylons プロジェクトを作るときに SQLAlchemy の質問に "yes" と答えた場合、
簡単なデフォルトモデルが構成されます。 モデルは 2 つのファイルから成り
ます: *__init__.py* と *meta.py* です。 *__init__.py* はテーブル定義と
ORM のクラス、およびアプリケーション開始時に呼ばなければならない
``init_model()`` 関数を含んでいます。 *meta.py* は単に SQLAlchemy のハ
ウスキーピングのオブジェクト (``Session``, ``metadata``, ``engine``) の
ためのコンテナです。これらはすべてのアプリケーションで使用するわけでは
ないでしょう。アプリケーションが小さいなら、簡潔さのためにテーブル定義
を *__init__.py* に入れることができます。アプリケーションに多くのテーブ
ルや複数のデータベースがあるなら、それらをモデルの中の複数のモジュール
に分けると良いかもしれません。


.. Here's a sample *model/__init__.py* with a "persons" table, which
.. is based on the default model with the comments removed:

ここに、サンプルの *model/__init__.py* と "persons" テーブルがあります
(which is based on the default model with the comments removed):


.. code-block:: python

    """The application's model objects"""
    import sqlalchemy as sa
    from sqlalchemy import orm

    from myapp.model import meta

    def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        ## Reflected tables must be defined and mapped here
        #global reflected_table
        #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
        #                           autoload_with=engine)
        #orm.mapper(Reflected, reflected_table)
        #
        meta.Session.configure(bind=engine)
        meta.engine = engine


    t_persons = sa.Table("persons", meta.metadata,
        sa.Column("id", sa.types.Integer, primary_key=True),
        sa.Column("name", sa.types.String(100), primary_key=True),
        sa.Column("email", sa.types.String(100)),
        )

    class Person(object):
        pass

    orm.mapper(Person, t_persons)


.. This model has one table, "persons", assigned to the variable
.. ``t_persons``.  ``Person`` is an ORM class which is tied to the
.. table via the mapper.

このモデルには、 変数 ``t_persons`` に割り当てられた 1 個のテーブル
"persons" があります。 ``Person`` はマッパーを通してテーブルに結びつけ
られた ORM のクラスです。


.. If the table already exists, you can read its column definitions
.. from the database rather than specifying them manually; this is
.. called *reflecting* the table.  The advantage is you don't have to
.. specify the column types in Python code.  Reflecting must be done
.. inside ``init_model()`` because it depends on a live database
.. engine, which is not available when the module is imported.  (An
.. *engine* is a SQLAlchemy object that knows how to connect to a
.. particular database.)  Here's the second example with reflection:

テーブルが既に存在しているなら、手動でカラム定義を指定する代わりにデー
タベースからそれを読むことができます。 これはテーブルの *リフレクション*
と呼ばれます。 利点は Python コードでカラムタイプを指定する必要がないと
いうことです。リフレクションは生きたデータベースエンジンを必要とするた
め、 ``init_model()`` の中で行わなければなりません。モジュールがインポー
トされるときにエンジンは利用可能でないからです (*エンジン* とは、特定の
データベースにどのように接続すればよいかを知っている SQLAlchemy のオブ
ジェクトです)。ここに、リフレクションを使用した 2 番目の例があります:


.. code-block:: python

    """The application's model objects"""
    import sqlalchemy as sa
    from sqlalchemy import orm

    from myapp.model import meta

    def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        # Reflected tables must be defined and mapped here
        global t_persons
        t_persons = sa.Table("persons", meta.metadata, autoload=True,
                             autoload_with=engine)
        orm.mapper(Person, t_persons)

        meta.Session.configure(bind=engine)
        meta.engine = engine


    t_persons = None

    class Person(object):
        pass


.. Note how ``t_persons`` and the ``orm.mapper()`` call moved into
.. ``init_model``, while the ``Person`` class didn't have to.  Also
.. note the ``global t_persons`` statement.  This tells Python that
.. ``t_persons`` is a global variable outside the function.
.. ``global`` is required when assigning to a global variable inside a
.. function.  It's not required if you're merely modifying a mutable
.. object in place, which is why ``meta`` doesn't have to be declared
.. global.

``t_persons`` と ``orm.mapper()`` 呼び出しがどのように
``init_model()`` に移動されたか、その一方で ``Person`` クラスを移動する
必要がなかったことに注意してください。また、 ``global t_persons`` 文に
注意してください。これは ``t_persons`` が関数外の大域変数であると
Python に伝えます。関数内部で大域変数に代入するときは ``global`` が必要
です。単に mutable なオブジェクトを in place で変更するだけなら、それは
必要ではありません (これは ``meta`` を global と宣言する必要がない理由
です)。


.. SQLAlchemy 0.5 has an optional Declarative syntax which defines the
.. table and the ORM class in one step:

SQLAlchemy 0.5 には、 1 ステップでテーブルと ORM クラスを定義するための
オプションの Declarative (宣言的) 構文があります:


.. code-block:: python

    """The application's model objects"""
    import sqlalchemy as sa
    from sqlalchemy import orm
    from sqlalchemy.ext.declarative import declarative_base

    from myapp.model import meta

    _Base = declarative_base()

    def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        meta.Session.configure(bind=engine)
        meta.engine = engine


    class Person(_Base):
        __tablename__ = "persons"

        id = sa.Column(sa.types.Integer, primary_key=True)
        name = sa.Column(sa.types.String(100))
        email = sa.Column(sa.types.String(100))


.. Relation example 

関連の例
^^^^^^^^^^^^^^^^

.. Here's an example of a `Person` and an `Address` class with a
.. many:many relationship on `people.my_addresses`. See `Relational
.. Databases for People in a Hurry
.. <http://wiki.pylonshq.com/display/pylonscookbook/Relational+databases+for+people+in+a+hurry>`_
.. and the SQLAlchemy manual for details.

ここに、 `Person` クラスと `Address` クラス、そして
`people.my_addresses` 上の多対他関連に関する例があります。詳細に関して
は `Relational Databases for People in a Hurry
<http://wiki.pylonshq.com/display/pylonscookbook/Relational+databases+for+people+in+a+hurry>`_
と SQLAlchemy マニュアルを見てください。


.. code-block:: python

    t_people = sa.Table('people', meta.metadata, 
        sa.Column('id', sa.types.Integer, primary_key=True), 
        sa.Column('name', sa.types.String(100)), 
        sa.Column('email', sa.types.String(100)),
        ) 

    t_addresses_people = sa.Table('addresses_people', meta.metadata, 
        sa.Column('id', sa.types.Integer, primary_key=True), 
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('people.id')), 
        sa.Column('address_id', sa.types.Integer, sa.ForeignKey('addresses.id')),
        ) 

    t_addresses = sa.Table('addresses', meta.metadata, 
        sa.Column('id', sa.types.Integer, primary_key=True), 
        sa.Column('address', sa.types.String(100)),
        ) 

    class Person(object): 
        pass 

    class Address(object): 
        pass 

    orm.mapper(Address, t_addresses) 
    orm.mapper(Person, t_people, properties = { 
        'my_addresses' : orm.relation(Address, secondary = t_addresses_people), 
        }) 


.. Using the model standalone 

スタンドアローンでモデルを使用する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. You now have everything necessary to use the model in a standalone
.. script such as a cron job, or to test it interactively. You just
.. need to create a SQLAlchemy engine and connect it to the
.. model. This example uses a database "test.sqlite" in the current
.. directory:

ここまでで cron ジョブなどのスタンドアロンスクリプトでモデルを使用した
り、インタラクティブにモデルをテストするために必要なものはすべて揃って
います。あなたは、ただ SQLAlchemy engine を作成して、それをモデルに接続
する必要があります。 この例はカレントディレクトリ中の "test.sqlite" と
いうデータベースを使用します:


.. code-block:: pycon

    % python 
    Python 2.5.1 (r251:54863, Oct 5 2007, 13:36:32) 
    [GCC 4.1.3 20070929 (prerelease) (Ubuntu 4.1.2-16ubuntu2)] on linux2 
    Type "help", "copyright", "credits" or "license" for more information. 
    >>> import sqlalchemy as sa 
    >>> engine = sa.create_engine("sqlite:///test.sqlite") 
    >>> from myapp import model 
    >>> model.init_model(engine) 


.. Now you can use the tables, classes, and Session as described in
.. the SLQAlchemy manual.  For example:

すると、 SLQAlchemy マニュアルで説明されるようにテーブル、クラス、およ
び Session を使用できます。例えば:


.. code-block:: python

    #!/usr/bin/env python
    import sqlalchemy as sa
    import tmpapp.model as model
    import tmpapp.model.meta as meta

    DB_URL = "sqlite:///test.sqlite" 

    engine = sa.create_engine(DB_URL)
    model.init_model(engine)

    # Create all tables, overwriting them if they exist.
    if hasattr(model, "_Base"):
        # SQLAlchemy 0.5 Declarative syntax
        model._Base.metadata.drop_all(bind=engine, checkfirst=True)
        model._Base.metadata.create_all(bind=engine)
    else:
        # SQLAlchemy 0.4 and 0.5 syntax without Declarative
        meta.metadata.drop_all(bind=engine, checkfirst=True)
        meta.metadataa.create_all(bind=engine)

    # Create two records and insert them into the database using the ORM.
    a = model.Person()
    a.name = "Aaa"
    a.email = "aaa@example.com"
    meta.Session.add(a)

    b = model.Person()
    b.name = "Bbb"
    b.email = "bbb@example.com"
    meta.Session.add(b)

    meta.Session.commit()

    # Display all records in the persons table.
    print "Database data:"
    for p in meta.Session.query(model.Person):
        print "id:", p.id
        print "name:", p.name
        print "email:", p.email
        print


.. The config file

設定ファイル
---------------

.. When your Pylons application runs, it needs to know which database
.. to connect to. Normally you put this information in
.. *development.ini* and activate the model in *environment.py*. Put
.. the following in *development.ini* in the `\[app:main\]` section,
.. depending on your database,

Pylons アプリケーションは、実行されるときにどのデータベースに接続するか
を知る必要があります。 通常、 *development.ini* にこの情報を入れて、
*environment.py* でモデルを activate します。使用するデータベースに応じ
て、以下を *development.ini* の `\[app:main\]` セクションに置いてくださ
い:


.. For SQLite 

SQLite の設定
^^^^^^^^^^^^^^

.. code-block:: ini

    sqlalchemy.url = sqlite:///%(here)s/mydatabasefilename.sqlite 


.. Where `mydatabasefilename.db` is the path to your SQLite database
.. file. "%(here)s" represents the directory containing the
.. development.ini file. If you're using an absolute path, use four
.. slashes after the colon:
.. "sqlite:////var/lib/myapp/database.sqlite". Don't use a relative
.. path (three slashes) because the current directory could be
.. anything. The example has three slashes because the value of
.. "%(here)s" always starts with a slash (or the platform equivalent;
.. e.g., "C:\\foo" on Windows).

ここで `mydatabasefilename.db` は SQLite データベースファイルへのパスで
す。"%(here)s" は development.ini ファイルを含むディレクトリを表します。
絶対パスを使用するなら、コロンの後に 4 つのスラッシュを使用してください:
"sqlite:////var/lib/myapp/database.sqlite" 。カレントディレクトリが何で
あるか分からないので、相対パス (スラッシュ 3 つ) は使用しないでください。
例では 3 つのスラッシュが使われていますが、これは "%(here)s" の値は常に
スラッシュ (またはプラットホームの同等物; 例えば Windows では
"C:\\foo") から始まるためです。


.. For MySQL 

MySQL の設定
^^^^^^^^^^^^^


.. code-block:: ini

    sqlalchemy.url = mysql://username:password@host:port/database 
    sqlalchemy.pool_recycle = 3600 


.. Enter your username, password, host (localhost if it is on your
.. machine), port number (usually 3306) and the name of your
.. database. The second line is an example of setting `engine options
.. <http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_options>`_.

ユーザ名、パスワード、ホスト (自分のマシン上であれば localhost)、ポート
番号 (通常は 3306)、およびデータベースの名前を入力してください。2 行目
は `engine オプション
<http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_options>`_ を
設定する例です。


.. It's important to set "pool_recycle" for MySQL to prevent "MySQL
.. server has gone away" errors. This is because MySQL automatically
.. closes idle database connections without informing the
.. application. Setting the connection lifetime to 3600 seconds (1
.. hour) ensures that the connections will be expired and recreated
.. before MySQL notices they're idle.

MySQL の場合、 "MySQL server has gone away" エラーを防ぐために
"pool_recycle" をセットすることは重要です。これは、 MySQL がアプリケー
ションに知らせずに idle なデータベースコネクションを自動的に閉じるから
です。 コネクション存続期間を 3600 秒 (1時間) に設定することで、コネク
ションがidle であると MySQL が判断する前に有効期限が切れて再接続するよ
うになります。


.. Don't be tempted to use the ".echo" option to enable SQL logging
.. because it may cause duplicate log output. Instead see the
.. "Logging" section below to integrate MySQL logging into Paste's
.. logging system.

SQL ログを有効にするのに ".echo" オプションを使いたくなるかもしれません
が、それは重複するログ出力を引き起こすので使わないようにしてください。
代わりに下の "Logging" セクションを見て、 MySQL ログを Paste のログシス
テムに統合してください。


.. For PostgreSQL 

PostgreSQL の設定
^^^^^^^^^^^^^^^^^^


.. code-block:: ini

    sqlalchemy.url = postgres://username:password@host:port/database 


.. Enter your username, password, host (localhost if it is on your
.. machine), port number (usually 5432) and the name of your database.

ユーザ名、パスワード、ホスト (自分のマシン上なら localhost)、ポート番号
(通常は 5432)、およびデータベースの名前を入力してください。


.. The engine

エンジン
----------

.. Put this at the top of *myapp/config/environment.py*: 

*myapp/config/environment.py* の先頭にこれを置いてください:


.. code-block:: python

    from sqlalchemy import engine_from_config 
    from myapp.model import init_model 


.. And this in the `load_environment` function: 

そしてこれを `load_environment` 関数に置いてください:

.. code-block:: python

    engine = engine_from_config(config, 'sqlalchemy.') 
    init_model(engine) 


.. The second argument is the prefix to look for. If you named your
.. keys "sqlalchemy.default.url", you would put "sqlalchemy.default."
.. here. The prefix may be anything, as long as it's consistent
.. between the config file and this function call.

2番目の引数は検索する接頭語です。キーが "sqlalchemy.default.url" という
名前なら、これは "sqlalchemy.default." になります。設定ファイルとこの関
数呼び出しの間で一貫している限り、接頭語は何でも構いません。


.. Controller

コントローラ
------------

.. The paster create SQLAlchemy option adds the following to the top of
.. *myapp/lib/base.py* (the base controller):

paster create SQLAlchemy オプションは *myapp/lib/base.py* (ベースコント
ローラ) の先頭に以下を追加します:


.. code-block:: python

    from myapp.model import meta 


.. and also changes the `.\_\_call\_\_` method to: 

そして、 `.\_\_call\_\_` メソッドを以下のように変更します:


.. code-block:: python

    def __call__(self, environ, start_response): 
        try: 
            return WSGIController.__call__(self, environ, start_response) 
        finally: 
            meta.Session.remove() 


.. The .remove() method is so that any leftover ORM data in the
.. current web request is discarded. This usually happens
.. automatically as a product of garbage collection but calling
.. .remove() ensures this is the case.

.remove() メソッドは、現在のウェブリクエストにおける ORM データのあらゆ
る残り物が捨てられるようにします。これは通常ガーベージコレクションの
product として自動的に起こりますが、.remove() を呼ぶことでそれを確実に
します。


.. Building the database

データベースを構築する
-----------------------

.. To actually create the tables in the database, you call the
.. metadata's `.create_all()` method. You can do this interactively or
.. use `paster`'s application initialization feature. To do this, put
.. the code in *myapp/websetup.py*. After the `load_environment()`
.. call, put:

データベースに実際にテーブルを作成するために、メタデータの
`.create_all()` メソッドを呼びます。インタラクティブにこれをするか、ま
たは `paster` のアプリケーション初期化機能を使用できます。これをするた
めに、 *myapp/websetup.py* にコードを追加します。 `load_environment()`
呼び出しの後に、以下を置いてください:


.. code-block:: python

    from myapp.model import meta 
    log.info("Creating tables") 
    meta.metadata.drop_all(bind=meta.engine, checkfirst=True)
    meta.metadata.create_all(bind=meta.engine) 
    log.info("Successfully setup") 


.. Or for the new SQLAlchemy 0.5 Declarative syntax:

または、 SQLAlchemy 0.5 の新しい Declarative 構文に対しては:


.. code-block:: python

    from myapp import model
    log.info("Creating tables") 
    model._Base.metadata.drop_all(bind=meta.engine, checkfirst=True)
    model._Base.metadata.create_all(bind=meta.engine) 
    log.info("Successfully setup") 


.. Then run the following on the command line: 

そしてコマンドラインから以下を実行します:


.. code-block:: bash

    $ paster setup-app development.ini 


.. Data queries and modifications

データのクエリと修正
------------------------------

.. important::  

    .. this section assumes you're putting the code in a high-level
    .. model function. If you're putting it directly into a controller
    .. method, you'll have to put a `model.` prefix in front of every
    .. object defined in the model, or import the objects
    .. individually. Also note that the `Session` object here (capital
    .. s) is not the same as the Beaker `session` object (lowercase s)
    .. in controllers.

    このセクションは、コードを高レベルのモデル関数に入れること
    を想定しています。 コントローラメソッドに直接コードを入れるなら、
    モデルで定義されたあらゆるオブジェクトの前に `model.` を置くか、オ
    ブジェクトを個別にインポートする必要があるでしょう。また、ここでの
    `Session` オブジェクト (大文字の s) が、コントローラにおける
    Beaker `session` オブジェクト (小文字の s) と同じでないことに注意し
    てください。


.. Here's how to enter new data into the database: 

これは、新しいデータをデータベースに入力する方法です:


.. code-block:: python

    mr_jones = Person() 
    mr_jones.name = 'Mr Jones' 
    meta.Session.add(mr_jones) 
    meta.Session.commit() 


.. `mr_jones` here is an instance of `Person`. Its properties
.. correspond to the column titles of `t_people` and contain the data
.. from the selected row. A more sophisticated application would have
.. a `Person.\_\_init\_\_` method that automatically sets attributes
.. based on its arguments.

ここで `mr_jones` は `Person` のインスタンスです。そのプロパティが
`t_people` のカラムに対応していて、選択された行からのデータを含んでいま
す。より精巧なアプリケーションには、引数に基づいて自動的に属性を設定す
る `Person.__init__` メソッドがあるでしょう。


.. An example of loading a database entry in a controller method,
.. performing a sex change, and saving it:

コントローラメソッドでデータベースエントリをロードして、性別の変化を実
行して、それを保存する例です:


.. code-block:: python

    person_q = meta.Session.query(Person) # An ORM Query object for accessing the Person table 
    mr_jones = person_q.filter(Person.name=='Mr Jones').one() 
    print mr_jones.name # prints 'Mr Jones' 
    mr_jones.name = 'Mrs Jones' # only the object instance is changed here ... 
    meta.Session.commit() # ... only now is the database updated 


.. To return a list of entries use:

エントリのリストを返すのに、以下を使用してください。


.. code-block:: python

    all_mr_joneses = person_q.filter(Person.name=='Mr Jones').all() 


.. To get all list of all the people in the table use: 

テーブルのすべての人のすべてのリストを得るには、以下を使用してください。


.. code-block:: python

    everyone = person_q.all() 


.. To retrieve by id: 

id で検索する場合:


.. code-block:: python

    someuser = person_q.get(5) 


.. You can iterate over every person even more simply: 

もっと簡単に、すべての人に対して繰り返すことができます:


.. code-block:: python

    print "All people" 
    for p in person_q: 
        print p.name 
    print 
    print "All Mr Joneses:" 
    for p in person_q.filter(Person.name=='Mr Jones'): 
        print p.name 


.. To delete an entry use the following: 

エントリーを削除するには、以下を使用してください:


.. code-block:: python

    mr_jones = person_q.filter(Person.name=='Mr Jones').one() 
    meta.Session.delete(mr_jones) 
    meta.Session.commit() 


.. Working with joined objects 

join されたオブジェクトを使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Recall that the `my_addresses` property is a list of `Address`
.. objects

`my_addresses` プロパティは `Address` オブジェクトのリストであったこと
を思い出してください。


.. code-block:: python

    print mr_jones.my_addresses[0].address # prints first address 


.. To add an existing address to 'Mr Jones' we do the following:

'Mr Jones' に既存のアドレスを加えるためには、以下をします:


.. code-block:: python

    address_q = meta.Session.query(Address) 
    
    # Retrieve an existing address 
    address = address_q.filter(Address.address=='33 Pine Marten Lane, Pleasantville').one()
    
    # Add to the list 
    mr_jones.my_addresses.append(new_address)
    
    # issue updates to the join table
    meta.Session.commit()  


.. To add an entirely new address to 'Mr Jones' we do the following:

'Mr Jones' にまったく新しいアドレスを追加するために、以下をします:


.. code-block:: python

    new_address = Address() # Construct an empty address object 
    new_address.address = '33 Pine Marten Lane, Pleasantville' 
    mr_jones.my_addresses.append(new_address) # Add to the list 
    meta.Session.commit() # Commit changes to the database 


.. After making changes you must call `meta.Session.commit()` to store
.. them permanently in the database; otherwise they'll be discarded at
.. the end of the web request. You can also call
.. `meta.Session.rollback()` at any time to undo any changes that
.. haven't been committed.

変更を行った後に、 `meta.Session.commit()` を呼んでそれらをデータベース
に永久に格納する必要があります。さもなければ、それらはウェブリクエスト
の終わりに捨てられるでしょう。 また、コミットされていないあらゆる変更を
元に戻すために、いつでも `meta.Session.rollback()` を呼ぶことができます。


.. To search on a joined object we can pass an entire object as a
.. query:

join されたオブジェクトを対象に検索するために、クエリとしてオブジェクト
全体を渡すことができます:


.. code-block:: python

    search_address = Address() 
    search_address.address = '33 Pine Marten Lane, Pleasantville' 
    residents_at_33_pine_marten_lane = \
        person_q.filter(Person.my_addresses.contains(search_address)).all() 


.. * All attributes must match in the query object. 

クエリオブジェクトのすべての属性がマッチしなければなりません。


.. Or we can can search on a joined objects' property, 

または、 join されたオブジェクトのプロパティを検索することができます。


.. code-block:: python

    residents_at_33_pine_marten_lane = \
     person_q.join('my_addresses').filter(
        Address.address=='33 Pine Marten Lane, Pleasantville').all() 


.. A shortcut for the above is to use `any()`:

上記の近道は `any()` を使用することです:


.. code-block:: python

    residents_at_33_pine_marten_lane = \
     person_q.filter(Person.my_addresses.any(
        Address.address=='33 Pine Marten Lane, Pleasantville')).all() 



.. To disassociate an address from Mr Jones we do the following: 

Mr Jones からアドレスを分離するために、以下をします:


.. code-block:: python

    del mr_jones.my_addresses[0] # Delete the reference to the address 
    meta.Session.commit() 


.. To delete the address itself in the address table, normally we'd
.. have to issue a separate `delete()` for the `Address` object
.. itself:

address テーブルのアドレス自体を削除するために、通常 `Address` オブジェ
クト自体のために別々の `delete()` を発行しなければなりません:


.. code-block:: python

    meta.Session.delete(mr_jones.my_addresses[0]) # Delete the Address object 
    del mr_jones.my_addresses[0] 
    meta.Session.commit() # Commit both operations to the database 


.. However, SQLAlchemy supports a shortcut for the above
.. operation. Configure the mapper relation using `cascade = "all,
.. delete-orphan"` instead:

しかしながら、 SQLAlchemy は上の操作のために近道をサポートします。マッ
パーリレーションを構成する際に、代わりに `cascade = "all,
delete-orphan"` を使用してください:


.. code-block:: python

    orm.mapper(Address, t_addresses) 
    orm.mapper(Person, t_people, properties = { 
    'my_addresses': orm.relation(
            Address, secondary=t_addresses_people, cascade="all,delete-orphan"), 
    }) 


.. Then, any items removed from `mr_jones.my_addresses` is automatically
.. deleted from the database:

すると、 `mr_jones.my_addresses` から取り除かれた項目は、データベースか
らも自動的に削除されます:


.. code-block:: python

    del mr_jones.my_addresses[0] # Delete the reference to the address, 
                                 # also deletes the Address 
    meta.Session.commit() 


.. For any relationship, you can add `cascade = "all, delete-orphan"` as
.. an extra argument to `relation()` in your mappers to ensure that when
.. a join is deleted the joined object is deleted as well, so that the
.. above delete() operation is not needed - only the removal from the
.. `my_addresses` list. Beware though that despite its name,
.. `delete-orphan` removes joined objects even if another object is
.. joined to it.

マッパーのどんな関係にも、 join が削除されたときに join されたオブジェ
クトも同時に削除されるように `relation()` の追加の引数として`cascade =
"all, delete-orphan"` を渡すことができます。従って上の delete() 操作は
必要ありません。 `my_addresses` リストから削除するだけです。ただし、そ
の名前にもかかわらず `delete-orphan` は、別のオブジェクトがそれに join
していたとしても、 join されたオブジェクトを取り除くことに注意してくだ
さい


.. Non-ORM SQL queries 

非 ORM SQL クエリ
^^^^^^^^^^^^^^^^^^^

.. Use `meta.Session.execute()` to execute a non-ORM SQL query within
.. the session's transaction. Bulk updates and deletes can modify
.. records significantly faster than looping through a query and
.. modifying the ORM instances.

セッションのトランザクション中で 非 ORM SQL クエリを実行するには、
`meta.Session.execute()` を使用してください。 bulk update と delete は、
クエリでループして ORM インスタンスを変更するよりかなり速くレコードを変
更できます。


.. code-block:: python

    q = sa.select([table1.c.id, table1.c.name], order_by=[table1.c.name]) 
    records = meta.Session.execute(q).fetchall() 

    # Example of a bulk SQL UPDATE. 
    update = table1.update(table1.c.name=="Jack") 
    meta.Session.execute(update, name="Ed") 
    meta.Session.commit() 

    # Example of updating all matching records using an expression. 
    update = table1.update(values={table1.c.entry_id: table1.c.entry_id + 1000}) 
    meta.Session.exececute(update) 
    meta.Session.commit() 

    # Example of a bulk SQL DELETE. 
    delete = table1.delete(table1.c.name.like("M%")) 
    meta.Session.execute(delete) 
    meta.Session.commit() 

    # Database specific, use only if SQLAlchemy doesn't have methods to construct the desired query. 
    meta.Session.execute("ALTER TABLE Foo ADD new_column (VARCHAR(255)) NOT NULL") 


.. warning::

    .. The last example changes the database structure and may
    .. adversely interact with ORM operations.

    最後の例は、データベース構造を変えるので、ORM 操作に悪影響を及ぼす
    かもしれません。


Further reading 
^^^^^^^^^^^^^^^

.. The Query object has many other features, including filtering on
.. conditions, ordering the results, grouping, etc. These are
.. excellently described in the SQLAlchemy manual. See especially the
.. `Data Mapping <http://www.sqlalchemy.org/docs/datamapping.html>`_
.. and `Session / Unit of Work
.. <http://www.sqlalchemy.org/docs/unitofwork.html>`_ chapters.

Query オブジェクトには、条件によるフィルタリング、結果の並び替え、グルー
ピングを含む他の多くの特徴があります。これらは SQLAlchemy マニュアルに
優れた説明があります。 特に `Data Mapping
<http://www.sqlalchemy.org/docs/datamapping.html>`_ と `Session / Unit
of Work <http://www.sqlalchemy.org/docs/unitofwork.html>`_ の章を見てく
ださい。


.. Testing Your Models

モデルをテストする
-------------------

.. Normal model usage works fine in model tests, however to use the
.. metadata you must specify an engine connection for it. To have your
.. tables created for every unit test in your project, use a
.. test_models.py such as:

通常のモデルの使い方はモデルテストでも同様にうまく働きますが、メタデー
タを使用するためには、そのためのエンジンコネクションを指定しなければな
りません。プロジェクトの中で毎回ユニットテストの度にテーブルを作成する
ために、以下のような test_models.py を使用してください。


.. code-block:: python

    from myapp.tests import * 
    from myapp import model 
    from myapp.model import meta 

    class TestModels(TestController):

        def setUp(self): 
            meta.Session.remove() 
            meta.metadata.create_all(meta.engine) 

        def test_index(self): 
            # test your models 
            pass


.. note::

    .. Notice that the tests inherit from TestController. This is to
    .. ensure that the application is setup so that the models will
    .. work.

    テストが TestController から派生されることに注意してください。 これ
    は、モデルが動くようにアプリケーションがセットアップされることを保
    証するためのものです。


.. "nosetests --with-pylons=/path/to/test.ini ..." is another way to
.. ensure that your model is properly initialized before the tests are
.. run. This can be used when running non-controller tests.

"nosetests --with-pylons=/path/to/test.ini ..." は、テストが実行される
前にモデルが適切に初期化されるのを保証する別の方法です。これは非コント
ローラテストを実行するときに使用できます。


.. Multiple engines

複数のエンジン
----------------

.. Some applications need to connect to multiple databases
.. (engines). Some always bind certain tables to the same engines
.. (e.g., a general database and a logging database); this is called
.. "horizontal partitioning". Other applications have several
.. databases with the same structure, and choose one or another
.. depending on the current request. A blogging app with a separate
.. database for each blog, for instance. A few large applications
.. store different records from the same logical table in different
.. databases to prevent the database size from getting too large; this
.. is called "vertical partitioning" or "sharding". The pattern above
.. can accommodate any of these schemes with a few minor changes.

いくつかのアプリケーションでは、複数のデータベース (エンジン) に接続す
る必要があります。 あるアプリケーションは、特定のテーブルをいつも同じエ
ンジンに bind します (例えば、一般的なデータベースとログデータベース)。
これは「水平パーティショニング」と呼ばれます。 他のアプリケーションは、
同じ構造を持ついくつかのデータベースを持っていて、現在のリクエストによっ
て、どれかを選びます。 例えば、それぞれのブログのための別々のデータベー
スを持ったウェブログアプリです。 大きなアプリケーションでは、データベー
スサイズが大きくなり過ぎるのを防ぐために、同じ論理的なテーブルからの別
のレコードを別のデータベースに保存します。これは「垂直パーティショニン
グまたは sharding」と呼ばれます。 上のパターンはいくつかのマイナーチェ
ンジがあるこれらの体系のいずれにも対応できます。


.. First, you can define multiple engines in your config file like
.. this:

まず最初に、設定ファイルに複数のエンジンをこのように定義することができ
ます:


.. code-block:: ini

    sqlalchemy.default.url = "mysql://..." 
    sqlalchemy.default.pool_recycle = 3600 
    sqlalchemy.log.url = "sqlite://..." 

.. This defines two engines, "default" and "log", each with its own
.. set of options. Now you have to instantiate every engine you want
.. to use.

これは 2 つのエンジン "default" および "log" を、それぞれに固有のオプショ
ンで定義しています。 次に、使用するすべてのエンジンをインスタンス化しな
ければなりません。


.. code-block:: python

    default_engine = engine_from_config(config, 'sqlalchemy.default.') 
    log_engine = engine_from_config(config, 'sqlalchemy.log.') 
    init_model(default_engine, log_engine) 


.. Of course you'll have to modify `init_model()` to accept both
.. arguments and create two engines.

もちろん、 `init_model()` が両方の引数を受け取って 2 つのエンジンを作成
するように変更しなければならないでしょう。


.. To bind different tables to different databases, but always with a
.. particular table going to the same engine, use the `binds` argument
.. to `sessionmaker` rather than `bind`:

異なるテーブルを異なるデータベースに bind するが、いつも特定のテーブル
が同じエンジンに bind されるようにするには、 `sessionmaker` の引数とし
て `bind` ではなく `binds` を使用してください。


.. code-block:: python

    binds = {"table1": engine1, "table2": engine2} 
    Session = scoped_session(sessionmaker(binds=binds))


.. To choose the bindings on a per-request basis, skip the
.. sessionmaker bind(s) argument, and instead put this in your base
.. controller's `\_\_call\_\_` method before the superclass call, or
.. directly in a specific action method:

リクエスト毎に binding を選択するなら、 sessionmaker の bind(s) 引数を
省略して、代わりにベースコントローラの `__call__` メソッドのスーパーク
ラス呼び出しの前か、特定のアクションメソッドで、直接これを実行してくだ
さい:


.. code-block:: python

    meta.Session.configure(bind=meta.engine) 


.. `binds=` works the same way here too. 

`binds=` はここでも同じように働いています。


.. Discussion on coding style, the Session object, and bound metadata

コーディングスタイル、セッションオブジェクト、 bind されたメタデータに関する議論
----------------------------------------------------------------------------------

.. All ORM operations require a `Session` and an engine. All non-ORM SQL
.. operations require an engine. (Strictly speaking, they can use a
.. connection instead, but that's beyond the scope of this tutorial.) You
.. can either pass the engine as the `bind=` argument to every SQLAlchemy
.. method that does an actual database query, or bind the engine to a
.. session or metadata. This tutorial recommends binding the session
.. because that is the most flexible, as shown in the "Multiple Engines"
.. section above.

すべての ORM 操作は `Session` とエンジンを必要とします。 すべての非
ORM SQL 操作は、エンジンを必要とします。 (厳密に言うと、それらは代わり
にコネクションを使用できますが、それはこのチュートリアルの範囲を超えて
います。) 実際のデータベースクエリを行うあらゆる SQLAlchemy メソッドに
対して`bind=` 引数でエンジンを渡すか、またはセッションまたはメタデータ
にエンジンを bind することができます。このチュートリアルは、それが最も
柔軟性があるので、上の "Multiple Engines" セクションで示されるように、
セッションを bind することを勧めます。


.. It's also possible to bind a metadata to an engine using the
.. `MetaData(engine)` syntax, or to change its binding with
.. `metadata.bind = engine`. This would allow you to do autoloading
.. without the `autoload_with` argument, and certain SQL operations
.. without specifying an engine or session. Bound metadata was common
.. in earlier versions of SQLAlchemy but is no longer recommended for
.. beginners because it can cause unexpected behavior when ORM and
.. non-ORM operations are mixed.

`MetaData(engine)` 構文を使用することで、メタデータをエンジンに bind し
たり、 `metadata.bind = engine` で binding を変えることも可能です。これ
は `autoload_with` 引数なしにオートロードをできるようにします。そして、
エンジンまたはセッションを指定することなく特定の SQL 操作を実行できるよ
うにします。 bind されたメタデータは SQLAlchemy の以前のバージョンでは
一般的でしたが、 ORM 操作と非 ORM 操作が混在しているときに予期しない振
舞いを引き起こす場合があるので、初心者にはもはや推奨されません。


.. Don't confuse SQLAlchemy sessions and Pylons sessions; they're two
.. different things! The `session` object used in controllers
.. (`pylons.session`) is an industry standard used in web applications
.. to maintain state between web requests by the same
.. user. SQLAlchemy's session is an object that synchronizes ORM
.. objects in memory with their corresponding records in the database.

SQLAlchemy のセッションと Pylons のセッションを混同しないでください。
それら2つは別物です! コントローラで使用される `session` オブジェクト
(`pylons.session`) は、ウェブアプリケーションで使用される業界標準で、同
じユーザによるウェブリクエストの間の状態を維持します。 SQLAlchemy のセッ
ションは、メモリ上の ORM オブジェクトとそれが対応するデータベースのレコー
ドを同期させるオブジェクトです。


.. The `Session` variable in this chapter is _not_ a SQLAlchemy
.. session object; it's a "contextual session" class. Calling it
.. returns the (new or existing) session object appropriate for this
.. web request, taking into account threading and middleware
.. issues. Calling its class methods (`Session.commit()`,
.. `Session.query(...)`, etc) implicitly calls the corresponding
.. method on the appropriate session. You can normally just call the
.. `Session` class methods and ignore the internal session objects
.. entirely. See "Contextual/Thread-local Sessions" in the SQLAlchemy
.. manual for more information. This is equivalent to SQLAlchemy 0.3's
.. `SessionContext` but with a different API.

本章の `Session` 変数は SQLAlchemy のセッションオブジェクトでは
*ありません* 。 それは "contextual session" クラスです。 それを呼ぶと、
スレッドとミドルウェア問題を考慮してこのウェブリクエストに適切な (新し
いまたは既存の) セッションオブジェクトを返します。そのクラスメソッド
(`Session.commit()` 、 `Session.query(…)` など) を呼ぶと、対応するメソッ
ドが適切なセッションを使用して暗黙的に呼ばれます。通常は `Session` クラ
スメソッドだけを呼んで、内部のセッションオブジェクトを完全に無視できま
す。 詳しい情報に関して SQLAlchemy マニュアルの
"Contextual/Thread-local Sessions" を見てください。これは SQLAlchemy
0.3 の `SessionContext` と同等のものですが、 API が異なっています。


.. "Transactional" sessions are a new feature in SQLAlchemy 0.4; this
.. is why we're using `Session.commit()` instead of
.. `Session.flush()`. The `autocommit=False` (`transactional=True` in
.. SQLALchemy 0.4) and `autoflush=True` args (which are the defaults)
.. to `sessionmaker` enable this, and should normally be used
.. together.

「トランザクション」セッションは SQLAlchemy 0.4 の新機能です。 これは私
たちが `Session.flush()` の代わりに `Session.commit()` を使用している理
由です。 `sessionmaker` に対する `autocommit=False` (SQLALchemy 0.4 で
は `transactional=True`) と `autoflush=True` 引数 (これはデフォルトです)
はこれを可能にして、通常それらは一緒に使用されるはずです。


Fancy classes
-------------

.. Here's an ORM class with some extra features: 

これは、いくつかの追加機能を持つ ORM クラスです:


.. code-block:: python

    class Person(object): 

        def __init__(self, firstname, lastname, sex): 
            if not firstname:
                raise ValueError("arg 'firstname' cannot be blank") 
            if not lastname:
                raise ValueError("arg 'lastname' cannot be blank") 
            if sex not in ["M", "F"]:
                raise ValueError("sex must be 'M' or 'F'") 
            self.firstname = firstname 
            self.lastname = lastname 
            self.sex = sex 

        def __repr__(self): 
            myclass = self.__class__.__name__ 
            return "<%s %s %s>" % (myclass, self.firstname, self.lastname) 
            #return "%s(%r, %r)" % (myclass, self.firstname, self.lastname, self.sex) 
            #return "<%s %s>" % (self.firstname, self.lastname) 

        @property 
        def name(self): 
            return "%s %s" % (self.firstname, self.lastname) 

        @classmethod 
        def all(cls, order=None, sex=None): 
            """Return a Query of all Persons. The caller can iterate this,
            do q.count(), add additional conditions, etc. 
            """ 
            q = meta.Session.query(Person) 
            if order and order.lower().startswith("d"): 
                q = q.order_by([Person.birthdate.desc()]) 
            else: 
                q = q.order_by([Person.lastname, Person.firstname]) 
            return q 

        @classmethod 
        def recent(self, cutoff_days=30): 
            cutoff = datetime.date.today() - datetime.timedelta(days=cutoff_days) 
            q = meta.Session.query(Person).order_by(
                    [Person.last_transaction_date.desc()]) 
            q = q.filter(Person.last_transaction_date >= cutoff) 
            return q 


.. With this class you can create new records with constructor
.. args. This is not only convenient but ensures the record starts off
.. with valid data (no required field empty). `.\_\_init\_\_` is not
.. called when loading an existing record from the database, so it
.. doesn't interfere with that. Instances can print themselves in a
.. friendly way, and a read-only property is calculated from multiple
.. fields.

このクラスを使うと、コンストラクタ引数と共に新しいレコードを作成できま
す。 これは、便利であるだけでなく、レコードが有効なデータによって始めら
れることを確実にします (空の required フィールドがありません)。データベー
スから既存のレコードをロードするときは `. __init__` が呼ばれないので、
それは干渉しません。インスタンスは読みやすく表示されます。そして、書き
込み禁止のプロパティが複数のフィールドから計算されます。


.. Class methods return high-level queries for the controllers. If you
.. don't like the class methods you can have a separate `PersonSearch`
.. class for them. The methods get the session from the
.. `myapp.model.meta` module where we've stored it. Note that this
.. module imported the `meta` module, not the `Session` object
.. directly. That's because `init_model()` replaces the `Session`
.. object, so if we'd imported the `Session` object directly we'd get
.. its original value rather than its current value.

クラスメソッドはコントローラに、高レベルのクエリを返します。 クラスメソッ
ドが好きでないなら、そのための別々の `PersonSearch` クラスを作ることが
できます。 そのメソッドはそれを保存した `myapp.model.meta` モジュールか
らセッションを得ます。 このモジュールが直接 `Session` オブジェクトをイ
ンポートせずに`meta` モジュールをインポートしたことに注意してください。
`init_model()` が `Session` オブジェクトを置き換えるので、直接
`Session` オブジェクトをインポートすると現在の値ではなく元の値を得るた
めです。


.. You can do many more things in SQLAlchemy, such as a read-write
.. property on a hidden column, or specify relations or default
.. ordering in the `orm.mapper` call. You can make a composite
.. property like `person.location.latitude` and
.. `person.location.longitude` where `latitude` and `longitude` come
.. from different table columns. You can have a class that mimics a
.. list or dict but is associated with a certain table. Some of these
.. properties you'll make with Pylons normal property mechanism;
.. others you'll do with the `property` argument to `orm.mapper`. And
.. you can have relations up the gazoo, which can be lazily loaded if
.. you don't use one side of the relation much of the time, or eagerly
.. loaded to minimize the number of queries. (Only the latter use SQL
.. joins.) You can have certain columns in your class lazily loaded
.. too, although SQLAlchemy calls this "deferred" rather than
.. "lazy". SQLAlchemy will automatically load the columns or related
.. table when they're accessed.

あなたは、隠れたカラムの読み書き可能プロパティや `orm.mapper` 呼び出し
にデフォルトの並び順を指定することなど、 SQLAlchemy のずっと多くのこと
をすることができます。 `latitude` と `longitude` が異なるテーブルカラム
から来る `person.location.latitude` と `person.location.longitude` のよ
うな合成プロパティを作ることができます。リストや辞書に見えるが、あるテー
ブルに関連しているクラスを作ることができます。これらのプロパティのいく
つかは Pylons の通常のプロパティのメカニズムで作ることができます。その
他は `orm.mapper` の `property` 引数で実現できます。そして gazoo との関
連を lazy に読み込むか (gazoo を関連の one side にあまり使用しないなら)、
または eager に読み込む (クエリの数を最小にするために) ことができます。
(後者だけがSQL join を使用します) クラスの中のあるカラムを lazy に読み
込ませることができます。ただし SQLAlchemy では、これを "lazy" ではなく
"deferred" と呼んでいます。カラムまたは関連するテーブルがアクセスされた
とき、SQLAlchemy は自動的にそれらを読み込むでしょう。


.. If you have any more clever ideas for fancy classes, please add a
.. comment to this article.

fancy classes に対してより巧妙なアイデアがあれば、この記事にコメントを
追加してください。


.. Logging

ログ出力
--------

.. SQLAlchemy has several loggers that chat about the various aspects
.. of its operation. To log all SQL statements executed along with
.. their parameter values, put the following in
.. :file:`development.ini`:

SQLAlchemy は、操作の様々な側面について chat するいくつかのロガーを持っ
ています。実行されたすべての SQL 文をそのパラメタ値と共にログに記録する
には、 :file:`development.ini` に以下を入れてください:


.. code-block:: ini

    [logger_sqlalchemy] 
    level = INFO
    handlers = 
    qualname = sqlalchemy.engine 

.. Then modify the "[loggers]" section to enable your new logger:

次に、新しいロガーを有効にするように "[logger]" セクションを変更します:


.. code-block:: ini

    [loggers] 
    keys = root, myapp, sqlalchemy 


.. To log the results along with the SQL statements, set the level to
.. DEBUG. This can cause a lot of output! To stop logging the SQL, set
.. the level to WARN or ERROR.

SQL 文の結果をログに記録するには、レベルを DEBUG に設定してください。
これは大量の出力を引き起こす場合があります! SQL を登録するのを止めるに
は、レベルを WARN か ERROR に設定してください。


.. SQLAlchemy has several other loggers you can configure in the same
.. way. "sqlalchemy.pool" level INFO tells when connections are
.. checked out from the engine's connection pool and when they're
.. returned. "sqlalchemy.orm" and buddies log various ORM
.. operations. See "Configuring Logging" in the SQLAlchemy manual.

SQLAlchemy には、同様の方法で構成できる他のロガーがいくつかあります。
"sqlalchemy.pool" レベル INFO は、コネクションがエンジンのコネクション
プールからいつ調べられるか、そして、それらがいつ返されるかを伝えます。
"sqlalchemy.orm" と buddies は様々な ORM 操作を記録します。 SQLAlchemy
マニュアルの "Configuring Logging" を見てください。


.. Multiple application instances

複数のアプリケーションインスタンス
----------------------------------

.. If you're running multiple instances of the _same_ Pylons
.. application in the same WSGI process (e.g., with Paste HTTPServer's
.. "composite" application), you may run into concurrency issues. The
.. problem is that :class:`Session` is thread local but not
.. application-instance local. We're not sure how much this is really
.. an issue if ``Session.remove()`` is properly called in the base
.. controller, but just in case it becomes an issue, here are possible
.. remedies:

*同じ* Pylons アプリケーションの複数のインスタンスを同じ WSGI プロセス
で (例えば、 Paste HTTPServerの "composite" アプリケーションで) 実行し
ているなら、並行性問題に出くわすでしょう。この問題は、
:class:`Session` はスレッドローカルであってアプリケーションインスタンス
ローカルではないということです。ベースコントローラの中で
``Session.remove()`` が適切に呼ばれるなら、これが実際にはどれほど問題に
なるかはっきりしませんが、もしそれが問題になる場合、可能な療法がありま
す:


.. 1) Attach the engine(s) to ``pylons.app_globals`` (aka. ``config["pylons.app_globals"]``)
..    rather than to the `meta` module. The globals object is not shared
..    between application instances.

1) `meta` モジュールの代わりに ``pylons.app_globals`` (別名
   ``config["pylons.app_globals"]``) にエンジンを取り付けます。 globals オブジェ
   クトはアプリケーションインスタンスの間で共有されません。


.. 2) Add a scoping function. This prevents the application instances
..    from sharing the same session objects. Add the following function
..    to your model, and pass it as the second argument to
..    `scoped_session`:

2) スコープ関数を加えます。 これは、アプリケーションインスタンスが同じ
   セッションオブジェクトを共有するのを防ぎます。 以下の関数をモデルに
   追加してください。そして、`scoped_session` に対する 2 番目の引数とし
   てそれを渡してください:


.. code-block:: python

    def pylons_scope(): 
        import thread 
        from pylons import config 
        return "Pylons|%s|%s" % (thread.get_ident(), config._current_obj()) 

    Session = scoped_session(sessionmaker(), pylons_scope) 


.. If you're affected by this, or think you might be, please bring it
.. up on the pylons-discuss mailing list. We need feedback from actual
.. users in this situation to verify that our advice is correct.

これによって影響を受けるか、または影響を受けると思うなら、それを
pylons-discuss メーリングリストに提起してください。ここでのアドバイスが
正しいことを検証するために、私たちはこの状況に直面している実際のユーザ
からのフィードバックを必要としています。
