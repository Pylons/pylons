.. _helpers:

=======
Helpers
=======

.. Helpers are functions intended for usage in templates, to assist
.. with common HTML and text manipulation, higher level constructs
.. like a HTML tag builder (that safely escapes variables), and
.. advanced functionality like Pagination of data sets.

helpers はテンプレートで使用することを想定した関数で、一般的な HTML と
テキスト処理、 HTML タグビルダー (それは変数を安全にエスケープする) の
ようなより高レベルの構築、およびデータセットのページングのような高度な
機能性を補助します。


.. The majority of the helpers available in Pylons are provided by the
.. :mod:`webhelpers` package. Some of these helpers are also used in
.. controllers to prepare data for use in the template by other
.. helpers, such as the :func:`~webhelpers.rails.secure_form_tag`
.. function which has a corresponding
.. :func:`~pylons.decorators.secure.authenticate_form`.

Pylons で利用可能な helpers の大部分は :mod:`webhelpers` パッケージによっ
て提供されます。また、これらの helpers のいくつかは、テンプレートの中で
他の helpers によって使われるデータを準備するため、コントローラでも使用
されます。例えば :func:`~pylons.decorators.secure.authenticate_form` に
対応する :func:`~webhelpers.rails.secure_form_tag` 関数などです。


.. To make individual helpers available for use in templates under
.. :term:`h`, the appropriate functions need to be imported in
.. :file:`lib/helpers.py`. All the functions available in this file
.. are then available under :term:`h` just like any other module
.. reference.

個々の helpers をテンプレートの中で :term:`h` の下で使えるように、適切
な関数が :file:`lib/helpers.py` でインポートされる必要があります。そう
すると、このファイルで利用可能なすべての関数が、他のモジュール参照と全
く同じように :term:`h` の下で利用可能です。


.. By customizing the :file:`lib/helpers.py` module you can quickly
.. add custom functions and classes for use in your templates.

:file:`lib/helpers.py` モジュールをカスタマイズすることで、テンプレート
で使うためのカスタム関数とクラスをすぐに加えることができます。


.. Helper functions are organized into modules by theme. All HTML
.. generators are under the ``webhelpers_html`` package, except for a
.. few third-party modules which are directly under
.. ``webhelpers``. The webhelpers modules are separately documented,
.. see :mod:`webhelpers`.

ヘルパー関数はテーマ別にモジュールに組織化されます。 ``webhelpers`` 直
下のいくつかのサードパーティー製のモジュールを除き、すべての HTML ジェ
ネレータは ``webhelpers_html`` パッケージの下にあります。 webhelpers モ
ジュールは別にドキュメント化されます。 :mod:`webhelpers` を参照してくだ
さい。


.. Pagination

.. _pagination:

ページング
==========

.. note::

    .. The `paginate` module is not compatible to the deprecated
    .. `pagination` module that was provided with former versions of
    .. the Webhelpers package.

    `paginate` モジュールは、 Webhelpers パッケージの以前のバージョンで
    提供されていた非推奨 (deprecated) の `pagination` モジュールとは互
    換性がありません。


.. Purpose of a paginator

paginator の目的
----------------------

.. When you display large amounts of data like a result from an SQL
.. query then usually you cannot display all the results on a single
.. page. It would simply be too much. So you divide the data into
.. smaller chunks. This is what a paginator does. It shows one page of
.. chunk of data at a time. Imagine you are providing a company
.. phonebook through the web and let the user search the
.. entries. Assume the search result contains 23 entries. You may
.. decide to display no more than 10 entries per page. The first page
.. contains entries 1-10, the second 11-20 and the third 21-23. And
.. you also show a navigational element like ``Page 1 of 3: [1] 2 3``
.. that allows the user to switch between the available pages.

SQL クエリの結果のような多量のデータを表示する場合、通常すべての結果を
1 ページに表示できるわけではありません。 それは単純にあまりに多いでしょ
う。 そこで、データをより小さな塊に分割します。 これは paginator が行う
ことです。 それは一度に 1 ページ分のデータの塊を表示します。例えば、
Web を通して会社の電話帳を提供していて、ユーザにエントリを検索させるこ
とを想像してください。検索結果が 23 のエントリを含むと仮定します。 あな
たは 1 ページあたり 10 未満のエントリを表示すると決めることができます。
最初のページはエントリ 1-10 、 2 番目は 11-20 、そして 3 番目は 21-23
を含んでいます。 そして、ユーザが利用可能なページを切り換えることができ
る ``Page 1 of 3: [1] 2 3`` のようなナビゲーション要素を表示します。


.. The ``Page`` class

``Page`` クラス
------------------

.. The :mod:`webhelpers` package provides a *paginate* module that can
.. be used for this purpose. It can create pages from simple Python
.. lists as well as SQLAlchemy queries and SQLAlchemy select
.. objects. The module provides a ``Page`` object that represents a
.. single page of items from a larger result set. Such a ``Page``
.. mainly behaves like a list of items on that page. Let's take the
.. above example of 23 items spread across 3 pages:

:mod:`webhelpers` パッケージはこのために使用できる *paginate* モジュー
ルを提供します。 それは簡単な Python リストに加えて SQLAlchemy のクエリ
と select オブジェクトからページを作成することができます。そのモジュー
ルは、より大きな結果セットからの 1 ページ分のアイテムを表現する
``Page`` オブジェクトを提供します。 そのような ``Page`` は主にそのペー
ジのアイテムのリストのように振る舞います。上記の、 23 アイテムが 3 ペー
ジに分割された例を挙げましょう:


.. code-block :: pycon
       
    # Create a list of items from 1 to 23
    >>> items = range(1,24)
    
    # Import the paginate module
    >>> import webhelpers.paginate
    
    # Create a Page object from the 'items' for the second page
    >>> page2 = webhelpers.paginate.Page(items, page=2, items_per_page=10)

    # The Page object can be printed (__repr__) to show details on the page
    >>> page2

        Page:
        Collection type:  <type 'list'>
        (Current) page:   2
        First item:       11
        Last item:        20
        First page:       1
        Last page:        3
        Previous page:    1
        Next page:        3
        Items per page:   10
        Number of items:  23
        Number of pages:  3

    # Show the items on this page
    >>> list(page2)
    
        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    # Print the items in a for loop
    >>> for i in page2: print "This is entry", i

        This is entry 11
        This is entry 12
        This is entry 13
        This is entry 14
        This is entry 15
        This is entry 16
        This is entry 17
        This is entry 18
        This is entry 19
        This is entry 20


.. There are further parameters to invoking a ``Page`` object. Please
.. see :class:`webhelpers.paginate.Page`

``Page`` オブジェクトを呼び出すためのさらなるパラメタがあります。
:class:`webhelpers.paginate.Page` を見てください。


.. note::

    .. Page numbers and item numbers start from 1. If you are
    .. accessing the items on the page by their index please note that
    .. the first item is ``item[1]`` instead of ``item[0]``.

    ページ番号とアイテム番号は 1 から始まります。インデックスによってペー
    ジアイテムにアクセスしているなら、最初のアイテムは ``item[0]`` では
    なく ``item[1]`` であることに注意してください。


.. Switching between pages using a `pager`

`pager` を使用してページを切り替える
---------------------------------------

.. The user needs a way to get to another page. This is usually done
.. with a list of links like ``Page 3 of 41 - 1 2 [3] 4 5
.. .. 41``. Such a list can be created by the Page's
.. :meth:`~webhelpers.paginate.Page.pager` method.  Take the above
.. example again:

ユーザは他のページに移動する方法を必要とします。 これは通常、 ``Page 3
of 41 - 1 2 [3] 4 5 .. 41`` のようなリンクのリストによって実現されます。
そのようなリストは Page の :meth:`~webhelpers.paginate.Page.pager` メソッ
ドで作成できます。 もう一度上記の例を見てください:


.. code-block:: pycon

    >>> page2.pager()
    
        <a class="pager_link" href="/content?page=1">1</a>
        <span class="pager_curpage">2</span>
        <a class="pager_link" href="/content?page=3">3</a>


.. Without the HTML tags it looks like ``1 [2] 3``. The links point to
.. a URL where the respective page is found. And the current page (2)
.. is highlighted.

HTML タグがなければ、それは ``1 [2] 3`` のように見えます。それらのリン
クは各ページが見つかる URL を指しています。そして、現在のページ (2) は
強調されています。


.. The appearance of a pager can be customized. By default the format
.. string is ``~2~`` which means it shows adjacent pages from the
.. current page with a maximal radius of 2. In a larger set this would
.. look like ``1 .. 34 35 [36] 37 38 .. 176``. The radius of 2 means
.. that two pages before and after the current page 36 are shown.

pager の見た目はカスタマイズできます。デフォルトではフォーマット文字列
は ``~2~`` で、現在のページから最大半径 2 の隣接するページを表示するこ
とを意味します。より大きなセットでは、これは ``1 .. 34 35 [36] 37 38
..  176`` のように表示されるでしょう。半径 2 は、現在のページ 36 の前後
に 2 ページが表示されることを意味します。


.. Several special variables can be used in the format string. See
.. :meth:`~webhelpers.paginate.Page.pager` for a complete list. Some
.. examples for a pager of 20 pages while being on page 10 currently:

フォーマット文字列でいくつかの特別な変数を使用できます。 全リストについ
ては :meth:`~webhelpers.paginate.Page.pager` を見てください。 20 ページ
のうち現在 10ページ目を表示している pager のいくつかの例:


.. code-block:: pycon

    >>> page.pager()
    
        1 .. 8 9 [10] 11 12 .. 20
        
    >>> page.pager('~4~')
    
        1 .. 6 7 8 9 [10] 11 12 13 14 .. 20
        
    >>> page.pager('Page $page of $page_count - ~3~')
    
        Page 10 of 20 - 1 .. 7 8 9 [10] 11 12 13 .. 20
        
    >>> page.pager('$link_previous $link_next ~2~')
    
        < > 1 .. 8 9 [10] 11 12 .. 20
        
    >>> page.pager('Items $first_item - $last_item / ~2~')
    
        Items 91 - 100 / 1 .. 8 9 [10] 11 12 .. 20


.. Paging over an SQLAlchemy query

SQLAlchemy query に対するページング
-----------------------------------

.. If the data to page over comes from a database via SQLAlchemy then
.. the ``paginate`` module can access a ``query`` object
.. directly. This is useful when using ORM-mapped models. Example:

ページのデータが SQLAlchemy を通してデータベースからやって来たものなら、
``paginate`` モジュールは直接 ``query`` オブジェクトにアクセスできます。
これは ORM にマッピングされたモデルを使用するときに便利です。 例:


.. code-block:: pycon

    >>> employee_query = Session.query(Employee)
    >>> page2 = webhelpers.paginate.Page(
            employee_query,
            page=2,
            items_per_page=10)
    >>> for employee in page2: print employee.first_name

        John
        Jack
        Joseph
        Kay
        Lars
        Lynn
        Pamela
        Sandra
        Thomas
        Tim


.. The `paginate` module is smart enough to only query the database
.. for the objects that are needed on this page. E.g. if a page
.. consists of the items 11-20 then SQLAlchemy will be asked to fetch
.. exactly that 10 rows through `LIMIT` and `OFFSET` in the actual SQL
.. query. So you must not load the complete result set into memory and
.. pass that. Instead always pass a `query` when creating a `Page`.

`paginate` モジュールは十分賢いので、このページで必要なオブジェクトだけ
をデータベースに問い合わせることができます。例えば、 1 ページがアイテム
11-20 から成る場合、 SQLAlchemy は実際の SQL クエリにおいて `LIMIT` と
`OFFSET` を通してまさにその 10 列を取得するように依頼されるでしょう。
そのため、完全な結果セットをメモリに読み込んでからそれを渡してはいけま
せん。 `Page` を作成するときには代わりにいつも `query` を渡してください。


.. Paging over an SQLAlchemy select

SQLAlchemy select に対するページング
------------------------------------

.. SQLAlchemy also allows to run arbitrary SELECTs on database tables.
.. This is useful for non-ORM queries. `paginate` can use such select
.. objects, too. Example:

また、 SQLAlchemy はデータベースのテーブルに対する任意の SELECT 文を実
行することが可能です。これは非 ORM クエリに便利です。 `paginate` はその
ような select オブジェクトも使用できます。 例:


.. code-block:: pycon

    >>> selection = sqlalchemy.select([Employee.c.first_name])
    >>> page2 = webhelpers.paginate.Page(
            selection,
            page=2,
            items_per_page=10,
            sqlalchemy_session=model.Session)
    >>> for first_name in page2: print first_name
    
        John
        Jack
        Joseph
        Kay
        Lars
        Lynn
        Pamela
        Sandra
        Thomas
        Tim


.. The only difference to using SQLAlchemy *query* objects is that you
.. need to pass an SQLAlchemy *session* via the ``sqlalchemy_session``
.. parameter.  A bare ``select`` does not have a database connection
.. assigned. But the session has.

SQLAlchemy *query* オブジェクトを使用することとの唯一の違いは、
``sqlalchemy_session`` パラメタで SQLAlchemy *session* を渡す必要がある
ということです。 素の ``select`` は割り当てられたデータベース接続を持っ
ていません。 しかし、セッションは持っています。


.. Usage in a Pylons controller and template

Pylons コントローラとテンプレートにおける使用法
-----------------------------------------------

.. A simple example to begin with.

始めるための簡単な例。


Controller:

.. code-block:: python

    def list(self):
        c.employees = webhelpers.paginate.Page(
            model.Session.query(model.Employee),
            page = int(request.params['page']),
            items_per_page = 5)
        return render('/employees/list.mako')


Template:

.. code-block:: mako

    ${c.employees.pager('Page $page: $link_previous $link_next ~4~')}
    <ul>
    % for employee in c.employees:
        <li>${employee.first_name} ${employee.last_name}</li>
    % endfor
    </ul>


.. The `pager()` creates links to the previous URL and just sets the
.. *page* parameter appropriately. That's why you need to pass the
.. requested page number (``request.params['page']``) when you create
.. a `Page`.

`pager()` は以前の URL へのリンクを作成して、単に適切に *page* パラメタ
を設定します。そんなわけで、 `Page` を作成するときにリクエストされたペー
ジ番号 (``request.params['page']``) を渡す必要があります。


.. Partial updates with AJAX

AJAX による部分アップデート
---------------------------

.. Updating a page partially is easy. All it takes is a little
.. Javascript that - instead of loading the complete page - updates
.. just the part of the page containing the paginated items. The
.. ``pager()`` method accepts an ``onclick`` parameter for that
.. purpose. This value is added as an ``onclick`` parameter to the
.. A-HREF tags. So the ``href`` parameter points to a URL that loads
.. the complete page while the ``onclick`` parameter provides
.. Javascript that loads a partial page. An example (using the jQuery
.. Javascript library for simplification) may help explain that.

ページを部分的にアップデートすることは簡単です。それに必要なのは、 (完
全なページをロードする代わりに) ページングアイテムを含むページの一部を
アップデートする小さな Javascript だけです。 ``pager()`` メソッドはその
目的のために ``onclick`` パラメタを受け付けます。その値は ``onclick``
パラメタとして A-HREF タグに追加されます。それで、 ``href`` パラメタは
完全なページをロードする URL を指す一方、 ``onclick`` パラメタが部分的
なページをロードする Javascript を提供します。例 (簡単のために jQuery
Javascript ライブラリを使用します) は、その説明の助けになるでしょう。


Controller:

.. code-block:: python

    def list(self):
        c.employees = webhelpers.paginate.Page(
            model.Session.query(model.Employee),
            page = int(request.params['page']),
            items_per_page = 5)
        if 'partial' in request.params:
            # Render the partial page
            return render('/employees/list-partial.mako')
        else:
            # Render the full page
            return render('/employees/list-full.mako')


Template ``list-full.mako``:

.. code-block:: mako

    <html>
        <head>
            ${webhelpers.html.tags.javascript_link('/public/jQuery.js')}
        </head>
        <body>
            <div id="page-area">
                <%include file="list-partial.mako"/>
            </div>
        </body>
    </html>


Template ``list-partial.mako``:

.. code-block:: mako

    ${c.employees.pager(
        'Page $page: $link_previous $link_next ~4~',
        onclick="$('#my-page-area').load('%s'); return false;")}
    <ul>
    % for employee in c.employees:
        <li>${employee.first_name} ${employee.last_name}</li>
    % endfor
    </ul>


.. To avoid code duplication in the template the full template
.. includes the partial template. If a partial page load is requested
.. then just the ``list-partial.mako`` gets rendered. And if a full
.. page load is requested then the ``list-full.mako`` is rendered
.. which in turn includes the ``list-partial.mako``.

テンプレートのコードが重複するのを避けるため、完全なテンプレートは部分
的なテンプレートを include しています。 部分的なページロードがリクエス
トされるなら、 ``list-partial.mako`` だけがレンダリングされます。 また、
全ページロードがリクエストされるなら、 ``list-partial.mako`` がレンダリ
ングされ、それが今度は ``list-full.mako`` を include します。


.. The ``%s`` variable in the ``onclick`` string gets replaced with a
.. URL pointing to the respective page with a ``partial=1`` added (the
.. name of the parameter can be customized through the
.. ``partial_param`` parameter). Example:

``onclick`` 文字列中の ``%s`` 変数は、それぞれのページを示す URL に
``partial=1`` が加えられたものと置き換えられます (パラメタの名前は
``partial_param`` パラメタを通してカスタマイズできます)。 例:


.. * ``href`` parameter points to ``/employees/list?page=3``
.. * ``onclick`` parameter contains Javascript loading
..   ``/employees/list?page=3&partial=1``

* ``href`` パラメータは ``/employees/list?page=3`` を指す
* ``onclick`` パラメータは ``/employees/list?page=3&partial=1`` をロー
  ドする Javascript を含む


.. jQuery's syntax to load a URL into a certain DOM object (e.g. a
.. DIV) is simply:

ある DOM オブジェクト (例えば、 DIV) に URL をロードする jQuery の構文
は単に以下の通りです:


.. code-block:: javascript

    $('#some-id').load('/the/url')


.. The advantage of this technique is that it degrades gracefully. If
.. the user does not have Javascript enabled then a full page is
.. loaded. And if Javascript works then a partial load is done through
.. the ``onclick`` action.

このテクニックの利点は優雅に退行 (degrade) するということです。もしユー
ザが Javascript を有効にしていなければ全ページがロードされます。そして、
Javascript が動作しているなら ``onclick`` 動作で部分ロードが行われます。


.. _secure-forms:

Secure Form Tag Helpers
=======================

.. For prevention of Cross-site request forgery (CSRF) attacks.

クロスサイトリクエストフォージェリ (CSRF) 攻撃防止のために。


.. Generates form tags that include client-specific authorization
.. tokens to be verified by the destined web app.

destined のウェブアプリによって検証されるクライアント固有の権限トークン
を含むフォームタグを生成します。


.. Authorization tokens are stored in the client's session. The web
.. app can then verify the request's submitted authorization token
.. with the value in the client's session.

権限トークンはクライアントのセッションの中に保存されます。 そして、ウェ
ブアプリはリクエストの送信された権限トークンをクライアントのセッション
の中にある値と共に検証することができます。


.. This ensures the request came from the originating page. See the
.. wikipedia entry for `Cross-site request forgery`__ for more
.. information.

.. .. __: http://en.wikipedia.org/wiki/Cross-site_request_forgery


これは、リクエストが元のページから来たことを保証します。詳しい情報に関
しては wikipedia の `クロスサイトリクエストフォージェリ`__ の項を見てく
ださい。

.. __: http://ja.wikipedia.org/wiki/%E3%82%AF%E3%83%AD%E3%82%B9%E3%82%B5%E3%82%A4%E3%83%88%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E3%83%95%E3%82%A9%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%AA


.. Pylons provides an ``authenticate_form`` decorator that does this
.. verification on the behalf of controllers.

Pylons はコントローラに代わってこの検証を行う ``authenticate_form`` デ
コレータを提供します。


.. These helpers depend on Pylons' ``session`` object.  Most of them
.. can be easily ported to another framework by changing the API
.. calls.

これらの helpers は Pylons の ``session`` オブジェクトに依存しています。
それらの大部分は、API 呼び出しを変えることによって別のフレームワークに
容易に移植できます。


.. The helpers are implemented in such a way that it should be easy
.. for developers to create their own helpers if using helpers for
.. AJAX calls.

それらの helpers は、 AJAX 呼び出しに helpers を使用するなら開発者が簡
単に自身の helpers を作成できるような方法で実装されています。
(訳注: この段落が前後の段落とどうつながるのかちょっと分からない)


.. :func:`authentication_token` returns the current authentication token,
.. creating one and storing it in the session if it doesn't already
.. exist.

:func:`authentication_token` は現在の認証トークンを返します。まだ存在し
ていないなら、認証トークンを 1 つ作成して、それをセッションの中に保存し
ます。


.. :func:`auth_token_hidden_field` creates a hidden field containing
.. the authentication token.

:func:`auth_token_hidden_field` は認証トークンを含む hidden フィールド
を作成します。


.. :func:`secure_form` is :func:`form` plus
.. :func:`auth_token_hidden_field`.

:func:`secure_form` は :func:`form` + :func:`auth_token_hidden_field`
です。
