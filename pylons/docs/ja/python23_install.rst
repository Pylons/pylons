.. Python 2.3 Installation Instructions

.. _python23_installation:

====================================
Python 2.3 インストールガイド
====================================

.. Advice of **end of support for Python 2.3**

**Python 2.3 のサポート終了** に対するアドバイス
-------------------------------------------------

.. warning::

    .. **END OF SUPPORT FOR PYTHON 2.3** This is the **LAST** version
    .. to support Python 2.3 **BEGIN UPGRADING OR DIE**

    **Python 2.3 のサポート終了** これは Python 2.3 をサポートする **最
    後の** バージョンです。 **BEGIN UPGRADING OR DIE**


.. Preparation

準備
-----------

.. First, please note that Python 2.3 users on Windows will need to
.. install `subprocess.exe`__ before beginning the installation
.. (whereas Python 2.4 users on Windows do not). All windows users
.. also should read the section :ref:`windows_notes` after
.. installation. Users of Ubuntu/debian will also likely need to
.. install the python-dev package.

最初に、 Windows の Python 2.3 ユーザは、インストールを始める前に
`subprocess.exe`__ をインストールする必要があることに注意してください
(それに対して Windows の Python 2.4 ユーザはその必要はありません)。すべ
ての Windows ユーザは、インストールの後で :ref:`windows_notes` も読むべ
きです。また、 Ubuntu/debian ユーザは、おそらく python-dev パッケージを
インストールする必要があるでしょう。

.. __: http://www.pylonshq.com/download/subprocess-0.1-20041012.win32-py2.3.exe


.. System-wide Install

システム全体へのインストール
----------------------------

.. To install Pylons so it can be used by everyone (you'll need root
.. access).

全員が Pylons を使用できるようにインストールする (root アクセスが必要で
す)。


.. If you already have easy install:

すでに easy install がインストールされているなら:


.. code-block:: bash

    $ easy_install Pylons==0.9.7


.. note::

    .. On rare occasions, the python.org Cheeseshop goes down. It is
    .. still possible to install Pylons and its dependencies however
    .. by specifying our local package directory for installation
    .. with:

    たまに python.org Cheeseshop が落ちていることがあります。その場合で
    も、以下のように私たちのローカルパッケージディレクトリを指定するこ
    とで Pylons と依存するパッケージをインストールすることが可能です:


    .. code-block:: bash

        $ easy_install -f http://pylonshq.com/download/ Pylons==0.9.7


    .. Which will use the packages necessary for the latest
    .. release. If you're using an older version of Pylons, you can
    .. get the packages that went with it by specifying the version
    .. desired:

    これは最新のリリースに必要なパッケージを使用します。 Pylons の過去
    のバージョンを使用しているなら、それと共にバージョンを指定すること
    によって必要なパッケージを入手することができます:


    .. code-block:: bash

        $ easy_install -f http://pylonshq.com/download/0.9.7/ Pylons==0.9.7


.. Otherwise: 

別の方法:

.. #. Download the easy install setup file from http://peak.telecommunity.com/dist/ez_setup.py
.. #. Run:

#. http://peak.telecommunity.com/dist/ez_setup.py から easy install セットアップファイルをダウンロードする
#. 以下を実行:


.. code-block:: bash

    $ python ez_setup.py Pylons==0.9.7


.. warning::

    .. **END OF SUPPORT FOR PYTHON 2.3** This is the **LAST** version
    .. to support Python 2.3 **BEGIN UPGRADING OR DIE**

    **Python 2.3 のサポート終了** これは Python 2.3 をサポートする **最
    後の** バージョンです。 **BEGIN UPGRADING OR DIE**
