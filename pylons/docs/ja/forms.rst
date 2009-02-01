.. _forms:

===========
フォーム
===========

.. The basics

基本
==========

.. When a user submits a form on a website the data is submitted to
.. the URL specified in the `action` attribute of the `<form>`
.. tag. The data can be submitted either via HTTP `GET` or `POST` as
.. specified by the `method` attribute of the `<form>` tag. If your
.. form doesn't specify an `action`, then it's submitted to the
.. current URL, generally you'll want to specify an `action`. When a
.. file upload field such as `<input type="file" name="file" />` is
.. present, then the HTML `<form>` tag must also specify
.. `enctype="multipart/form-data"` and `method` must be `POST`.

ユーザがウェブサイトのフォームを送信すると、 `<form>` タグの `action`
属性で指定された URL にデータが送信されます。データは `<form>` タグの
`method` 属性によって指定された HTTP `GET` または `POST` によって送信さ
れます。フォームに `action` が指定されていなければ、それは現在の URL に
送信されます。一般に `action` を指定した方が良いでしょう。また、
`<input type="file" name="file" />` のようなファイルアップロードフィー
ルドが存在している場合、 HTML `<form>` タグで
`enctype="multipart/form-data"` を指定しなければならず、 `method` は
`POST` でなければなりません。


Getting Started 
=============== 

.. Add two actions that looks like this: 

このような 2 つのアクションを加えてください:


.. code-block:: python 

    # in the controller 

    def form(self): 
        return render('/form.mako') 

    def email(self): 
        return 'Your email is: %s' % request.params['email'] 


.. Add a new template called `form.mako` in the `templates` directory
.. that contains the following:

`templates` ディレクトリに以下の内容で `form.mako` という名前の新しいテ
ンプレートを加えてください:


.. code-block:: html 

    <form name="test" method="GET" action="/hello/email"> 
    Email Address: <input type="text" name="email" /> 
    <input type="submit" name="submit" value="Submit" /> 
    </form> 


.. If the server is still running (see the :ref:`Getting Started Guide
.. <getting_started>`) you can visit http://localhost:5000/hello/form
.. and you will see the form. Try entering the email address
.. `test@example.com` and clicking Submit. The URL should change to
.. ``http://localhost:5000/hello/email?email=test%40example.com`` and
.. you should see the text `Your email is test@example.com`.

サーバが実行されているなら (:ref:`Getting Started Guide
<getting_started>` を参照)、 http://localhost:5000/hello/form を訪問す
ることができて、フォームが表示されるでしょう。 E メールアドレス
`test@example.com` を入力して、 Submit をクリックしてみてください。URL
は ``http://localhost:5000/hello/email?email=test%40example.com`` に変
化して、テキスト `Your email is test@example.com` が見られるはずです。


.. In Pylons all form variables can be accessed from the
.. :data:`request.params` object which behaves like a dictionary. The
.. keys are the names of the fields in the form and the value is a
.. string with all the characters entity decoded. For example note how
.. the `@` character was converted by the browser to `%40` in the URL
.. and was converted back ready for use in :data:`request.params`.

Pylons では、すべてのフォーム変数は辞書のように振る舞う
:data:`request.params` オブジェクトからアクセスできます。 そのキーは
フォームのフィールドの名前で、値はすべての文字実体がデコードされた文字
列です。 例えば、 `@` 文字列はブラウザによって URL の中で `%40` に変換
されている一方、 :data:`request.params` の中ではすぐに使用できるように
元に戻されていることに注意してください。


.. Note::

    .. `request` and `response` are objects from the `WebOb` library.
    .. Full documentation on their attributes and methods is `here
    .. <http://pythonpaste.org/webob/>`_.

    `request` と `response` は `WebOb` ライブラリのオブジェクトです。そ
    の属性とメソッドの完全なドキュメントは `ここ
    <http://pythonpaste.org/webob/>`_ にあります。


.. If you have two fields with the same name in the form then using
.. the dictionary interface will return the first string. You can get
.. all the strings returned as a list by using the `.getall()`
.. method. If you only expect one value and want to enforce this you
.. should use `.getone()` which raises an error if more than one value
.. with the same name is submitted.

フォームに同じ名前を持った 2 つのフィールドがある場合、辞書インタフェー
スを使用すると、最初の文字列が返されます。 `.getall()` メソッドを使用す
ることによって、すべての文字列をリストとして返させることができます。 1
つの値しか期待していなくて、これを強制したいなら `.getone()` を使用する
べきです。これは同じ名前がある 1 つ以上の値が送信されたらエラーを発生し
ます。


.. By default if a field is submitted without a value, the dictionary
.. interface returns an empty string. This means that using `.get(key,
.. default)` on `request.params` will only return a default if the
.. value was not present in the form.

デフォルトでは、値のないフィールドが送信されると辞書インタフェースは空
の文字列を返します。つまり、 `request.params` の `.get(key, default)`
を使用すると、フォームに値が存在しなかった場合にだけ default が返される
ことを意味します。


.. POST vs GET and the Re-Submitted Data Problem 

POST vs GET とデータの再送信の問題
--------------------------------------------- 

.. If you change the `form.mako` template so that the method is `POST`
.. and you re-run the example you will see the same message is
.. displayed as before. However, the URL displayed in the browser is
.. simply http://localhost:5000/hello/email without the query
.. string. The data is sent in the body of the request instead of the
.. URL, but Pylons makes it available in the same way as for GET
.. requests through the use of `request.params`.

もし `form.mako` テンプレートで method を `POST` に変えて例を再実行する
と、同じメッセージがこれまでと同様に表示されるのを見るでしょう。 しかし、
ブラウザで表示された URL は、クエリ文字列のないただの
http://localhost:5000/hello/email です。データは URL の代わりにリクエス
トのボディーで送られますが、Pylons はそれを GET リクエストの場合と同様
`request.params` を使用して参照できるようにします。


.. note:: 

    .. If you are writing forms that contain password fields you
    .. should usually use POST to prevent the password being visible
    .. to anyone who might be looking at the user's screen.

    パスワードフィールドを含むフォームを書く場合、パスワードがユーザの
    画面を見ているかもしれない誰かの目に入るのを防ぐのに、通常は POST
    を使用するべきです。


.. When writing form-based applications you will occasionally find
.. users will press refresh immediately after submitting a form. This
.. has the effect of repeating whatever actions were performed the
.. first time the form was submitted but often the user will expect
.. that the current page be shown again. If your form was submitted
.. with a POST, most browsers will display a message to the user
.. asking them if they wish to re-submit the data, this will not
.. happen with a GET so POST is preferable to GET in those
.. circumstances.

フォームベースのアプリケーションを書いていると、時折ユーザがフォームを
送信した直後に再読み込みを押すことがわかるでしょう。これには、最初に
フォームが送信されたときに実行されたあらゆるアクションが繰り返されると
いう効果がありますが、ユーザはしばしば現在のページが再表示されると予想
するでしょう。フォームが POST によって送信されたなら、ほとんどのブラウ
ザがユーザにデータを再送信するかどうかを尋ねるメッセージを表示します。
これは GET を使った場合には起こらないので、この点で POST は GET より望
ましいです。


.. Of course, the best way to solve this issue is to structure your
.. code differently so:

もちろん、この問題を解決する最も良い方法は、異なるやり方でコードを構造
化することです:


.. code-block:: python 

    # in the controller 

    def form(self): 
        return render('/form.mako') 

    def email(self): 
        # Code to perform some action based on the form data 
        # ... 
        redirect_to(action='result') 

    def result(self): 
        return 'Your data was successfully submitted' 


.. In this case once the form is submitted the data is saved and an
.. HTTP redirect occurs so that the browser redirects to
.. http://localhost:5000/hello/result. If the user then refreshes the
.. page, it simply redisplays the message rather than re-performing
.. the action.

この場合、いったんフォームが送信されるとデータが保存されて HTTP リダイ
レクトが起こり、ブラウザが http://localhost:5000/hello/result にリダイ
レクトされます。次にユーザがページを再読み込みすると、それはアクション
を再実行する代わりに単にメッセージを再度表示します。


.. Using the Helpers 

helpers を使う
================= 

.. Creating forms can also be done using WebHelpers, which comes with
.. Pylons. Here is the same form created in the previous section but
.. this time using the helpers:

また、フォームを作成するのに WebHelpers を使用することができます。それ
は Pylons に付属しています。これは前のセクションで作成したのと同じフォー
ムですが、今回は helpers を使用しています:


.. code-block:: html+mako 

    ${h.form(h.url(action='email'), method='get')} 
    Email Address: ${h.text('email')} 
    ${h.submit('Submit')} 
    ${h.end_form()} 


.. Before doing this you'll have to import the helpers you want to use
.. into your project's `lib/helpers.py` file; then they'll be
.. available under Pylons' ``h`` global.  Most projects will want to
.. import at least these:

これをする前に、使用したい helper をプロジェクトの `lib/helpers.py` ファ
イルの中にインポートする必要があるでしょう。そうすれば、それらは
Pylons の ``h`` グローバル変数の下で利用可能になります。 ほとんどのプロ
ジェクトでは少なくともこれらをインポートするとよいでしょう:


.. code-block:: python

   from webhelpers.html import escape, HTML, literal, url_escape
   from webhelpers.html.tags import *


.. There are many other helpers for text formatting, container
.. objects, statistics, and for dividing large query results into
.. pages.  See the :mod:`WebHelpers documentation <webhelpers>`
.. documentation to choose the helpers you'll need.

他にもテキスト整形やコンテナーオブジェクト、統計、および巨大なクエリ結
果をページに分割するための多くの helper があります。 :mod:`WebHelpers
のドキュメント <webhelpers>` を見て、あなたが必要とする helper を選んで
ください。


.. _file_uploads:

ファイルアップロード
====================

.. File upload fields are created by using the `file` input field
.. type. The `file_field` helper provides a shortcut for creating
.. these form fields:

ファイルアップロードフィールドは、入力フィールドのタイプ `file` を使用
することによって作成されます。 `file_field` ヘルパーは、これらのフォー
ムフィールドを作成するための近道を提供します:


.. code-block:: mako 

    ${h.file_field('myfile')} 


.. The HTML form must have its `enctype` attribute set to
.. `multipart/form-data` to enable the browser to upload the file. The
.. `form` helper's `multipart` keyword argument provides a shortcut
.. for setting the appropriate `enctype` value:

HTML フォームはブラウザがファイルをアップロードできるように `enctype`
属性を `multipart/form-data` に設定しなければなりません。 `form` ヘルパー
の `multipart` キーワード引数は、適切な `enctype` 値を設定するための近
道を提供します:


.. code-block:: html+mako 

    ${h.form(h.url(action='upload'), multipart=True)} 
    Upload file: ${h.file_field('myfile')} <br /> 
    File description: ${h.text_field('description')} <br /> 
    ${h.submit('Submit')} 
    ${h.end_form()} 


.. When a file upload has succeeded, the `request.POST` (or
.. `request.params`) `MultiDict` will contain a `cgi.FieldStorage` object
.. as the value of the field.

ファイルアップロードが成功したとき、 `request.POST` (または
`request.params`) `MultiDict` は、フィールドの値として
`cgi.FieldStorage` オブジェクトを含むでしょう。


.. `FieldStorage` objects have three important attributes for file
.. uploads:

`FieldStorage` オブジェクトには、ファイルアップロードのための3つの重要
な属性があります:


`filename` 

    .. The name of file uploaded as it appeared on the uploader's filesystem. 

    アップロードしたユーザのファイルシステム上での、アップロードされた
    ファイルの名前


`file` 

    .. A file(-like) object from which the file's data can be read: A
    .. python `tempfile` or a `StringIO` object.

    ファイルのデータを読むことができる file(-like) オブジェクト:
    Python `tempfile` か `StringIO` オブジェクト。


`value` 

    .. The content of the uploaded file, eagerly read directly from
    .. the file object.

    事前にファイルオブジェクトから直接読み込まれた、アップロードされた
    ファイルの中身


.. The easiest way to gain access to the file's data is via the
.. `value` attribute: it returns the entire contents of the file as a
.. string:

ファイルのデータへアクセスする最も簡単な方法は `value` 属性を使用するこ
とです: それは文字列としてファイル全体の内容を返します:


.. code-block:: python 

    def upload(self): 
        myfile = request.POST['myfile'] 
        return 'Successfully uploaded: %s, size: %i, description: %s' % \ 
            (myfile.filename, len(myfile.value), request.POST['description']) 


.. However reading the entire contents of the file into memory is
.. undesirable, especially for large file uploads. A common means of
.. handling file uploads is to store the file somewhere on the
.. filesystem. The `FieldStorage` typically reads the file onto
.. filesystem, however to a non permanent location, via a python
.. `tempfile` object (though for very small uploads it stores the file
.. in a `StringIO` object instead).

しかしながら、特に大きなファイルのアップロードでは、メモリからファイル
の全体のコンテンツを読み取ることは望ましくありません。ファイルアップロー
ドの一般的な取り扱い手段は、ファイルをファイルシステムのどこかに保存す
ることです。 `FieldStorage` は通常ファイルをファイルシステムへ読み込み
ますが、それは Python `tempfile` オブジェクトを通して非永久的な位置に保
存されます (非常に小さいアップロードに対しては、代わりに `StringIO` オ
ブジェクトが使われることもあります)。


.. Python `tempfiles` are secure file objects that are automatically
.. destroyed when they are closed (including an implicit close when
.. the object is garbage collected). One of their security features is
.. that their path cannot be determined: a simple `os.rename` from the
.. `tempfile's` path isn't possible. Alternatively,
.. `shutil.copyfileobj` can perform an efficient copy of the file's
.. data to a permanent location:

Python `tempfiles` は、 close されるとき (ガベージコレクションによって
暗黙的に close される場合を含む) に自動的に破壊される、 secure なファイ
ルオブジェクトです。それらのセキュリティ機能の 1 つは、それらのパスが決
定できないということです: `tempfile` のパスからは単純な `os.rename` が
できません。代わりに、 `shutil.copyfileobj` はファイルデータを永久的な
位置へ効率的にコピーすることができます:


.. code-block:: python 

    permanent_store = '/uploads/' 

    class Uploader(BaseController): 
        def upload(self): 
            myfile = request.POST['myfile'] 
            permanent_file = open(os.path.join(permanent_store, 
                                    myfile.filename.lstrip(os.sep)), 
                                    'w') 

        shutil.copyfileobj(myfile.file, permanent_file) 
        myfile.file.close() 
        permanent_file.close() 

        return 'Successfully uploaded: %s, description: %s' % \ 
            (myfile.filename, request.POST['description']) 


.. warning:: 

    .. The previous basic example allows any file uploader to
    .. overwrite any file in the `permanent_store` directory that your
    .. web application has permissions to.

    前の基本的な例では、ファイルをアップロードするユーザは
    `permanent_store` ディレクトリ内でウェブアプリケーションがパーミッ
    ションを持っているあらゆるファイルを上書きすることができます。


.. Also note the use of `myfile.filename.lstrip(os.sep)` here: without
.. it, `os.path.join` is unsafe. `os.path.join` won't join absolute
.. paths (beginning with `os.sep`), i.e. `os.path.join('/uploads/',
.. '/uploaded_file.txt')` == `'/uploaded_file.txt'`. Always check user
.. submitted data to be used with `os.path.join`.

また、ここで `myfile.filename.lstrip(os.sep)` を使用していることに注意
してください: それがなければ、 `os.path.join` は危険です。
`os.path.join` は (`os.sep` で始まる) 絶対パスを join しません。つまり、
`os.path.join('/uploads/', '/uploaded_file.txt')` ==
`'/uploaded_file.txt'` です。ユーザが送信したデータを `os.path.join` と
共に使用する場合、常にチェックして下さい。


.. Validating user input with FormEncode

FormEncode を使用してユーザの入力をバリデーションする
=====================================================

.. Validation the Quick Way 

簡単な方法
------------------------

.. At the moment you could enter any value into the form and it would
.. be displayed in the message, even if it wasn't a valid email
.. address. In most cases this isn't acceptable since the user's input
.. needs validating. The recommended tool for validating forms in
.. Pylons is `FormEncode <http://www.formencode.org>`_.

これまでのところ、フォームにどんな値でも入力することができます。そして、
有効な E メールアドレスではなかったとしても、それをメッセージに表示する
でしょう。多くの場合、ユーザの入力に対してバリデーションを行う必要があ
るので、これは許容できません。 Pylons でフォームのバリデーションを行う
ためのお勧めのツールは `FormEncode <http://www.formencode.org>`_ です。


.. For each form you create you also create a validation schema. In
.. our case this is fairly easy:

また、作成した各フォームのためにバリデーションスキーマを作成します。今
の場合、これはかなり簡単です:


.. code-block:: python 

    import formencode 

    class EmailForm(formencode.Schema): 
        allow_extra_fields = True 
        filter_extra_fields = True 
        email = formencode.validators.Email(not_empty=True) 


.. note:: 

    .. We usually recommend keeping form schemas together so that you
    .. have a single place you can go to update them. It's also
    .. convenient for inheritance since you can make new form schemas
    .. that build on existing ones. If you put your forms in a
    .. `models/form.py` file, you can easily use them throughout your
    .. controllers as `model.form.EmailForm` in the case shown.

    通常、フォームのスキーマを一緒にしておいて、スキーマを更新するため
    の単一の場所を持つことを勧めます。新しいフォームスキーマを既存のも
    のの上に作ることができるので、それは継承にも便利です。フォームを
    `models/form.py` ファイルに入れるなら、この例ではコントローラ中で
    `model.form.EmailForm` として容易にそれらを使用できます。


.. Our form actually has two fields, an email text field and a submit
.. button. If extra fields are submitted FormEncode's default behavior
.. is to consider the form invalid so we specify `allow_extra_fields =
.. True`. Since we don't want to use the values of the extra fields we
.. also specify `filter_extra_fields = True`. The final line specifies
.. that the email field should be validated with an `Email()`
.. validator. In creating the validator we also specify
.. `not_empty=True` so that the email field will require input.

このフォームには、実際に 2 つのフィールド、メールテキストフィールドと送
信ボタンがあります。余分なフィールドが送信された場合 FormEncode のデフォ
ルトの振舞いではフォームが無効とみなされるので、 `allow_extra_fields =
True` を指定します。また、余分なフィールドの値を使用したいとは思わない
ので、 `filter_extra_fields = True` を指定します。 最後の行は、メール
フィールドが `Email()` バリデータでバリデーションされるべきであると指定
します。 また、バリデータを作成する際に、メールフィールドが入力を必要と
するように `not_empty=True` を指定します。


.. Pylons comes with an easy to use `validate` decorator, if you wish
.. to use it import it in your `lib/base.py` like this:

Pylons は簡単に使える `validate` デコレータを含んでいます。それを使用し
たければ、このように `lib/base.py` でそれをインポートしてください:


.. code-block:: python

    # other imports

    from pylons.decorators import validate

 
.. Using it in your controller is pretty straight-forward: 

コントローラでそれを使用するのはとても簡単です:


.. code-block:: python 

    # in the controller 

    def form(self): 
        return render('/form.mako') 

    @validate(schema=EmailForm(), form='form') 
    def email(self): 
        return 'Your email is: %s' % self.form_result.get('email') 


.. Validation only occurs on POST requests so we need to alter our
.. form definition so that the method is a POST:

バリデーションは POST リクエストのときにだけ起こります。そのため、フォー
ム定義を変更して method を POST にする必要があります:


.. code-block:: mako 

    ${h.form(h.url(action='email'), method='post')} 


.. If validation is successful, the valid result dict will be saved as
.. `self.form_result` so it can be used in the action. Otherwise, the
.. action will be re-run as if it was a GET request to the controller
.. action specified in `form`, and the output will be filled by
.. FormEncode's htmlfill to fill in the form field errors. For simple
.. cases this is really handy because it also avoids having to write
.. code in your templates to display error messages if they are
.. present.

バリデーションが成功すると、バリデーション結果の辞書がアクションで使用
できるように `self.form_result` として保存されます。 さもなければ、アク
ションはまるでそれが `form` で指定されたコントローラアクションへの GET
リクエストであるかのように再実行されるでしょう。そして、その出力は、
FormEncode の htmlfill によってフォームフィールドエラーが埋め込まれます。
簡単なケースでは、テンプレートに (存在しているなら) エラーメッセージを
表示するためのコードを書かなくても済むので、これは本当に便利です。


.. This does exactly the same thing as the example above but works
.. with the original form definition and in fact will work with any
.. HTML form regardless of how it is generated because the validate
.. decorator uses `formencode.htmlfill` to find HTML fields and
.. replace them with the values were originally submitted.

これは上記の例とまさに同じことをします。しかし、それはオリジナルのフォー
ム定義と共に動いています。 validate デコレータは `formencode.htmlfill`
を使用して HTML フィールドを見つけて、それらを元々送信された値に置き換
えているので、事実上 HTML フォームがどのように生成されたかにかかわらず、
それはどんなフォームとも共に動くでしょう。


.. note:: 

    .. Python 2.3 doesn't support decorators so rather than using the
    .. `@validate()` syntax you need to put `email =
    .. validate(schema=EmailForm(), form='form')(email)` after the
    .. email function's declaration.

    Python 2.3 はデコレータをサポートしていません。そのため、
    `@validate()` 構文を使用する代わりに `email =
    validate(schema=EmailForm(), form='form')(email)` を email 関数の宣
    言の後に置く必要があります。


.. Validation the Long Way 

長い方法
-----------------------

.. The `validate` decorator covers up a bit of work, and depending on
.. your needs it's possible you could need direct access to FormEncode
.. abilities it smoothes over.

`validate` デコレータは作業の一部を隠します。そして、必要に応じて隠され
た FormEncode の能力に直接アクセスする必要があるかもしれません。


.. Here's the longer way to use the `EmailForm` schema: 

これは `EmailForm` スキーマを使用するもっと長い方法です:


.. code-block:: python 

    # in the controller 

    def email(self): 
        schema = EmailForm() 
        try: 
            form_result = schema.to_python(request.params) 
        except formencode.validators.Invalid, error: 
            return 'Invalid: %s' % error 
        else: 
            return 'Your email is: %s' % form_result.get('email') 


.. If the values entered are valid, the schema's `to_python()` method
.. returns a dictionary of the validated and coerced
.. `form_result`. This means that you can guarantee that the
.. `form_result` dictionary contains values that are valid and correct
.. Python objects for the data types desired.

入力された値が有効なら、スキーマの `to_python()` メソッドはバリデーショ
ンと型変換 (coerce) された `form_result` の辞書を返します。 これは、
`form_result` 辞書が期待するデータ型に対して有効で正しい Python オブジェ
クトである値を含んでいることを信用できることを意味します。


.. In this case the email address is a string so
.. `request.params['email']` happens to be the same as
.. `form_result['email']`. If our form contained a field for age in
.. years and we had used a `formencode.validators.Int()` validator,
.. the value in `form_result` for the age would also be the correct
.. type; in this case a Python integer.

この場合 E メールアドレスが文字列なので、 `request.params['email']` は
たまたま `form_result['email']` と同じです。 もしフォームが年齢フィール
ドを含んでいて、 `formencode.validators.Int()` バリデータを使用したなら、
年齢に対する `form_result` の値は正しい型になるでしょう。この場合は
Python 整数型です。


.. FormEncode comes with a useful set of validators but you can
.. also easily create your own. If you do create your own
.. validators you will find it very useful that all FormEncode
.. schemas' `.to_python()` methods take a second argument named
.. `state`. This means you can pass the Pylons `c` object into
.. your validators so that you can set any variables that your
.. validators need in order to validate a particular field as an
.. attribute of the `c` object. It can then be passed as the `c`
.. object to the schema as follows:

FormEncode は役に立つバリデータのセットを含んでいますが、独自のバリ
データを作成することも容易にできます。 独自のバリデータを作成する場
合、 FormEncode のすべての schemas の `.to_python()` メソッドが
`state` という2番目の引数を取るのが非常に役に立つことがわかるでしょ
う。これは、バリデータが特定のフィールドをバリデーションするために
必要とするどんな変数も `c` オブジェクトの属性として設定できるように、
Pylons `c` オブジェクトをバリデータに渡すことができることを意味しま
す。そして、以下のようにそれを `c` オブジェクトとしてスキーマに渡す
ことができます:


.. code-block:: python 

    c.domain = 'example.com' 
    form_result = schema.to_python(request.params, c) 


.. The schema passes `c` to each validator in turn so that you can do
.. things like this:

スキーマは `c` を各バリデータに順番に渡すので、このようなことができます:


.. code-block:: python 

    class SimpleEmail(formencode.validators.Email): 
        def _to_python(self, value, c): 
            if not value.endswith(c.domain): 
                raise formencode.validators.Invalid(
                    'Email addresses must end in: %s' % \ 
                        c.domain, value, c) 
            return formencode.validators.Email._to_python(self, value, c) 


.. For this to work, make sure to change the `EmailForm` schema you've
.. defined to use the new `SimpleEmail` validator. In other words,

これが動作するように、定義済みの `EmailForm` スキーマを新しい
`SimpleEmail` バリデータを使用するように変えてください。言い換えれば、


.. code-block:: python 

    email = formencode.validators.Email(not_empty=True) 
    # becomes: 
    email = SimpleEmail(not_empty=True) 


.. In reality the invalid error message we get if we don't enter a
.. valid email address isn't very useful. We really want to be able to
.. redisplay the form with the value entered and the error message
.. produced. Replace the line:

実際には、有効な E メールアドレスを入力しなかった場合に得られる
invalid エラーメッセージはそれほど役に立ちません。入力された値と生成さ
れたエラーメッセージが入ったフォームを再表示したいと思うでしょう。次の
行を、


.. code-block:: python 

    return 'Invalid: %s' % error 


.. with the lines: 

以下のように置き換えてください:


.. code-block:: python 

    c.form_result = error.value 
    c.form_errors = error.error_dict or {} 
    return render('/form.mako') 


.. Now we will need to make some tweaks to `form.mako`. Make it look
.. like this:

次に、 `form.mako` にいくつかの修正をする必要があります。このようにして
ください:


.. code-block:: html+mako 

    ${h.form(h.url(action='email'), method='get')} 

    % if c.form_errors: 
    <h2>Please correct the errors</h2> 
    % else: 
    <h2>Enter Email Address</h2> 
    % endif 

    % if c.form_errors: 
    Email Address: ${h.text_field('email', value=c.form_result['email'] or '')} 
    <p>${c.form_errors['email']}</p> 
    % else: 
    Email Address: ${h.text_field('email')} 
    % endif 

    ${h.submit('Submit')} 
    ${h.end_form()} 


.. Now when the form is invalid the `form.mako` template is
.. re-rendered with the error messages.

これで、フォームが無効なときに `form.mako` テンプレートはエラーメッセー
ジと共に再レンダリングされます。


.. Other Form Tools 

その他のフォームツール
======================

.. If you are going to be creating a lot of forms you may wish to
.. consider using `FormBuild <http://formbuild.org>`_ to help create
.. your forms. To use it you create a custom Form object and use that
.. object to build all your forms. You can then use the API to modify
.. all aspects of the generation and use of all forms built with your
.. custom Form by modifying its definition without any need to change
.. the form templates.

大量のフォームを作成するつもりなら、フォームの作成を補助するために
`FormBuild <http://formbuild.org>`_ を使用することを検討すると良いかも
しれません。 FormBuild を使用するためには、カスタム Form オブジェクトを
作成します。そして、そのオブジェクトを使用してすべてのフォームを作成し
てください。そうすると、カスタム Form の定義を変更することによって、
フォームテンプレートを少しも変更する必要なく、カスタム Form を使って構
築されたすべてのフォームの生成と使用のあらゆる側面を API を使用して変更
することができます。


.. Here is an one example of how you might use it in a controller to
.. handle a form submission:

これは、コントローラでフォーム送信を扱うのに FormBuild をどのように使用
するかに関する 1 つの例です:


.. code-block:: python 

    # in the controller 

    def form(self): 
        results, errors, response = formbuild.handle( 
            schema=Schema(), # Your FormEncode schema for the form 
                             # to be validated 
            template='form.mako', # The template containg the code 
                                  # that builds your form 
            form=Form # The FormBuild Form definition you wish to use 
        )
        if response: 
            # The form validation failed so re-display 
            # the form with the auto-generted response 
            # containing submitted values and errors or 
            # do something with the errors 
            return response 
        else: 
            # The form validated, do something useful with results. 
            ... 

.. Full documentation of all features is available in the `FormBuild
.. manual <http://formbuild.org/manual.html>`_ which you should read
.. before looking at `Using FormBuild in Pylons
.. <http://formbuild.org/pylons.html>`_.

すべての特徴の完全なドキュメンテーションは `FormBuild manual
<http://formbuild.org/manual.html>`_ にあります。それを読んだら、次は
`Using FormBuild in Pylons <http://formbuild.org/pylons.html>`_ を見る
とよいでしょう。


.. Looking forward it is likely Pylons will soon be able to use the
.. TurboGears widgets system which will probably become the
.. recommended way to build forms in Pylons.

将来的には、 Pylons はもうすぐ TurboGears ウィジェットシステムを使用で
きるようになりそうです。それはおそらく Pylons でフォームを構築するお勧
めの方法になるでしょう。
