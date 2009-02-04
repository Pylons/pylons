.. _upgrading:

==============
アップグレード
==============

.. Upgrading your project is slightly different depending on which
.. versions you're upgrading from and to. It's recommended that
.. upgrades be done in minor revision steps, as deprecation warnings
.. are added between revisions to help in the upgrade process.

プロジェクトのアップグレードは、どのバージョンからどのバージョンへアッ
プグレードしようとしているかに応じて、方法がやや異なります。アップグレー
ドは、マイナーリビジョン間で行うことをお勧めします。なぜなら、リビジョ
ン間でアップグレードの過程で役に立つ deprecation warnings が加えられる
からです


.. For example, if you're running 0.9.4, first upgrade to 0.9.5, then
.. 0.9.6, then finally 0.9.7 when desired. The change to 0.9.7 can be
.. done in two steps unlike the older upgrades which should follow the
.. process documented here after the 0.9.7 upgrade.

例えば、もし 0.9.4 を動かしているなら、最初に 0.9.5 にアップグレードし
て、次に 0.9.6 に、最後に 0.9.7 に任意のタイミングでアップグレードしま
す。 0.9.7 への変更は、過去のアップグレードとは異なり 2 ステップで行う
ことができます。過去のアップグレードについては、このページの 0.9.7 アッ
プグレードの後に書かれているプロセスに従う必要があります。


.. Upgrading from 0.9.6 -> 0.9.7

0.9.6 -> 0.9.7 へのアップグレード
=================================

.. Pylons 0.9.7 changes several implicit behaviors of 0.9.6, as well
.. as toggling some new options of Routes, and using automatic HTML
.. escaping in Mako. These changes can be done in waves, and do not
.. need to be completed all at once for a 0.9.6 project to run under
.. 0.9.7.

Pylons 0.9.7 は 0.9.6 におけるいくつかの暗黙的な振る舞いを変更します。
それと同時に、 Routes の新しいオプションが切り替えられ、 Mako の自動的
な HTML エスケープが有効になっています。これらの変更は順番に行っていく
ことができ、 0.9.6 プロジェクトを 0.9.7 で動かすためにすべてを一度に終
わらせる必要はありません。


.. Minimal Steps to run a 0.9.6 project under 0.9.7

0.9.6 プロジェクトを 0.9.7 で動かす最短の方法
------------------------------------------------

.. Add the following lines to ``config/middleware.py``:

以下の行を ``config/middleware.py`` に追加してください:


.. code-block:: python
    
    # Add these imports to the top
    from beaker.middleware import CacheMiddleware, SessionMiddleware
    from routes.middleware import RoutesMiddleware
    
    # Add these below the 'CUSTOM MIDDLEWARE HERE' line, or if you removed
    # that, add them immediately after the PylonsApp initialization
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)


.. The Rails helpers from WebHelpers are no longer automatically
.. imported in the webhelpers package. To use them 'lib/helpers.py'
.. should be changed to import them:

WebHelpers の Rails helpers は webhelpers パッケージに自動的にインポー
トされなくなりました。それらを使用するためには、 'lib/helpers.py' でそ
れらをインポートするように変えてください:


.. code-block:: python

    from webhelpers.rails import *


.. Your Pylons 0.9.6 project should now run without issue in Pylons
.. 0.9.7. Note that some deprecation warnings will likely be thrown
.. reminding you to upgrade other parts.

これで、あなたの Pylons 0.9.6 プロジェクトは Pylons 0.9.7 で問題なく実
行できるはずです。おそらく、他の部分をアップグレードする必要があること
を知らせるために、いくつかの deprecation warning が投げられることに注意
してください。


.. Moving to use the new features of 0.9.7

0.9.7 の新機能を使うための変更
---------------------------------------

.. To use the complete set of new features in 0.9.7, such as the
.. automatic HTML escaping, new webhelpers, and new error middleware,
.. follow the `What's new in Pylons 0.9.7 overview
.. <http://wiki.pylonshq.com/pages/viewpage.action?pageId=11174779>`_
.. to determine how to change the other files in your project to use
.. the new features.

自動 HTML エスケープ、新しい webhelpers 、新しいエラーミドルウェアのよ
うな、 0.9.7 の新機能のすべてを使用するためには、 `What's new in
Pylons 0.9.7 overview
<http://wiki.pylonshq.com/pages/viewpage.action?pageId=11174779>`_ に従っ
て、新機能を使うためにあなたのプロジェクトで他のファイルをどのように変
更するか判断してください。


.. Moving from a pre-0.9.6 to 0.9.6

0.9.6 以前から 0.9.6 へのアップグレード
=======================================

.. Pylons projects should be updated using the paster command
.. create. In addition to creating new projects, paster create when
.. run over an existing project will provide several ways to update
.. the project template to the latest version.

Pylons のプロジェクトは paster create コマンドを用いて更新できます。
paster create は、新しいプロジェクトを作成するだけでなく、既存のプロジェ
クトに対して実行することで、プロジェクトテンプレートを最新のバージョン
に更新する幾つかの方法を提供します。


.. Using this tool properly can make upgrading a fairly minor
.. task. For the purpose of this document, the project being upgraded
.. will be called 'demoapp' and all commands will use that name.

この機能を適切に用いると、更新作業をとても小さなタスクとして片づけるこ
とができます。本文書では説明のため、更新対象のプロジェクトを 'demoapp'
と呼び、すべてのコマンドにおいてこの名前を利用します。


.. Running ``paster create`` to upgrade 

更新のために paster create を実行する
-------------------------------------

.. First, navigate to the directory *above* the project's main
.. directory.  The main directory is the one that contains the
.. ``setup.py``, ``setup.cfg``, and ``development.ini`` files.

まずはじめに、プロジェクトのメインディレクトリの *1 つ上の* ディレクト
リに移動してください。メインディレクトリとは、 ``setup.py`` や
``setup.cfg``, ``development.ini`` といったファイルを含んでいるディレク
トリのことです。


.. code-block:: bash 

    /home/joe/demoapp $ cd .. 
    /home/joe $ 


.. Then run paster create on the project directory: 

次に、プロジェクトディレクトリに対して paster create を実行して下さい。


.. code-block:: bash 

    /home/joe $ paster create demoapp -t pylons 


.. paster will issue prompts to allow the handling conflicts and updates
.. to the existing project files. The options available are (hit the key
.. in the parens to perform the operation):

paster は、既存のプロジェクトファイルに対する衝突と更新をどのように処理
するかを尋ねます。オプションは以下の通りです (操作を実行するには丸括弧
の中のキーを入力してください):


    .. (d)iff them, and show the changes between the project files and
    .. the ones that have changed in Pylons

    (d) diff を実行し、あなたのプロジェクトのファイルと Pylons で変更の
    あったファイルの違いを表示します。

 
    .. (b)ackup the file and copy the new version into its place. The
    .. backup file that is created will have a ``.bak`` extension.

    (b) ファイルをバックアップし、新しいバージョンを適切な場所にコピー
    します。古いファイルは ``.bak`` という拡張子で保存されます。


    .. (y)es to overwrite the existing file with the new one. This
    .. approach is generally not recommended as it does not allow the
    .. developer to view the content of the file that will be replaced
    .. and it offers no opportunity for later recovery of the content.
    .. The option can be made less intrepid by first viewing the diff
    .. to ascertain if any changes will be lost in the overwriting.

    (y) 新しいファイルで既存のファイルを上書きします (yes to
    overwrite) 。この方法は一般に推奨されません。置換されるファイルの中
    身を確認することができず、後で内容を回復する機会がまったくなくなっ
    てしまうためです。最初に diff を見て、上書きによってどんな変更が失
    われるかを確かめることで、このオプションの危険性を減らすことができ
    ます。


    .. (n)o to overwrite, retain the existing file. Safe if nothing
    .. has changed.

    (n) 上書きしないで、既存のファイルを維持します (no to overwite) 。
    これは、何も変更がない場合に安全です。


.. It's recommended when upgrading your project that you always look
.. at the diff first to see what has changed. Then either overwrite
.. your existing one if you are not going to lose changes you want, or
.. backup yours and write the new one in.  You can then manually
.. compare and add your changes back in.

プロジェクトをアップグレードする際には、何が変更されたかを知るためにま
ず diff で確認することをお勧めします。それから、必要な変更が失わわれる
ことがない場合には既存のファイルを上書きし、そうでなければ既存のファイ
ルをバックアップして新しいファイルを書き込んでください。そうすることで、
手動で変更点を比較し、あなたの加えた変更点を元に戻すことができます。
