.. _getting_started:

===================
Getting Started
===================

.. This section is intended to get Pylons up and running as fast as
.. possible and provide a quick overview of the project. Links are
.. provided throughout to encourage exploration of the various aspects
.. of Pylons.

このセクションでは、できるだけ早く Pylons を始められるようになることと、
そのプロジェクトの quick overview を提供することを意図しています。
Pylons の種々な側面の探検を奨励するために、リンクが提供されます。


.. Requirements

******************
動作条件
******************

.. * Python 2.3+ (Python 2.4+ highly recommended)

* Python 2.3 以上 (Python 2.4 以上を強く推奨)


.. Installing

**************
インストール
**************

.. warning::
    
    .. These instructions require Python 2.4+. For installing with
    .. Python 2.3, see :ref:`python23_installation`.

    以下の instruction は Python 2.4 以上を必要とします。Python 2.3 と
    ともにインストールするには :ref:`python23_installation` を見てくだ
    さい。


.. To avoid conflicts with system-installed Python libraries, Pylons
.. comes with a boot-strap Python script that sets up a "virtual"
.. Python environment. Pylons will then be installed under the virtual
.. environment.

システムにインストールされた Python ライブラリとの衝突を避けるために、
Pylons には "仮想" Python 環境をセットアップするブートストラップ
Python スクリプトが付属しています。そして Pylons は仮想環境にインストー
ルされます。


.. admonition:: By the Way
    
    .. :term:`virtualenv` is a useful tool to create isolated Python
    .. environments. In addition to isolating packages from possible
    .. system conflicts, it makes it easy to install Python libraries
    .. using :term:`easy_install` without dumping lots of packages
    .. into the system-wide Python.

    :term:`virtualenv` は独立した Python 環境を作成する便利なツールです。
    潜在的なシステム衝突の可能性からパッケージを隔離することに加え、多
    くのパッケージを system-wide の Python の中にばらまくことなく、
    :term:`easy_install` を使用して Python ライブラリを簡単にインストー
    ルできるようにします。


    .. The other great benefit is that no root access is required
    .. since all modules are kept under the desired directory. This
    .. makes it easy to setup a working Pylons install on shared
    .. hosting providers and other systems where system-wide access is
    .. unavailable.

    もう一つのすばらしい利点は、すべてのモジュールを好きなディレクトリ
    の下に置くことができるので、 root アクセスは全く必要でないというこ
    とです。 これによって、共有ホスティングプロバイダーや、
    system-wide へのアクセスが入手できないその他のシステムに、動作する
    Pylons インストールをセットアップすることが簡単になります。


.. 1. Download the `go-pylons.py <http://www.pylonshq.com/download/0.9.7/go-pylons.py>`_ script.
.. 2. Run the script and specify a directory for the virtual environment to be created under:

1. `go-pylons.py <http://www.pylonshq.com/download/0.9.7/go-pylons.py>`_ スクリプトをダウンロードします。
2. スクリプトを実行して、以下のように、仮想環境を作成するためのディレクトリを指定します:

    
    .. code-block:: bash
        
        $ python go-pylons.py mydevenv


.. admonition:: Tip
    
    .. The two steps can be combined on unix systems with curl using the
    .. following short-cut:

    これら 2 つのステップは、 Unix システム上では curl を用いて以下の
    ショートカットでまとめて実行することができます:


    .. code-block:: bash
    
        $ curl http://pylonshq.com/download/0.9.7/go-pylons.py | python - mydevenv

    
    .. To isolate further from additional system-wide Python libraries, run
    .. with the --no-site-packages option:

    system-wide の追加の Python ライブラリからも分離するためには、
    \-\-no-site-packages オプションを付けて実行します。


    .. code-block:: bash
    
        $ python go-pylons.py --no-site-packages mydevenv


.. This will leave a functional virtualenv and Pylons installation.
.. Activate the virtual environment (scripts may also be run by specifying the
.. full path to the mydevenv/bin dir):

この結果、動作する virtualenv と Pylons インストールが得られます。仮想
環境を activate してください (スクリプトは、 mydevenv/dir ディレクトリ
へのフルパスを指定することによって実行することもできます):


.. code-block:: bash

    $ source mydevenv/bin/activate


.. Or on Window to activate:

Windows では、このように activate してください:


.. code-block:: text
    
    > mydevenv\Scripts\activate.bat


.. Working Directly From the Source Code 

ソースコードから直接動かす
===========================================

.. `Mercurial <http://www.selenic.com/mercurial/wiki/>`_ must be
.. installed to retrieve the latest development source for
.. Pylons. `Mercurial packages
.. <http://www.selenic.com/mercurial/wiki/index.cgi/BinaryPackages>`_
.. are also available for Windows, MacOSX, and other OS's.

Pylons の最新の開発版ソースを取得するために、 `Mercurial
<http://www.selenic.com/mercurial/wiki/>`_ をインストールしなければなり
ません。 Windows, MacOSX, および他の OS のための `Mercurial パッケージ
<http://www.selenic.com/mercurial/wiki/index.cgi/BinaryPackages>`_ も利
用可能です。


.. Check out the latest code: 

最新のコードをチェクアウトします:


.. code-block:: bash 

    $ hg clone https://www.knowledgetap.com/hg/pylons-dev Pylons 


.. To tell setuptools to use the version in the ``Pylons`` directory: 

setuptools に ``Pylons`` というディレクトリに含まれるバージョンを使用す
るように伝えるために:


.. code-block:: bash 

    $ cd Pylons 
    $ python setup.py develop 


.. The active version of Pylons is now the copy in this directory, and
.. changes made there will be reflected for Pylons apps running.

現在 Pylons のアクティブなバージョンは、このディレクトリの中のコピーで
あり、そこで行われた変更は実行される Pylons アプリケーションに反映され
るでしょう。


.. Creating a Pylons Project

*******************************
Pylons プロジェクトを作成する
*******************************

.. Create a new project named ``helloworld`` with the following command:

以下のコマンドで ``helloworld`` という名前の新しいプロジェクトを作成し
てください:


.. code-block:: bash

    $ paster create -t pylons helloworld


.. note:: 
    
    .. Windows users must configure their ``PATH`` as described in
    .. :ref:`windows_notes`, otherwise they must specify the full path
    .. to the ``paster`` command (including the virtual environment
    .. bin directory).

    Window ユーザーは、 :ref:`windows_notes` で説明されているように
    ``PATH`` を構成しなければなりません。さもなければ、 (仮想環境 bin
    ディレクトリに含まれている) ``paster`` コマンドにフルパスを指定する
    必要があります。


.. Running this will prompt for two choices:

これを実行すると、 2 つのプロンプトが表示されます:


.. 1. which templating engine to use
.. 2. whether to include :term:`SQLAlchemy` support

1. どのテンプレートエンジンを使用するか
2. :term:`SQLAlchemy` サポートを含めるか


.. Hit enter at each prompt to accept the defaults (Mako templating,
.. no :term:`SQLAlchemy`, no :term:`Google App Engine` settings).

それぞれのプロンプトについて、デフォルトを受け入れるなら Enter キーを打っ
てください (デフォルトでは Mako テンプレート、 :term:`SQLAlchemy` なしです)


.. Here is the created directory structure with links to more information:

これは作成されたディレクトリ構造と詳しい情報へのリンクです:


- helloworld
    - MANIFEST.in
    - README.txt
    - development.ini - :ref:`run-config`
    - docs
    - ez_setup.py
    - helloworld (入れ子の :ref:`helloworld ディレクトリ <helloworld_dir>` 参照)
    - helloworld.egg-info
    - setup.cfg
    - setup.py - :ref:`setup-config`
    - test.ini


.. _helloworld_dir:

.. The nested ``helloworld directory`` looks like this:

入れ子の ``helloworld ディレクトリ`` はこんな風になっています:


- helloworld
    - __init__.py
    - config
        - environment.py - :ref:`environment-config`
        - middleware.py - :ref:`middleware-config`
        - routing.py - :ref:`url-config`
    - controllers - :ref:`controllers`
    - lib
        - app_globals.py - :term:`app_globals`
        - base.py
        - helpers.py - :ref:`helpers`
    - model - :ref:`models`
    - public
    - templates - :ref:`templates`
    - tests - :ref:`testing`
    - websetup.py - :ref:`run-config`


.. Running the application

*****************************
アプリケーションを実行する
*****************************

.. Run the web application:

Web アプリケーションを起動する:


.. code-block:: bash

    $ cd helloworld
    $ paster serve --reload development.ini

    
.. The command loads the project's server configuration file in
.. :file:`development.ini` and serves the Pylons application.

このコマンドは、 :file:`development.ini` からプロジェクトのサーバ構成ファ
イルを読み込んで、 Pylons アプリケーションを起動します。


.. note::
    
    .. The ``--reload`` option ensures that the server is
    .. automatically reloaded if changes are made to Python files or
    .. the :file:`development.ini` config file. This is very useful
    .. during development. To stop the server press :command:`Ctrl+c`
    .. or the platform's equivalent.

    ``--reload`` オプションは、Python ファイルまたは
    :file:`development.ini` 構成ファイルに変更が加えられたら自動的にサー
    バがリロードされるようにします。これは、開発中は非常に便利です。 サー
    バを止めるには、 :command:`Ctrl+c` あるいはプラットホームでそれに相
    当するキーを押してください


.. Visiting http://127.0.0.1:5000/ when the server is running will
.. show the welcome page.

サーバが稼働しているときに http://127.0.0.1:5000/ を訪問すると、ウェル
カムページが表示されるでしょう。


***********
Hello World
***********

.. To create the basic hello world application, first create a
.. :term:`controller` in the project to handle requests:

基本的な hello world アプリケーションを作成するには、リクエストを扱うた
めの :term:`controller` をプロジェクトに作成します。


.. code-block:: bash

    $ paster controller hello


.. Open the :file:`helloworld/controllers/hello.py` module that was created.
.. The default controller will return just the string 'Hello World':

作成された :file:`helloworld/controllers/hello.py` モジュールを開いてく
ださい。デフォルトコントローラは単に 'Hello World' 文字列を返すようになっ
ています。


.. code-block:: python

    import logging

    from pylons import request, response, session, tmpl_context as c
    from pylons.controllers.util import abort, redirect_to

    from helloworld.lib.base import BaseController, render

    log = logging.getLogger(__name__)
    
    class HelloController(BaseController):

        def index(self):
            # Return a rendered template
            #return render('/hello.mako')
            # or, Return a response
            return 'Hello World'


.. At the top of the module, some commonly used objects are imported
.. automatically.

モジュールの先頭で、コントローラで共通に使用されるいくつかのオブジェク
トが自動的にインポートされています。


.. Navigate to http://127.0.0.1:5000/hello/index where there should be
.. a short text string saying "Hello World" (start up the app if
.. needed):

http://127.0.0.1:5000/hello/index を開いてください。そこには "Hello
World" という短いテキスト文字列があるはずです。(必要ならアプリケーショ
ンを立ち上げます):


.. image:: _static/helloworld.png

.. admonition:: Tip
    
    .. :ref:`url-config` explains how URL's get mapped to controllers
    .. and their methods.

    :ref:`url-config` では URL がどのようにコントローラとそのメソッドに
    マッピングされるかが説明されています。


.. Add a template to render some of the information that's in the
.. :term:`environ`.

:term:`environ` の中にある情報のいくつかをレンダリングするためのテンプ
レートを加えます。


.. First, create a :file:`hello.mako` file in the :file:`templates`
.. directory with the following contents:

まず最初に、 :file:`templates` ディレクトリに :file:`hello.mako` を以下
の内容で作成してください:


.. code-block:: mako

    Hello World, the environ variable looks like: <br />
    
    ${request.environ}


.. The :term:`request` variable in templates is used to get
.. information about the current request. :ref:`Template globals
.. <template-globals>` lists all the variables Pylons makes available
.. for use in templates.

テンプレートの中の :term:`request` 変数は、現在のリクエストの情報を得る
ために使用されます。 Pylons においてテンプレートの中で使えるすべての変
数は、 `template グローバル変数 <template-globals>` にリストされています。


.. Next, update the :file:`controllers/hello.py` module so that the
.. index method is as follows:

次に、 :file:`controllers/hello.py` モジュールを更新して index メソッド
を以下の通りにしてください:


.. code-block:: python

    class HelloController(BaseController):

        def index(self):
            return render('/hello.mako')


.. Refreshing the page in the browser will now look similar to this:

ブラウザでページをリフレッシュすると、今度はこのように見えるでしょう:


.. image:: _static/hellotemplate.png
