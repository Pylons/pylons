.. Troubleshooting & Debugging

.. _debugging:

================================
トラブルシューティングとデバッグ
================================

.. Interactive debugging

.. _interactive_debugging:

インタラクティブなデバッグ
--------------------------

.. Things break, and when they do, quickly pinpointing what went wrong
.. and why makes a huge difference. By default, Pylons uses a
.. customized version of `Ian Bicking's
.. <http://blog.ianbicking.org/>`_ EvalException middleware that also
.. includes full Mako/Myghty Traceback information.

どんなものも、いずれ壊れます (Things break)。そんなとき、何がうまく行っ
ていないのか、なぜ大きな違いが生まれるのかを即座に明らかにすることは大
きな価値があります。 Pylons は、 `Ian Bicking
<http://blog.ianbicking.org/>`_ の EvalException ミドルウェアを
Mako/Myghty の完全なトレースバックの情報を含むようにカスタマイズしたも
のをデフォルトで利用しています。


.. The Debugging Screen 

デバッグ画面
-------------------- 

.. The debugging screen has three tabs at the top: 

デバッグ画面の上部には3つのタブがあります。


``Traceback`` 

    .. Provides the raw exception trace with the interactive debugger 

    生の例外トレースと、インタラクティブなデバッガを提供します。

``Extra Data`` 

    .. Displays CGI, WSGI variables at the time of the exception, in
    .. addition to configuration information

    例外発生時の CGI, WSGI 変数と設定情報を表示します。

``Template`` 

    .. Human friendly traceback for Mako or Myghty templates 

    人間が読みやすい Mako または Myghty テンプレートのトレースバックで
    す。


.. Since Mako and Myghty compile their templates to Python modules, it
.. can be difficult to accurately figure out what line of the template
.. resulted in the error. The `Template` tab provides the full Mako or
.. Myghty traceback which contains accurate line numbers for your
.. templates, and where the error originated from. If your exception
.. was triggered before a template was rendered, no Template
.. information will be available in this section.

Mako と Myghty はテンプレートを Python モジュールにコンパイルするので、
テンプレートのどの行でエラーが起きたのかを正確に見出すのは難しい場合が
あります。 `Template` タブは、 Mako や Myghty の完全なトレースバックを
提供し、テンプレート内の正確な行番号と、エラーがどこで起こっているのか
の情報を提供します。例外がテンプレートを描画する前に発生した場合には、
この項目にはテンプレートに関する情報は表示されません。


.. Example: Exploring the Traceback 

例: トレースバックを探索する
-------------------------------- 

.. Using the interactive debugger can also be useful to gain a deeper
.. insight into objects present only during the web request like the
.. ``session`` and ``request`` objects.

インタラクティブなデバッガを利用することは、 ``session`` や
``request`` といった Web リクエスト中にしか現れないオブジェクトの中身を
深く知るのにも役に立ちます。


.. To trigger an error so that we can explore what's happening just raise
.. an exception inside an action you're curious about. In this example,
.. we'll raise an error in the action that's used to display the page
.. you're reading this on. Here's what the docs controller looks like:

エラーを起こして何が起きているかを知るためには、単に興味を持っているア
クションの中で例外を raise します。この例では、今あなたが見ているページ
を表示するのに使われているアクション (訳注: この記述は原文が間違ってい
るのでは?) の中でエラーを raise します。 docs コントローラは以下のよう
なものです。


.. code-block:: python 

    class DocsController(BaseController): 
        def view(self, url): 
            if request.path_info.endswith('docs'): 
                redirect_to('/docs/') 
            return render('/docs/' + url) 


.. Since we want to explore the ``session`` and ``request``, we'll
.. need to bind them first. Here's what our action now looks like with
.. the binding and raising an exception:

``session`` や ``request`` の中身を知りたいので、最初にそれらの値を束縛
(bind) しておく必要があります。ここで、値の束縛と例外の発生でアクション
がどのようになるか見てみましょう。


.. code-block:: python 

    def view(self, url): 
        raise "hi" 
        if request.path_info.endswith('docs'): 
            redirect_to('/docs/') 
        return render('/docs/' + url) 


.. Here's what exploring the Traceback from the above example looks
.. like (Excerpt of the relevant portion):

ここに、上記の例に対応したトレースバックを探索している様子を示します
(関連部分を抜粋しています):

.. note:: 訳注:

    以下の例では、例外が発生した時点で self に束縛されていた
    ``session`` や ``request`` が表示されていることがわかります。


.. image:: _static/doctraceback.png
    :width: 750px
    :height: 260px


.. Email Options 

Email オプション
----------------

.. You can make all sorts of changes to how the debugging works. For
.. example if you disable the ``debug`` variable in the config file
.. Pylons will email you an error report instead of displaying it as
.. long as you provide your email address at the top of the config
.. file:

デバッグの動作のしかたについて、あらゆる変更を行うことができます。たと
えば設定ファイルの中で ``debug`` 変数を無効にすると、設定ファイルの先頭
でメールアドレスを設定さえしておけば、画面にエラーレポートを表示する代
わりに、 Pylons はそれをメールしてくれます。


.. code-block:: ini 

    error_email_from = you@example.com 


.. This is very useful for a production site. Emails are sent via SMTP so
.. you need to specify a valid SMTP server too.

この機能はプロダクション・サイトでとても便利です。メールは SMTP を介し
て送られるので、適切な SMTP サーバも設定しておく必要があります。


.. Error Handling Options 

エラー処理オプション
====================== 

.. A number of error handling options can be specified in the config
.. file. These are described in the :ref:`interactive_debugging`
.. documentation but the important point to remember is that debug
.. should always be set to ``false`` in production environments
.. otherwise if an error occurs the visitor will be presented with the
.. developer's interactive traceback which they could use to execute
.. malicious code.

多くのエラー処理オプションを設定ファイルで指定することができます。それ
らは :ref:`interactive_debugging` で説明されますが、覚えておくべき重要
なポイントは、プロダクション環境では debug を常に ``false`` にセットし
なければならないということです。そうしなければ、エラーが発生した場合に、
悪意のあるコードを実行するために使用できる開発者のインタラクティブ・ト
レースバックを、サイト訪問者に与えてしまうことになります。
