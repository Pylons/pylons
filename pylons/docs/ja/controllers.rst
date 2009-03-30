.. _controllers:

=============
コントローラ
=============

.. image:: _static/pylon2.jpg
   :alt: 
   :align: left
   :height: 450px
   :width: 368px


.. In the :term:`MVC` paradigm the *controller* interprets the inputs,
.. commanding the model and/or the view to change as
.. appropriate. Under Pylons, this concept is extended slightly in
.. that a Pylons controller is not directly interpreting the clients
.. request, but is acting to determine the appropriate way to assemble
.. data from the model, and render it with the correct template.

:term:`MVC` パラダイムでは、 *コントローラ* は入力を解釈し、モデル
and/or ビューに対して適切に変化するように命令します。 Pylons の下ではこ
の概念はわずかに拡張されています。Pylons コントローラは直接クライアント
要求を解釈するのではなく、モデルからデータを集め、正しいテンプレートで
それをレンダリングする適切な方法を決定するために振る舞います。


.. The controller interprets requests from the user and calls portions
.. of the model and view as necessary to fulfill the request. So when
.. the user clicks a Web link or submits an HTML form, the controller
.. itself doesn’t output anything or perform any real processing. It
.. takes the request and determines which model components to invoke
.. and which formatting to apply to the resulting data.

コントローラはユーザからのリクエストを解釈して、そのリクエストを実現す
るために必要に応じてモデルとビューの一部を呼びます。したがって、ユーザ
がウェブリンクをクリックしたり HTML フォームを送信したりするとき、コン
トローラ自体は何も出力せず、実際の処理は何も実行しません。 それはリクエ
ストを受け取って、どのモデルの部品を呼び出すか、そして、結果として起こ
るデータにどのフォーマットを適用したらよいかを決定します。


.. Pylons uses a class, where the superclass provides the :term:`WSGI`
.. interface and the subclass implements the application-specific
.. controller logic.

Pylons はクラスを使用します。その親クラスは :term:`WSGI` インタフェース
を提供し、サブクラスがアプリケーション固有のコントローラロジックを実装
します。


.. The Pylons WSGI Controller handles incoming web requests that are
.. dispatched from the Pylons WSGI application
.. :class:`~pylons.wsgiapp.PylonsApp`.

Pylons WSGI コントローラは Pylons WSGI アプリケーション
:class:`~pylons.wsgiapp.PylonsApp` からディスパッチされて来るウェブリク
エストを扱います。


.. These requests result in a new instance of the
.. :class:`~pylons.controllers.core.WSGIController` being created,
.. which is then called with the dict options from the Routes
.. match. The standard WSGI response is then returned with
.. start_response called as per the WSGI spec.

これらのリクエストによって
:class:`~pylons.controllers.core.WSGIController` の新しいインスタンスが
作られます。それは次に、 Routes マッチからの dict オプションと共に呼ば
れます。そして、 WSGI 仕様に従って start_response が呼ばれるとともに標
準のWSGI レスポンスが返ります。


.. Since Pylons controllers are actually called with the WSGI
.. interface, normal WSGI applications can also be Pylons
.. ‘controllers’.

Pylons コントローラが実際に WSGI インタフェースで呼ばれるので、通常の
WSGI アプリケーションもまた Pylons `コントローラ` になることができます。


.. Standard Controllers

標準のコントローラ
====================

.. Standard Controllers intended for subclassing by web developers

標準のコントローラは、ウェブ開発者がサブクラス化することを意図しています。


.. Keeping methods private

メソッドをプライベートに保つ
-----------------------------

.. The default route maps any controller and action, so you will
.. likely want to prevent some controller methods from being callable
.. from a URL.

デフォルトのルーティングはあらゆるコントローラとアクションをマッピング
するので、おそらくコントローラメソッドのいくつかを URL から呼べないよう
にしたいと思うでしょう。


.. Routes uses the default Python convention of private methods
.. beginning with ``_``. To hide a method ``edit_generic`` in this
.. class, just changing its name to begin with ``_`` will be
.. sufficient:

Routes は、プライベートなメソッドを ``_`` で始めるという Python のデフォ
ルト規約を使用します。クラスの ``edit_generic`` メソッドを隠すためには、
単に ``_`` で始まるように名前を変更するだけで十分です。


.. code-block:: python

    class UserController(BaseController):
        def index(self):
            return "This is the index."

        def _edit_generic(self):
            """I can't be called from the web!"""
            return True


.. Special methods

特殊メソッド
---------------

.. Special controller methods you may define:

以下の特殊コントローラメソッドを定義することができます:


``__before__``
    .. This method is called before your action is, and should be used
    .. for setting up variables/objects, restricting access to other
    .. actions, or other tasks which should be executed before the
    .. action is called.

    このメソッドは、アクションが実行される前に呼ばれます。変数/オブジェ
    クトをセットアップしたり、他のアクションへのアクセスを制限したり、
    またはアクションが呼ばれる前に実行すべき他のタスクのために使用でき
    ます。

``__after__``
    .. This method is called after the action is, unless an unexpected
    .. exception was raised. Subclasses of
    .. :class:`~webob.exc.HTTPException` (such as those raised by
    .. ``redirect_to`` and ``abort``) are expected; e.g. ``__after__``
    .. will be called on redirects.

    このメソッドは、予期しない例外が raise されない限り、アクションが実
    行された後で実行されます。 :class:`~webob.exc.HTTPException` のサブ
    クラス (例えば ``redirect_to`` や ``abort`` で raise されるもの) は
    予期された例外です。従ってリダイレクトされた場合も ``__after__`` は
    呼ばれます。

    
.. Adding Controllers dynamically

コントローラを動的に追加する
------------------------------

.. It is possible for an application to add controllers without
.. restarting the application. This requires telling Routes to re-scan
.. the controllers directory.

アプリケーションをリスタートすることなしにコントローラを加えることは可
能です。そのためには、 Routes にコントローラディレクトリを再スキャンす
るように伝えます。


.. New controllers may be added from the command line with the paster
.. command (recommended as that also creates the test harness file),
.. or any other means of creating the controller file.

新しいコントローラは、コマンドラインから paster コマンドを用いるか (同
時にテストハーネスのファイルも作成されるのでおすすめです) 、またはコン
トローラファイルを作成する他の手段で追加することができます。


.. For Routes to become aware of new controllers present in the
.. controller directory, an internal flag is toggled to indicate that
.. Routes should rescan the directory:

Routes がコントローラディレクトリに存在している新しいコントローラを認識
するように、 Routes がディレクトリを再スキャンすべきことを示すための内
部フラグを切り換えます:


.. code-block:: python

    from routes import request_config

    mapper = request_config().mapper
    mapper._created_regs = False


.. On the next request, Routes will rescan the controllers directory
.. and those routes that use the ``:controller`` dynamic part of the
.. path will be able to match the new controller.

次回のリクエストのときに Routes が controllers ディレクトリを再スキャン
し、パスの動的部分に ``:controller`` を使っているルートが新しいコントロー
ラにマッチするようになります。


.. Attaching WSGI apps

WSGI アプリケーションを接続する
----------------------------------

.. note::

    .. This recipe assumes a basic level of familiarity with the WSGI
    .. Specification (PEP 333)

    このレシピは WSGI Specification (PEP 333) の基本的なレベルに馴染み
    があることを仮定しています。


.. WSGI runs deep through Pylons, and is present in many parts of the
.. architecture. Since Pylons controllers are actually called with the
.. WSGI interface, normal WSGI applications can also be Pylons
.. 'controllers'.

WSGI は Pylons を深く貫いており、アーキテクチャの多くの部分に存在してい
ます。 Pylons コントローラが実際に WSGI インタフェースで呼ばれるので、
通常の WSGI アプリケーションもまた Pylons 'コントローラ' になることがで
きます。


.. Optionally, if a full WSGI app should be mounted and handle the
.. remainder of the URL, Routes can automatically move the right part
.. of the URL into the :envvar:`SCRIPT_NAME`, so that the WSGI
.. application can properly handle its :envvar:`PATH_INFO` part.

オプションで、もし完全な WSGI アプリケーションをマウントして URL の残り
の部分を処理させたいなら、 Routes は自動的に URL の正しい部分を
:envvar:`SCRIPT_NAME` に移動することができます。これによって WSGI アプ
リケーションが適切に :envvar:`PATH_INFO` 部分を処理できるようになります。


.. This recipe will demonstrate adding a basic WSGI app as a Pylons
.. controller.

このレシピは、基本的な WSGI アプリケーションを Pylons コントローラとし
て加えることを実演します。


.. Create a new controller file in your Pylons project directory:

Pylons プロジェクトディレクトリに新しいコントローラファイルを作成してく
ださい:


.. code-block:: python

    $ paster controller wsgiapp


.. This sets up the basic imports that you may want available when
.. using other WSGI applications.

これは、他の WSGI アプリケーションを使用する際に利用したいであろう基本
的な インポートをセットアップします。


.. Edit your controller so it looks like this:

このようにコントローラを編集してください:


.. code-block:: python

    import logging

    from YOURPROJ.lib.base import *

    log = logging.getLogger(__name__)

    def WsgiappController(environ, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ["Hello World"]


.. When hooking up other WSGI applications, they will expect the part
.. of the URL that was used to get to this controller to have been
.. moved into :envvar:`SCRIPT_NAME`. :mod:`Routes <routes>` can
.. properly adjust the environ if a map route for this controller is
.. added to the :file:`config/routing.py` file:

他の WSGI アプリケーションを接続するとき、それはこのコントローラを得る
ために使用された URL の部分が :envvar:`SCRIPT_NAME` に移動されているこ
とを期待します。このコントローラのためのマップルートが
:file:`config/routing.py` ファイルに追加されるなら、 :mod:`Routes
<routes>` は environ を 適切に調整することができます。


.. code-block:: python

    # CUSTOM ROUTES HERE

    # Map the WSGI application
    map.connect('wsgiapp/{path_info:.*}', controller='wsgiapp')


.. By specifying the ``path_info`` dynamic path, Routes will put
.. everything leading up to the ``path_info`` in the
.. :envvar:`SCRIPT_NAME` and the rest will go in the
.. :envvar:`PATH_INFO`.

``path_info`` 変数を指定することによって、 Routes は ``path_info`` に
leading up to するすべてを :envvar:`SCRIPT_NAME` に入れて、残りは
:envvar:`PATH_INFO` に入るでしょう。


.. Using the WSGI Controller to provide a WSGI service

WSGI サービスを提供するために WSGI コントローラを使用する
===========================================================

.. The Pylons WSGI Controller

Pylons WSGI コントローラ
--------------------------

.. Pylons' own WSGI Controller follows the WSGI spec for calling and
.. return values

Pylons 自身の WSGI コントローラは、呼び出しと値の返却のために WSGI 仕様
に従います。


.. The Pylons WSGI Controller handles incoming web requests that are
.. dispatched from ``PylonsApp``. These requests result in a new
.. instance of the ``WSGIController`` being created, which is then
.. called with the dict options from the Routes match. The standard
.. WSGI response is then returned with :meth:`start_response` called
.. as per the WSGI spec.


Pylons の WSGI コントローラは ``PylonsApp`` からディスパッチされて来る
ウェブリクエストを扱います。これらのリクエストによって
``WSGIController`` の新しいインスタンスが作成されます。次に、 Routes マッ
チからの dict オプションを伴って呼ばれます。そして、 WSGI 仕様に従っ
て:meth:`start_response` が呼ばれ、標準の WSGI 応答を返します


.. WSGIController methods

WSGIController のメソッド
--------------------------

.. Special ``WSGIController`` methods you may define:

``WSGIController`` の以下の特殊メソッドを定義することができます:


``__before__``
    .. This method will be run before your action is, and should be
    .. used for setting up variables/objects, restricting access to
    .. other actions, or other tasks which should be executed before
    .. the action is called.

    このメソッドは、アクションが実行される前に実行されます。変数/オブジェ
    クトをセットアップしたり、他のアクションへのアクセスを制限したり、
    またはアクションが呼ばれる前に実行すべき他のタスクのために使用でき
    ます。

``__after__``
    .. Method to run after the action is run. This method will
    .. *always* be run after your method, even if it raises an
    .. Exception or redirects.

    アクションが実行された後で実行されるメソッドです。このメソッドは、
    たとえ例外が上がっても、リダイレクトしても、他のメソッドが呼ばれた
    後に *必ず* 呼ばれます。

(訳注: `特殊メソッド`_ と重複している?)

    
.. Each action to be called is inspected with :meth:`_inspect_call` so
.. that it is only passed the arguments in the Routes match dict that
.. it asks for. The arguments passed into the action can be customized
.. by overriding the :meth:`_get_method_args` function which is
.. expected to return a dict.

呼ばれる各アクションは、 :meth:`_inspect_call` で inspect されて
Routes の match dict の中から必要な値だけが引数として渡されます。アクショ
ンに渡される引数は :meth:`_get_method_args` 関数をオーバーライドするこ
とでカスタマイズできます。この関数は dict を返すことが期待されます。


.. In the event that an action is not found to handle the request, the
.. Controller will raise an "Action Not Found" error if in debug mode,
.. otherwise a ``404 Not Found`` error will be returned.

リクエストを扱うアクションが見つからない場合、コントローラはデバッグモー
ドでは "Action Not Found" エラーを raise します。デバッグモードでなけれ
ば ``404 Not Found`` エラーが返されます。


.. _rest_controller:

.. Using the REST Controller with a RESTful API

RESTful API で REST コントローラを使う
============================================

.. Using the paster restcontroller template

paster restcontroller テンプレートを使う
-----------------------------------------

.. code-block:: bash

    $ paster restcontroller --help

.. Create a REST Controller and accompanying functional test

REST Controller とそれに付属する機能テストを作成してください。


.. The RestController command will create a REST-based Controller file
.. for use with the :meth:`~routes.base.Mapper.resource` REST-based
.. dispatching. This template includes the methods that
.. :meth:`~routes.base.Mapper.resource` dispatches to in addition to
.. doc strings for clarification on when the methods will be called.

RestController コマンドは REST ベースのディスパッチング
:meth:`~routes.base.Mapper.resource` と共に使用される、 REST ベースのコ
ントローラファイルを作成します。このテンプレートには
:meth:`~routes.base.Mapper.resource` がディスパッチするメソッドと、その
メソッドがいつ呼ばれるか明確にするための docstring が含まれています。


.. The first argument should be the singular form of the REST
.. resource. The second argument is the plural form of the word. If
.. its a nested controller, put the directory information in front as
.. shown in the second example below.

最初の引数は REST リソースの単数形であるべきです。 2番目の引数はその単
語の複数形です。 それが入れ子になったコントローラなら、以下の 2 番目の
例に示されるように、ディレクトリ情報をその前に入れてください。


.. Example usage:

使用例:


.. code-block:: bash

    yourproj% paster restcontroller comment comments
    Creating yourproj/yourproj/controllers/comments.py
    Creating yourproj/yourproj/tests/functional/test_comments.py


.. If you'd like to have controllers underneath a directory, just
.. include the path as the controller name and the necessary
.. directories will be created for you:

コントローラをディレクトリの下に置きたければ、単にコントローラ名にパス
を含めてください。そうすれば必要なディレクトリが作成されます:


.. code-block:: bash

    $ paster restcontroller admin/trackback admin/trackbacks
    Creating yourproj/controllers/admin
    Creating yourproj/yourproj/controllers/admin/trackbacks.py
    Creating yourproj/yourproj/tests/functional/test_admin_trackbacks.py


.. An Atom-Style REST Controller for Users

Atom スタイルのユーザ REST コントローラ
---------------------------------------

.. code-block:: python

    # From http://pylonshq.com/pasties/503
    import logging

    from formencode.api import Invalid
    from pylons import url
    from simplejson import dumps

    from restmarks.lib.base import *

    log = logging.getLogger(__name__)

    class UsersController(BaseController):
        """REST Controller styled on the Atom Publishing Protocol"""
        # To properly map this controller, ensure your 
        # config/routing.py file has a resource setup:
        #     map.resource('user', 'users')

        def index(self, format='html'):
            """GET /users: All items in the collection.<br>
                @param format the format passed from the URI.
            """
            #url('users')
            users = model.User.select()
            if format == 'json':
                data = []
                for user in users:
                    d = user._state['original'].data
                    del d['password']
                    d['link'] = url('user', id=user.name)
                    data.append(d)
                response.headers['content-type'] = 'text/javascript'
                return dumps(data)
            else:
                c.users = users
                return render('/users/index_user.mako')

        def create(self):
            """POST /users: Create a new item."""
            # url('users')
            user = model.User.get_by(name=request.params['name'])
            if user:
                # The client tried to create a user that already exists
                abort(409, '409 Conflict', 
                      headers=[('location', url('user', id=user.name))])
            else:
                try:
                    # Validate the data that was sent to us
                    params = model.forms.UserForm.to_python(request.params)
                except Invalid, e:
                    # Something didn't validate correctly
                    abort(400, '400 Bad Request -- %s' % e)
                user = model.User(**params)
                model.objectstore.flush()
                response.headers['location'] = url('user', id=user.name)
                response.status_code = 201
                c.user_name = user.name
                return render('/users/created_user.mako')

        def new(self, format='html'):
            """GET /users/new: Form to create a new item.
                @param format the format passed from the URI.
            """
            # url('new_user')
            return render('/users/new_user.mako')

        def update(self, id):
            """PUT /users/id: Update an existing item.
                @param id the id (name) of the user to be updated
            """
            # Forms posted to this method should contain a hidden field:
            #    <input type="hidden" name="_method" value="PUT" />
            # Or using helpers:
            #    h.form(url('user', id=ID),
            #           method='put')
            # url('user', id=ID)
            old_name = id
            new_name = request.params['name']
            user = model.User.get_by(name=id)

            if user:
                if (old_name != new_name) and model.User.get_by(name=new_name):
                    abort(409, '409 Conflict')
                else:
                    params = model.forms.UserForm.to_python(request.params)
                    user.name = params['name']
                    user.full_name = params['full_name']
                    user.email = params['email']
                    user.password = params['password']
                    model.objectstore.flush()
                    if user.name != old_name:
                        abort(301, '301 Moved Permanently',
                              [('Location', url('users', id=user.name))])
                    else:
                        return

        def delete(self, id):
            """DELETE /users/id: Delete an existing item.
                @param id the id (name) of the user to be updated
            """
            # Forms posted to this method should contain a hidden field:
            #    <input type="hidden" name="_method" value="DELETE" />
            # Or using helpers:
            #    h.form(url('user', id=ID),
            #           method='delete')
            # url('user', id=ID)
            user = model.User.get_by(name=id)
            user.delete()
            model.objectstore.flush()
            return

        def show(self, id, format='html'):
            """GET /users/id: Show a specific item.
                @param id the id (name) of the user to be updated.
                @param format the format of the URI requested.
            """
            # url('user', id=ID)
            user = model.User.get_by(name=id)
            if user:
                if format=='json':
                    data = user._state['original'].data
                    del data['password']
                    data['link'] = url('user', id=user.name)
                    response.headers['content-type'] = 'text/javascript'
                    return dumps(data)
                else:
                    c.data = user
                    return render('/users/show_user.mako')
            else:
                abort(404, '404 Not Found')

        def edit(self, id, format='html'):
            """GET /users/id;edit: Form to edit an existing item.
                @param id the id (name) of the user to be updated.
                @param format the format of the URI requested.
            """
            # url('edit_user', id=ID)
            user = model.User.get_by(name=id)
            if not user:
                abort(404, '404 Not Found')
            # Get the form values from the table
            c.values = model.forms.UserForm.from_python(user.__dict__)
            return render('/users/edit_user.mako')


.. _xmlrpc_controller:

.. Using the XML-RPC Controller for XML-RPC requests

XML-RPC リクエストに XML-RPC コントローラを使う
================================================= 

.. In order to deploy this controller you will need at least a passing
.. familiarity with XML-RPC itself. We will first review the basics of
.. XML-RPC and then describe the workings of the ``Pylons
.. XMLRPCController``. Finally, we will show an example of how to use
.. the controller to implement a simple web service.

このコントローラを deploy するために、少なくとも XML-RPC それ自身に対す
るちょっとした慣れが必要でしょう。この文書では、最初に XML-RPC の基礎を
復習した後で、 ``Pylons XMLRPCController`` の働きについて説明します。最
後に、簡単なウェブサービスを実行するために、このコントローラをどのよう
に使用するかに関する例を示します。


.. After you've read this document, you may be interested in reading
.. the companion document: "A blog publishing web service in XML-RPC"
.. which takes the subject further, covering details of the MetaWeblog
.. API (a popular XML-RPC service) and demonstrating how to construct
.. some basic service methods to act as the core of a MetaWeblog blog
.. publishing service.

この文書を読んだ後で、 XML-RPC についてより詳しく説明している "A blog
publishing web service in XML-RPC" を読んだほうが良いでしょう。このガイ
ドでは MetaWeblog API (ポピュラーな XML-RPC サービス) の細部をカバーす
るとともに、MetaWeblog ブログ公開サービスの中核として機能するいくつかの
基本サービス方法を構成する方法が示されています。


.. A brief introduction to XML-RPC

XML-RPC の簡単なイントロダクション
-----------------------------------

.. XML-RPC is a specification that describes a Remote Procedure Call
.. (RPC) interface by which an application can use the Internet to
.. execute a specified procedure call on a remote XML-RPC server. The
.. name of the procedure to be called and any required parameter
.. values are "marshalled" into XML. The XML forms the body of a POST
.. request which is despatched via HTTP to the XML-RPC server. At the
.. server, the procedure is executed, the returned value(s) is/are
.. marshalled into XML and despatched back to the application. XML-RPC
.. is designed to be as simple as possible, while allowing complex
.. data structures to be transmitted, processed and returned.

XML-RPC は Remote Procedure Call (RPC) インタフェースを記述する仕様です。
XML-RPC を使えば、アプリケーションはインターネットを介して特定のプロシー
ジャ呼び出しをリモート XML-RPC サーバ上で実行することができます。呼び出
されるプロシージャの名前とすべての必須パラメータ値は XML 形式に "直列化"
(marshal) されます。この XML は、 HTTP を経由して XML-RPC サーバへと送
信される POST リクエストのボディーを形成します。サーバではプロシージャ
が実行され、その戻り値が XML 形式に直列化されてアプリケーションに返され
ます。 XML-RPC は、できるだけ単純になるように設計されている一方で、複雑
なデータ構造を送受信して処理を行わせることができます。


.. XML-RPC Controller that speaks WSGI 

WSGI を話す XML-RPC コントローラ
-----------------------------------

.. Pylons uses Python's xmlrpclib library to provide a specialised
.. :class:`XMLRPCController` class that gives you the full range of
.. these XML-RPC Introspection facilities for use in your service
.. methods and provides the foundation for constructing a set of
.. specialised service methods that provide a useful web service ---
.. such as a blog publishing interface.

Pylons は Python の xmlrpclib ライブラリを使用して独自の
:class:`XMLRPCController` クラスを提供します。このクラスはサービスメソッ
ドの中で使用することができる様々な XML-RPC イントロスペクション機能を提
供しています。また、(ブログ公開インタフェースのような) 便利なウェブサー
ビスを提供する 1 セットの独自のサービスメソッドを構成するための基礎を提
供します。


.. This controller handles XML-RPC responses and complies with the
.. `XML-RPC Specification <http://www.xmlrpc.com/spec>`_ as well as
.. the `XML-RPC Introspection
.. <http://scripts.incutio.com/xmlrpc/introspection.html>`_
.. specification.

このコントローラは XML-RPC レスポンスを扱い、 `XML-RPC 仕様
<http://www.xmlrpc.com/spec>`_ と `XML-RPC イントロスペクション
<http://scripts.incutio.com/xmlrpc/introspection.html>`_ 仕様に従います。


.. As part of its basic functionality an XML-RPC server provides three
.. standard introspection procedures or "service methods" as they are
.. called. The Pylons :class:`XMLRPCController` class provides these
.. standard service methods ready-made for you:

基本機能の一部として、 XML-RPC サーバは 3 つの標準的なイントロスペクショ
ン・プロシージャ、あるいは「サービスメソッド」を提供します (as they
are called)。 Pylons の :class:`XMLRPCController` クラスは、これらの標
準サービスメソッドを ready-made で提供します:


.. * :meth:`system.listMethods` Returns a list of XML-RPC methods for this XML-RPC resource 
.. * :meth:`system.methodSignature` Returns an array of arrays for the valid signatures for a method. The first value of each array is the return value of the method. The result is an array to indicate multiple signatures a method may be capable of. 
.. * :meth:`system.methodHelp` Returns the documentation for a method 

* :meth:`system.listMethods` XML-RPC リソースのメソッド一覧を返します。
* :meth:`system.methodSignature` メソッドの有効なシグネチャを表す配列の配列を返します。それぞれの配列の最初の値はメソッドの戻り値です。 その結果はメソッドが処理できる複数のシグネチャを表す配列です。
* :meth:`system.methodHelp` メソッドのドキュメンテーションを返します


.. By default, methods with names containing a dot are translated to
.. use an underscore. For example, the ``system.methodHelp`` is
.. handled by the method :meth:`system_methodHelp`.

デフォルトでは、メソッド名に含まれるドットはアンダースコアに変換されま
す。 例えば、 ``system.methodHelp`` はメソッド
:meth:`system_methodHelp` によって処理されることになります。


.. Methods in the XML-RPC controller will be called with the method
.. given in the XML-RPC body. Methods may be annotated with a
.. signature attribute to declare the valid arguments and return
.. types.

XML-RPC コントローラのメソッドは XML-RPC ボディに与えられたメソッドで呼
ばれます。 メソッドは signature 属性でアノテートすることによって、有効
な引数と戻り値の型を宣言することができます。


.. For example:

以下に例を示します:


.. code-block:: python

    class MyXML(XMLRPCController): 
        def userstatus(self): 
            return 'basic string' 
        userstatus.signature = [['string']] 

        def userinfo(self, username, age=None): 
            user = LookUpUser(username) 
            result = {'username': user.name} 
            if age and age > 10: 
                result['age'] = age 
            return result 
        userinfo.signature = [['struct', 'string'], 
                              ['struct', 'string', 'int']]


.. Since XML-RPC methods can take different sets of data, each set of
.. valid arguments is its own list. The first value in the list is the
.. type of the return argument. The rest of the arguments are the
.. types of the data that must be passed in.

XML-RPC メソッドは異なったデータセットを受け取ることができるので、それ
ぞれの有効な引数のセットはそれ自身のリストです。 リストにおける最初の値
は戻り値の型です。 引数の残りはそれに対して渡さなければならないデータの
型です。


.. In the last method in the example above, since the method can
.. optionally take an integer value, both sets of valid parameter
.. lists should be provided.

上の例における最後のメソッドでは、メソッドがオプションの整数値を取るこ
とができるので、有効なパラメータリストの両方のセットを与える必要があり
ます。


.. Valid types that can be checked in the signature and their
.. corresponding Python types:

シグネチャでチェックできる有効な型と Python 型の対応表を以下の表に示します:


+--------------------+--------------------+
| XMLRPC             | Python             |
+====================+====================+
| string             | str                |
+--------------------+--------------------+
| array              | list               |
+--------------------+--------------------+
| boolean            | bool               |
+--------------------+--------------------+
| int                | int                |
+--------------------+--------------------+
| double             | float              |
+--------------------+--------------------+
| struct             | dict               |
+--------------------+--------------------+
| dateTime.iso8601   | xmlrpclib.DateTime |
+--------------------+--------------------+
| base64             | xmlrpclib.Binary   |
+--------------------+--------------------+


.. Note, requiring a signature is optional. 

シグネチャを与えるかどうかはオプションであることに注意してください。


.. Also note that a convenient fault handler function is provided. 

また、便利な fault handler 関数が提供されることに注意してください。


.. code-block:: python 

    def xmlrpc_fault(code, message): 
        """Convenience method to return a Pylons response XMLRPC Fault""" 


.. (The `XML-RPC Home page <http://www.xmlrpc.com/>`_ and the `XML-RPC
.. HOW-TO <http://www.faqs.org/docs/Linux-HOWTO/XML-RPC-HOWTO.html>`_
.. both provide further detail on the XML-RPC specification.)

(`XML-RPC ホームページ <http://www.xmlrpc.com/>`_ と `XML-RPC HOW-TO
<http://www.faqs.org/docs/Linux-HOWTO/XML-RPC-HOWTO.html>`_ の両方が、
XML-RPC 仕様に関する詳細を提供します。)


.. A simple XML-RPC service  

単純な XML-RPC サービス
------------------------

.. This simple service ``test.battingOrder`` accepts a positive
.. integer < 51 as the parameter ``posn`` and returns a string
.. containing the name of the US state occupying that ranking in the
.. order of ratifying the constitution / joining the union.

この単純なサービス ``test.battingOrder`` は、 ``posn`` というパラメタで
51 未満の正の整数を受け取り、憲法を批准した/組合に加盟した順番でランク
付けしたアメリカの州名を含む文字列を返します。


.. code-block:: python
 
    import xmlrpclib

    from pylons import request
    from pylons.controllers import XMLRPCController

    states = ['Delaware', 'Pennsylvania', 'New Jersey', 'Georgia',
              'Connecticut', 'Massachusetts', 'Maryland', 'South Carolina',
              'New Hampshire', 'Virginia', 'New York', 'North Carolina',
              'Rhode Island', 'Vermont', 'Kentucky', 'Tennessee', 'Ohio',
              'Louisiana', 'Indiana', 'Mississippi', 'Illinois', 'Alabama',
              'Maine', 'Missouri', 'Arkansas', 'Michigan', 'Florida', 'Texas',
              'Iowa', 'Wisconsin', 'California', 'Minnesota', 'Oregon',
              'Kansas', 'West Virginia', 'Nevada', 'Nebraska', 'Colorado',
              'North Dakota', 'South Dakota', 'Montana', 'Washington', 'Idaho',
              'Wyoming', 'Utah', 'Oklahoma', 'New Mexico', 'Arizona', 'Alaska',
              'Hawaii'] 

    class RpctestController(XMLRPCController): 

        def test_battingOrder(self, posn): 
            """This docstring becomes the content of the 
            returned value for system.methodHelp called with 
            the parameter "test.battingOrder"). The method 
            signature will be appended below ... 
            """ 
            # XML-RPC checks agreement for arity and parameter datatype, so 
            # by the time we get called, we know we have an int. 
            if posn > 0 and posn < 51: 
                return states[posn-1] 
            else: 
                # Technically, the param value is correct: it is an int. 
                # Raising an error is inappropriate, so instead we 
                # return a facetious message as a string. 
                return 'Out of cheese error.' 
        test_battingOrder.signature = [['string', 'int']] 


.. Testing the service

サービスをテストする
---------------------

.. For developers using OS X, there's an `XML/RPC client
.. <http://www.ditchnet.org/xmlrpc/>`_ that is an extremely useful
.. diagnostic tool when developing XML-RPC (it's free ... but not
.. entirely bug-free). Or, you can just use the Python interpreter:

OS X を使用している開発者のために `XML/RPC クライアント
<http://www.ditchnet.org/xmlrpc/>`_ があります。 それは XML-RPC を開発
する際には非常に役に立つ診断用ツールです (それはフリーです… しかし、全
くバグがないわけではありません)。 あるいは Python インタプリタを使うこ
ともできます:


.. code-block:: pycon

    >>> from pprint import pprint 
    >>> import xmlrpclib 
    >>> srvr = xmlrpclib.Server("http://example.com/rpctest/") 
    >>> pprint(srvr.system.listMethods()) 
    ['system.listMethods', 
     'system.methodHelp', 
     'system.methodSignature', 
     'test.battingOrder'] 
    >>> print srvr.system.methodHelp('test.battingOrder') 
    This docstring becomes the content of the 
    returned value for system.methodHelp called with 
    the parameter "test.battingOrder"). The method 
    signature will be appended below ... 

    Method signature: [['string', 'int']] 
    >>> pprint(srvr.system.methodSignature('test.battingOrder')) 
    [['string', 'int']] 
    >>> pprint(srvr.test.battingOrder(12)) 
    'North Carolina' 


.. To debug XML-RPC servers from Python, create the client object
.. using the optional verbose=1 parameter. You can then use the client
.. as normal and watch as the XML-RPC request and response is
.. displayed in the console.

Python から XML-RPC サーバをデバッグするには、クライアントオブジェクト
を作成するときにオプショナルな verbose=1 パラメタを指定してください。そ
うすると、クライアントを通常通り使うことができ、 XML-RPC リクエストとレ
スポンスがコンソールに表示されるのを観察することができます。
