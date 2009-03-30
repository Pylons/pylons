.. _views:

=======
ビュー
=======

.. image:: _static/pylon4.jpg
   :alt: 
   :align: left
   :height: 434px
   :width: 368px


.. In the MVC paradigm the *view* manages the presentation of the
.. model.

MVC パラダイムでは、 *ビュー* はモデルのプレゼンテーションを管理します。


.. The view is the interface the user sees and interacts with. For Web
.. applications, this has historically been an HTML interface. HTML
.. remains the dominant interface for Web apps but new view options
.. are rapidly appearing.

ビューはユーザが見て、対話するインタフェースです。 ウェブアプリケーショ
ンにおいて、これは歴史的に HTML インタフェースです。 HTML は依然として
ウェブアプリケーションのための代表的なインタフェースですが、新しいビュー
オプションが急速に現れています。


.. These include Macromedia Flash, JSON and views expressed in
.. alternate markup languages like XHTML, XML/XSL, WML, and Web
.. services. It is becoming increasingly common for web apps to
.. provide specialised views in the form of a REST API that allows
.. programmatic read/write access to the data model.

それには Macromedia Flash や JSON 、それに XHTML, XML/XSL, WML, ウェブ
サービスのような代替のマークアップ言語で表現されたビューがあります。ウェ
ブアプリケーションが REST API の形式で特別なビューを提供して、プログラ
ムにデータモデルを読み書きできるようにすることはますます一般的になって
います。


.. More complex APIs are quite readily implemented via SOAP services,
.. yet another type of view on to the data model.

より複雑な API は、データモデルに対するさらに異なる種類のビューである
SOAP サービスを経由して全く容易に実装されます。


.. The growing adoption of RDF, the graph-based representation scheme
.. that underpins the Semantic Web, brings a perspective that is
.. strongly weighted towards machine-readability.

RDF (セマンティックウェブを支援するグラフベースの表現スキーム) の採用が
増えていることは、機械可読性に関して強い重み付けがなされるという展望を
もたらします。

.. NOTE: As much as I love RDF I think the following paragraph is too
.. verbose for our intro docs, maybe we can put this elsewhere
.. -pjenvey

.. RDF model data is serialized into an undecorated, standardized
.. format that can readily be processed and rendered by client
.. applications of increasing sophistication, such as the MIT
.. `Simile`__ project's "`Fresnel`__", "`Longwell`__" and "`Welkin`__"
.. browser extensions.

.. RDF モデルデータは、飾りのない、標準化された形式にシリアライズされま
.. す。そのため、より洗練されたクライアントアプリケーション (たとえば
.. MIT `Simile`__ プロジェクトの "`Fresnel`__", "`Longwell`__",
.. "`Welkin`__" ブラウザ拡張など) で容易に処理およびレンダリングできま
.. す。

.. .. __: http://simile.mit.edu/
.. .. __: http://simile.mit.edu/fresnel/
.. .. __: http://simile.mit.edu/longwell/
.. .. __: http://simile.mit.edu/welkin/


.. Handling all of these interfaces in an application is becoming
.. increasingly challenging. One big advantage of MVC is that it makes
.. it easier to create these interfaces and develop a web app that
.. supports many different views and thereby provides a broad range of
.. services.

アプリケーションでこれらのインタフェースのすべてを扱うのはますます困難
になっています。 MVC の大きな利点の 1 つは、これらのインタフェースを作
成することがより簡単になり、多くの異なったビューをサポートして、それに
よって広範囲なサービスを提供するウェブアプリの開発がより簡単になること
です。


.. Typically, no significant processing occurs in the view; it serves
.. only as a means of outputting data and allowing the user (or the
.. application) to act on that data, irrespective of whether it is an
.. online store or an employee list.

通常、ビューではどんな重要な処理も起こりません。 それは単にデータを出力
して、ユーザ (またはアプリケーション) がそのデータにアクセスするための
手段として機能します。このことは、オンラインストアであっても従業員リス
トであっても変わりません。


.. Templates

.. _templates:

*************
テンプレート
*************

.. Template rendering engines are a popular choice for handling the
.. task of view presentation.

テンプレートレンダリングエンジンは、ビューのプレゼンテーションに関する
タスクを扱うための一般的な選択です。


.. To return a processed template, it must be rendered and returned by
.. the controller::

処理されたテンプレートを返すために、コントローラはそれをレンダリングし
て結果を返さなければなりません:


.. code-block:: python
    
    from helloworld.lib.base import BaseController, render

    class HelloController(BaseController):
        def sample(self):
            return render('/sample.mako')


.. Using the default Mako template engine, this will cause Mako to
.. look in the :file:`helloworld/templates` directory (assuming the
.. project is called 'helloworld') for a template filed called
.. :file:`sample.mako`.

デフォルトの Mako テンプレートエンジンを使用すると、Mako は
:file:`helloworld/templates` ディレクトリから :file:`sample.mako` とい
うテンプレートファイルを検索します。(ここで、プロジェクトが
'helloworld' であると仮定します)


.. The :func:`render` function used here is actually an alias defined
.. in your projects' :file:`base.py` for Pylons'
.. :func:`~pylons.templating.render_mako` function.

ここで使用された :func:`render` 関数は、実際には Pylons の
:func:`~pylons.templating.render_mako` 関数のためにプロジェクトの
:file:`base.py` で定義された別名です。


.. Directly-supported template engines

直接サポートされるテンプレートエンジン
=======================================

.. Pylons provides pre-configured options for using the `Mako`__,
.. `Genshi`__ and `Jinja2`__ template rendering engines. They are
.. setup automatically during the creation of a new Pylons project, or
.. can be added later manually.

Pylons は `Mako`__ 、 `Genshi`__ 、 `Jinja2`__ テンプレートレンダリング
エンジンを使用するための設定済みのオプションを提供します。このオプショ
ンは、新しい Pylons プロジェクト作成の際に自動的にセットアップされます。
あるいは後で手動で加えることができます。


.. __: http://www.makotemplates.org/
.. __: http://genshi.edgewall.org/
.. __: http://jinja.pocoo.org/


.. Passing Variables to Templates

******************************
変数をテンプレートに渡す
******************************

.. To pass objects to templates, the standard Pylons method is to
.. attach them to the :term:`tmpl_context` (aliased as `c` in
.. controllers and templates, by default) object in the
.. :ref:`controllers`::

オブジェクトをテンプレートに渡すために、 Pylons 標準の方法は、それらを
:ref:`コントローラ <controllers>` の中で :term:`tmpl_context` オブジェ
クト (それはコントローラとテンプレートの中ではデフォルトで `c` という別
名にエイリアスされています) に追加することです:

.. code-block:: python

    import logging

    from pylons import request, response, session, tmpl_context as c
    from pylons.controllers.util import abort, redirect_to

    from helloworld.lib.base import BaseController, render

    log = logging.getLogger(__name__)
    
    class HelloController(BaseController):

        def index(self):
            c.name = "Fred Smith"
            return render('/sample.mako')


.. Using the variable in the template:

テンプレートで変数を使用します:


.. code-block:: html+mako
    
    Hi there ${c.name}!


.. Strict vs Attribute-Safe tmpl_context objects

厳格な vs 属性安全な tmpl_context オブジェクト
===============================================

.. The :term:`tmpl_context` object is created at the beginning of
.. every request, and by default is an instance of the
.. :class:`~pylons.util.AttribSafeContextObj` class, which is an
.. Attribute-Safe object. This means that accessing attributes on it
.. that do **not** exist will return an empty string **instead** of
.. raising an :exc:`AttributeError` error.

:term:`tmpl_context` オブジェクトはあらゆるリクエストの始めに作成されま
す。それはデフォルトで :class:`~pylons.util.AttribSafeContextObj` クラ
スのインスタンスです。このクラスは属性安全なオブジェクトです。つまり、
存在 *しない* 属性へのアクセスは :exc:`AttributeError` エラーを投げる
*代わりに* 空文字列を返します。


.. This can be convenient for use in templates since it can act as a
.. default:

これはデフォルトとして機能するので、テンプレートで使用するには便利です。


.. code-block:: html+mako
    
    Hi there ${c.name}


.. That will work when `c.name` has not been set, and is a bit shorter
.. than what would be needed with the strict
.. :class:`~pylons.util.ContextObj` context object.

これは `c.name` が設定されていないときにも動作し、厳格な
:class:`~pylons.util.ContextObj` コンテキストオブジェクトを使用したとき
よりも少し短く書くことができます。


.. Switching to the strict version of the :term:`tmpl_context` object
.. can be done in the :file:`config/environment.py` by adding (after
.. the config.init_app)::

:term:`tmpl_context` オブジェクトの厳格なバージョンに切り替えるには、
:file:`config/environment.py` で (config.init_app の後に) 以下を追加し
ます:


.. code-block:: python
    
    config['pylons.strict_c'] = True


.. Default Template Variables

.. _template-globals:

**************************
デフォルトテンプレート変数
**************************

.. By default, all templates have a set of variables present in them
.. to make it easier to get to common objects. The full list of
.. available names present in the templates global scope:

一般的なオブジェクトに簡単にアクセスできるように、デフォルトですべての
テンプレートの中で参照できるいくつかの変数があります。テンプレートのグ
ローバルスコープに存在する利用可能な名前に関する完全リストは以下の通り
です:


.. - :term:`c` -- Template context object (Alias for :term:`tmpl_context`)
.. - :term:`tmpl_context` -- Template context object
.. - :data:`config` -- Pylons :class:`~pylons.configuration.PylonsConfig`
..   object (acts as a dict)
.. - :term:`g` -- Project application globals object (Alias for
..   :term:`app_globals`)
.. - :term:`app_globals` -- Project application globals object
.. - :term:`h` -- Project helpers module reference
.. - :data:`request` -- Pylons :class:`~pylons.controllers.util.Request`
..   object for this request
.. - :data:`response` -- Pylons :class:`~pylons.controllers.util.Response`
..   object for this request
.. - :class:`session` -- Pylons session object (unless Sessions are
..   removed)
.. - :class:`translator` -- Gettext translator object configured for
..   current locale
.. - :func:`ungettext` -- Unicode capable version of gettext's ngettext
..   function (handles plural translations)
.. - :func:`_` -- Unicode capable gettext translate function
.. - :func:`N_` -- gettext no-op function to mark a string for
..   translation, but doesn't actually translate

- :term:`c` -- テンプレートコンテキストオブジェクト
  (:term:`tmpl_context` のエイリアス)
- :term:`tmpl_context` -- テンプレートコンテキストオブジェクト
- :data:`config` -- Pylons の :class:`~pylons.configuration.PylonsConfig`
  オブジェクト (辞書のように振る舞う)
- :term:`g` -- プロジェクトのアプリケーショングローバル変数
  (:term:`app_globals` のエイリアス)
- :term:`app_globals` -- プロジェクトのアプリケーショングローバル変数
- :term:`h` -- プロジェクトの helpers モジュールへの参照
- :data:`request` -- 現在のリクエストに対する Pylons の
  :class:`~pylons.controllers.util.Request` オブジェクト
- :data:`response` -- 現在のリクエストに対する Pylons の
  :class:`~pylons.controllers.util.Response` オブジェクト
- :class:`session` -- Pylons のセッションオブジェクト (セッションが削除
  されていなければ)
- :class:`translator` -- 現在のロケールに設定された Gettext translator
  オブジェクト
- :func:`ungettext` -- Unicode 版の gettext ngettext 関数 (単数形変換を
  処理する)
- :func:`_` -- Unicode 版の gettext translate 関数
- :func:`N_` -- 文字列を翻訳対象とマークするための gettext no-op 関数。
  しかし実際には翻訳はされません。


.. Configuring Template Engines

********************************
テンプレートエンジンを設定する
********************************

.. A new Pylons project comes with the template engine setup inside
.. the projects' :file:`config/environment.py` file. This section
.. creates the Mako template lookup object and attaches it to the
.. :term:`app_globals` object, for use by the template rendering
.. function.

新しい Pylons プロジェクトは、プロジェクトの
:file:`config/environment.py` の中でテンプレートエンジンがセットアップ
された状態で開始します。このセクションでは、 Mako テンプレート検索オブ
ジェクトを作成して、それをテンプレートレンダリング関数で使用するために
:term:`app_globals` オブジェクトに取り付けます。


.. code-block:: python

    # these imports are at the top
    from mako.lookup import TemplateLookup
    from pylons.error import handle_mako_error
    
    # this section is inside the load_environment function
    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])


.. Using Multiple Template Engines

複数のテンプレートエンジンを使う
=================================

.. Since template engines are configured in the
.. :file:`config/environment.py` section, then used by render
.. functions, it's trivial to setup additional template engines, or
.. even differently configured versions of a single template
.. engine. However, custom render functions will frequently be needed
.. to utilize the additional template engine objects.

テンプレートエンジンは :file:`config/environment.py` で構成されて
render 関数によって使用されるので、追加のテンプレートエンジンや、単一の
テンプレートエンジンの異なる設定をセットアップするのも trivial です。し
かし、追加のテンプレートエンジンオブジェクトを利用するためには、カスタ
ムな render 関数がしばしば必要になるでしょう。


.. Example of additional Mako template loader for a different
.. templates directory for admins, which falls back to the normal
.. templates directory::

admin に対して別のテンプレートディレクトリを使い、通常のテンプレートディ
レクトリに fall back する追加の Mako テンプレートローダーの例:


.. code-block:: python
    
    # Add the additional path for the admin template
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')],
                 admintemplates=[os.path.join(root, 'admintemplates'),
                                 os.path.join(root, 'templates')])
    
    config['pylons.app_globals'].mako_admin_lookup = TemplateLookup(
        directories=paths['admin_templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'admintemplates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])


.. That adds the additional template lookup instance, next a
.. :ref:`custom render function <custom-render>` is needed that
.. utilizes it::

それは追加のテンプレート検索インスタンスを加えます。次にそれを利用す
る :ref:`カスタム render 関数 <custom-render>` が必要です:


.. code-block: python
    
    from pylons.templating import cached_template, pylons_globals
    
    def render_mako_admin(template_name, extra_vars=None, cache_key=None, 
                          cache_type=None, cache_expire=None):
        # Create a render callable for the cache function
        def render_template():
            # Pull in extra vars if needed
            globs = extra_vars or {}

            # Second, get the globals
            globs.update(pylons_globals())

            # Grab a template reference
            template = globs['app_globals'].mako_admin_lookup.get_template(template_name)

            return template.render(**globs)

        return cached_template(template_name, render_template, cache_key=cache_key,
                               cache_type=cache_type, cache_expire=cache_expire)


.. The only change from the :func:`~pylons.templating.render_mako`
.. function that comes with Pylons is to use the `mako_admin_lookup`
.. rather than the `mako_lookup` that is used by default.

Pylons が提供する :func:`~pylons.templating.render_mako` 関数との唯一の
違いは、 `mako_lookup` の代わりに `mako_admin_lookup` をデフォルトで使
用することです。


.. Custom :func:`render` functions

.. _custom-render:

*******************************
カスタム :func:`render` 関数
*******************************

.. Writing custom render functions can be used to access specific
.. features in a template engine, such as Genshi, that go beyond the
.. default :func:`~pylons.templating.render_genshi` functionality or
.. to add support for additional template engines.

カスタム render 関数を書くことで、 (例えば Genshi でデフォルトの
:func:`~pylons.templating.render_genshi` の機能性を越えるような) テンプ
レートエンジンの特定の特徴にアクセスしたり、テンプレートエンジンの追加
サポートを加えることができます。


.. Two helper functions for use with the render function are provided
.. to make it easier to include the common Pylons globals that are
.. useful in a template in addition to enabling easy use of cache
.. capabilities. The :func:`pylons_globals` and
.. :func:`cached_template` functions can be used if desired.

キャッシュ機能を簡単に使用できるようにするとともに、テンプレートの中で
有用な共通の Pylons グローバル変数を簡単にインクルードできるようにする、
render 関数とともに使用する 2 つのヘルパー関数が提供されています。
:func:`pylons_globals` と :func:`cached_template` 関数も使うことができ
ます。


.. Generally, the custom render function should reside in the
.. project's ``lib/`` directory, probably in :file:`base.py`.

一般に、カスタム render 関数はプロジェクトの ``lib/`` ディレクトリの中
(おそらく :file:`base.py`) に置かれます。


.. Here's a sample Genshi render function as it would look in a
.. project's ``lib/base.py`` that doesn't fully render the result to a
.. string, and rather than use :data:`c` assumes that a dict is passed
.. in to be used in the templates global namespace. It also returns a
.. Genshi stream instead the rendered string.

これはプロジェクトの ``lib/base.py`` で見られるような Genshi render 関
数のサンプルです。それは結果を文字列に完全にレンダリングせず、また
:data:`c` を使う代わりにテンプレートのグローバルな名前空間の中で使用で
きる辞書が渡されると仮定します。そして、レンダリングされた文字列の代わ
りに Genshi のストリームを返します。


.. code-block:: python
    
    from pylons.templating import pylons_globals
    
    def render(template_name, tmpl_vars):
        # First, get the globals
        globs = pylons_globals()

        # Update the passed in vars with the globals
        tmpl_vars.update(globs)
        
        # Grab a template reference
        template = globs['app_globals'].genshi_loader.load(template_name)
        
        # Render the template
        return template.generate(**tmpl_vars)


.. Using the :func:`~pylons.templating.pylons_globals` function also
.. makes it easy to get to the :term:`app_globals` object which is
.. where the template engine was attached in
.. :file:`config/environment.py`.

:func:`~pylons.templating.pylons_globals` 関数を使うと、
:file:`config/environment.py` の中でテンプレートエンジンが取り付けられ
た :term:`app_globals` オブジェクトを受け取るのが簡単になります。


    .. Prior to 0.9.7, all templating was handled through a layer
    .. called 'Buffet'. This layer frequently made customization of
    .. the template engine difficult as any customization required
    .. additional plugin modules being installed. Pylons 0.9.7 now
    .. deprecates use of the Buffet plug-in layer.

.. versionchanged:: 0.9.7
    0.9.7 より以前は、すべてのテンプレートが 'Buffet' と呼ばれる層を通
    して扱われていました。Buffet では、どんなカスタマイズも追加の
    plugin モジュールがインストールされる必要があるため、この層はしばし
    ばテンプレートエンジンのカスタマイズを難しくしました。Pylons 0.9.7
    は現在、 Buffet プラグイン層の使用を非推奨 (deprecated) としています。


.. seealso::

    .. :mod:`pylons.templating` - Pylons templating API

    :mod:`pylons.templating` - Pylons テンプレート API


.. Templating with Mako

****************************
Mako によるテンプレート処理
****************************

.. Introduction

イントロダクション
==================

.. The template library deals with the *view*, presenting the
.. model. It generates (X)HTML code, CSS and Javascript that is sent
.. to the browser. *(In the examples for this section, the project
.. root is ``myapp``.)*

テンプレートライブラリは *ビュー* を扱い、モデルを提示します。それはブ
ラウザに送られる (X)HTML コード、 CSS 、 および Javascript を生成します。
*(このセクションの例では、プロジェクトルートは ``myapp`` です)*


.. Static vs. dynamic

静的 vs 動的
------------------

.. Templates to generate dynamic web content are stored in
.. `myapp/templates`, static files are stored in `myapp/public`.

動的なウェブコンテンツを生成するテンプレートは `myapp/templates` に保存
され、静的なファイルは `myapp/public` に保存されます。


.. Both are served from the server root, **if there is a name conflict
.. the static files will be served in preference**

その両方がサーバルートから serve されます。 **名前の衝突があれば、静的
なファイルが優先的に serve されます**


.. .. Making templates unicode safe
.. 
.. テンプレートを unicode 対応にする
.. ---------------------------------
.. 
.. .. Edit :file:`config/environment.py` and add these lines just after
.. .. `tmpl_options = {}` is declared,
.. 
.. :file:`config/environment.py` を編集して、 `tmpl_options = {}` が宣言さ
.. れているすぐ後に、これらの行を加えてください。
.. 
.. 
.. .. code-block:: python
.. 
..     tmpl_options['mako.input_encoding'] = 'UTF-8'
..     tmpl_options['mako.output_encoding'] = 'UTF-8'
..     tmpl_options['mako.default_filters'] = ['decode.utf8']
.. 
.. 
.. .. then change the final `return` statement in the same file so that
.. .. it reads,
.. 
.. そして、同じファイルの最後の `return` 文をこのように変えてください。
.. 
.. 
.. .. code-block:: python
.. 
..     return pylons.config.Config(tmpl_options, map, paths,
..         request_settings = dict(charset = 'utf-8', error = 'replace'))
.. 
.. 
.. .. Also, ensure that all templates begin with the line:
.. 
.. また、すべてのテンプレートが確実にこの行で始まるようにしてください:
.. 
.. 
.. .. code-block:: html+mako
.. 
..     # -*- coding: utf-8 -*-
.. 


.. Making a template hierarchy

テンプレート階層を作る
===========================

.. Create a base template

ベーステンプレートを作る
------------------------

.. In `myapp/templates` create a file named `base.mako` and edit it to
.. appear as follows:

`myapp/templates` に `base.mako` というファイルを作成してください。そし
て、以下のように編集してください:


.. code-block:: html+mako

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
      <head>
        ${self.head_tags()}
      </head>
      <body>
        ${self.body()}
      </body>
    </html>


.. A base template such as the very basic one above can be used for
.. all pages rendered by Mako. This is useful for giving a consistent
.. look to the application.

上の非常に基本的なベーステンプレートを Mako によってレンダリングされる
すべてのページで使用することができます。これはアプリケーションに一貫し
た外観を与えるのに役立ちます。


.. * Expressions wrapped in `${...}` are evaluated by Mako and returned
..   as text
.. * `${` and `}` may span several lines but the closing brace should not
..   be on a line by itself (or Mako throws an error)
.. * Functions that are part of the `self` namespace are defined in the
..   Mako templates

* `${...}` で囲まれた式は Mako によって評価され文字列として返されます
* `${` と `}` は複数行にまたがっても構いませんが、閉じ括弧が 1 行に単独
  で存在してはいけません (さもなければ Mako はエラーを throw します)
* `self` 名前空間の一部である関数は Mako テンプレートの中で定義されます


.. Create child templates

子テンプレートを作る
----------------------

.. Create another file in `myapp/templates` called `my_action.mako`
.. and edit it to appear as follows:

`myapp/templates` に `my_action.mako` という名前の別のファイルを作成し
てください。そして、以下のように編集してください:


.. code-block:: html+mako

    <%inherit file="/base.mako" />

    <%def name="head_tags()">
      <!-- add some head tags here -->
    </%def>

    <h1>My Controller</h1>

    <p>Lorem ipsum dolor ...</p>


.. This file define the functions called by `base.mako`. 

このファイルは `base.mako` によって呼ばれる関数を定義します。


.. * The `inherit` tag specifies a parent file to pass program flow to
.. * Mako defines functions with `<%def name="function_name()">...</%def>`,
..   the contents of the tag are returned
.. * Anything left after the Mako tags are parsed out is automatically
..   put into the `body()` function

* `inherit` タグはプログラムの流れを渡すための親ファイルを指定します
* Mako は `<%def name="function_name()">...</%def>` で関数を定義します。
  タグの内容が返されます。
* Mako タグが解析された後に残ったものは自動的に `body()` 関数の中に入れ
  られます


.. A consistent feel to an application can be more readily achieved if
.. all application pages refer back to single file (in this case
.. `base.mako`).

すべてのアプリケーションページが単一のファイル (この場合 `base.mako`)
を参照するなら、アプリケーションの一貫した印象をより簡単に達成できます。


.. Check that it works

動作を確認する
-------------------

.. In the controller action, use the following as a `return()` value,

コントローラのアクションでは、 `return()` 値として以下を使用してくださ
い。


.. code-block:: python

    return render('/my_action.mako')


.. Now run the action, usually by visiting something like
.. ``http://localhost:5000/my_controller/my_action`` in a
.. browser. Selecting 'View Source' in the browser should reveal the
.. following output:

さあ、アクションを実行しましょう。通常ブラウザで
``http://localhost:5000/my_controller/my_action`` のようなページを訪問
することになります。ブラウザで `View Source` を選択すると、以下の出力が
明らかになるでしょう:


.. code-block:: html

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
      <head>
      <!-- add some head tags here -->
      </head>
      <body>

    <h1>My Controller</h1>

    <p>Lorem ipsum dolor ...</p>

      </body>
    </html>


.. seealso::

    .. The `Mako documentation <http://www.makotemplates.org/docs/>`_
    ..     Reasonably straightforward to follow

    `Mako ドキュメント <http://www.makotemplates.org/docs/>`_
        かなり分かりやすいです

    .. See the :ref:`i18n` 
    ..     Provides more help on making your application more worldly.

    :ref:`i18n`
        アプリケーションをより世界的にするための助けになります。
