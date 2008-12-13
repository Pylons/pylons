.. _caching:

=========
Кешування
=========

Неминуче, під час розробки, або розгортання може трапитись таке, що деякі завдання будуть виконуватись велику кількість часу. Коли це станеться, найкращий шлях збільшити швидкодію, це застосувати :term:`caching`. 

Pylons одразу прийшов із можливістю кешування, це є частина того самого пакету `Beaker <http://beaker.groovie.org>`_, який використовується для роботи з сесіями. Також Beaker підримує різноманітні типи кешувань: memory-based, filesystem-based і спеціалізовану `memcached` бібліотеку. 

В Pylons існує декілька шляхів шоб закешувати діні, в залежності де проявляється низька швидкодія:

* Кешування на стороні веб-оглядача - HTTP/1.1 підтримує :term:`ETag` кешування, яке позволяє використовувати власний кеш оглядача, замість того щоб переґенеровувати цілу сторінку заново. ETag-базоване кешування запобігає уникнути повоторної реґенерації вмісту, проте якщо оглядач ніколи не бачив сторінки йому прийдеться зґенерувати її. Так що використання ETag кешування в поєднанні одним із інших типів кешування перерахованих нижче, забезпечить оптимальну продуктивність, і ви уникнуте непотрібних викликів в ресурсомістких операціях.

.. note:: отанній тип кешування може допомогти лише в тому випадку, коли можливо закешувати цілу сторінку.

* Контроллери - `cache` об’єкт є доступний в контроллерах і шаблонах, для кешування будь чого, що Python можна серіалізовати за допомогою pickle. 

* Шаблони - Результат цілого, виконаного шаблону може бути поміщений в кеш, використовуючи `3 аргументи в методі render <http://pylonshq.com/docs/class-pylons.templating.Buffet.html#render>`_. Їх також можна використовувати в середині шаблонів. 

* Mako/Myghty шаблони - вони містять вбудовані опції кешування, детальніше для `Mako <http://www.makotemplates.org/docs/caching.html>`_ і для `Myghty <http://www.myghty.org/docs/cache.myt>`_. Вони дозволяють дрібно-модульне кешування лише певних секцій шаблону, також як і кешування повного шаблону.

Дві основні концепції які треба памятати при роботі з кешем, це те що
i) кеш має *простір імен*
ii) кеш може мати ключі *keys* всередені цього простору імен.
Причина цьому є те, що для якогось одного шаблону, може бути багато версій цього шаблону кожна з яких вимагає її власну закешовану версію. Ключі в просторі імен це є ``версія`` і ім’я шаблону це ``простір імен``. **Обидва ці значення повинні бути Python стрічками.** 

В шаблонах, ``простір імен`` кешу буде автоматично мати назву шаблону який був щойно виконаний. Нічого більше не потрібно для простого кешування, поки розробник не буде бажати контролювати як довго шаблон є в кеші, та/або  мати можливість кешувати різні версії того ж шаблону. 

дивіться також Stephen Pierzchala `Caching for Performance <http://web.archive.org/web/20060424171425/http://www.webperformance.org/caching/caching_for_performance.pdf>`_ (stephen@pierzchala.com)

Використання обєкта cache 
-------------------------

Всередині контроллера буде доступний об’єкт `cache`, котрий можна використовувати. Якщо якась дія або частина коду використовує багато ресурсів, або виконується дуже довго, то може бути доречним закешувати результат. Об’єкт `cache` може закешувати будь яку Python структуру, котра може бути серіалізована за допомогою  `pickle <http://docs.python.org/lib/module-pickle.html>`_. 

Поглянемо на ситуацію, коли бажано закешувати код, який витрачає багато часу/ресурсів та повертає об’єкт, який може бути серіалізований (list, dict, tuple, etc.): 

.. code-block:: python 

    def some_action(self, day): 
        # hypothetical action that uses a 'day' variable as its key 

        def expensive_function(): 
            # do something that takes a lot of cpu/resources 
            return expensive_call()

        # Get a cache for a specific namespace, you can name it whatever 
        # you want, in this case its 'my_function' 
        mycache = cache.get_cache('my_function') 

        # Get the value, this will create the cache copy the first time 
        # and any time it expires (in seconds, so 3600 = one hour) 
        c.myvalue = mycache.get_value(key=day, createfunc=expensive_function, 
                                      type="memory", expiretime=3600)

        return render('/some/template.myt') 

`сreatefunc` опція, вимагає обє’кт або функцію, котру можна би було викликлати, і цей об’єкт або функцію `сache` буде викликати кожного разу, як значення переданого ключа не буде знаходитись в кеші, або термін його придатності буде вичерпаний.

Як бачимо `createfunc` викликається без аргументів, тому ресурсо/часо-затратна функція відповідно також не повинна вимагати жодного аргументу.

Інші опції кешування 
^^^^^^^^^^^^^^^^^^^^

Також cache підтримує видалення певних значень, використовуючи ключі як ідентифікатори значень які потрібно видалити, і також підримує очищення кеш-пам’яті повністю, якщо її потрібно скинути.

.. code-block:: python 

    # Clear the cache 
    mycache.clear() 

    # Remove a specific key 
    mycache.remove_value('some_key') 


Використання кеш параметрів в команді `render` 
----------------------------------------------

.. warning:: Цей розділ не описує специфічних викликів render_*, представлених у версії Pylons 0.9.7

Всі команди `render` мають вбудовану функціональність для роботи з кешем. Шоб її використовувати, просто
додайте відповідний параметр в виклику `render`. 

.. code-block:: python 

    class SampleController(BaseController): 

        def index(self): 
            # Cache the template for 10 mins 
            return render('/index.myt', cache_expire=600) 

        def show(self, id): 
            # Cache this version of the template for 3 mins 
            return render('/show.myt', cache_key=id, cache_expire=180) 

        def feed(self): 
            # Cache for 20 mins to memory 
            return render('/feed.myt', cache_type='memory', cache_expire=1200)

        def home(self, user): 
            # Cache this version of a page forever (until the cache dir
            # is cleaned)
            return render('/home.myt', cache_key=user, cache_expire='never') 


Використання Кеш Декоратора 
---------------------------

Pylons також постачає `beaker_cache 
<http://pylonshq.com/docs/module-pylons.decorators.cache.html#beaker_cache>`_ 
декоратор для кешування в `pylons.cache` рузльтатів, які повертає певна функція(memoizing).

.. warning:: ambiguous with respect to 'as does the render function'

Кеш декоратор використовує тіж самі кеш аргументи (не включаючи `cache_` префіксу), котрі приймає функція `render`.

.. code-block:: python 

    from pylons.decorators.cache import beaker_cache 

    class SampleController(BaseController): 

        # Cache this controller action forever (until the cache dir is
        # cleaned)
        @beaker_cache() 
        def home(self): 
            c.data = expensive_call() 
            return render('/home.myt') 

        # Cache this controller action by its GET args for 10 mins to memory
        @beaker_cache(expire=600, type='memory', query_args=True) 
        def show(self, id): 
            c.data = expensive_call(id) 
            return render('/show.myt') 

По замовчуванню, декоратор використовує суміш усіх параметрів функції яку він декорує як ключ кешу. Як альтернатива він може використовувати суміш `request.GET` аргументів як ключ кешу, якщо `query_args` опція включена. 

.. warning:: Двозначність. Чи опція `query_args`, додає дані для генерації ключа чи замінює його?

Ключ кешу пізніше може бути змінений використовуючи аргумент `key`. 

ETag кешування 
--------------

Використання кешування ETag, зумовлює відсилання веб-оглядачу хедера ETag, щоб він бачив що повинен зберегти і при можливості використовувати закешовану копію сторінки з його власного кешу, замість того щоб посилати запит для отримання свіжої копії.

Оскільки ETag кеш зумовлює відсилання веб-оглядачу хедера ETag, то це працює трохи в іншому стилі ніж механізми описані вище.

Функція :func:`etag_cache` встановлює належні HTTP хедери якшо веб-оглядач ще не має копії сторінки. Інакше, буде згенерована
виняткова ситуація 304 HTTP, яку буде оброблено проміжним кодом Paste і повернуто веб-оглядачу як належну 304-ту відповідь. Це буде мотивом щоб викорстовувати вашим веб-оглядачем, локальну закешовану копію.

:func:`etag_cache` повертає `pylons.response` for legacy purposes
(`pylons.response` should be used directly instead).

ETag базоване кешування вимагає єдиного ключа який посилається в ETag HTTP хедері назад до веб-оглядача. `RFC специфікація для HTTP headers <http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html>`_ вказує на те що 
ETag хедер просто повинен бути стрічкою. Значення цієї стрічки не не обовязково повинне бути унікальним для кожної URL адреси, оскільки веб оглядач сам визначає чи використовувати його власну копію чи ні, це рішення базується на URL адресі і на ETag ключі. 

.. code-block:: python 

    def my_action(self): 
        etag_cache('somekey') 
        return render('/show.myt', cache_expire=3600) 

Або змініть інші частини відповіді: 

.. code-block:: python 

    def my_action(self): 
        etag_cache('somekey') 
        response.headers['content-type'] = 'text/plain' 
        return render('/show.myt', cache_expire=3600) 

.. note:: 
    В цьому  прикладі ми вокиростовуємо кешування шаблонів в додаток до ETag
    кешування. Якщо на цю сторінку зайде новий відвідувач, ми уникнемо
    повторного виконання шаблону, у випадку якшо закешована копія вже існує
    and repeat hits to the page by that user
    will then trigger the ETag cache. Цей приклад ніколи не міняє
    ETag ключа, так що завжди буде використовуватись кеш веб-оглядача, якщо він вже має закешовану копію.

Частота з якою ключ ETag кешу буде змінюватись, залежитиме від веб програми, і рішення розробника про те як часто веб оглядач повинен робити запит для отримання чистої копії сторінки.


.. warning:: Вкрадено в Philip Cooper's `OpenVest wiki <http://www.openvest.com/trac/wiki/BeakerCache>`_  після чого це було редаговано і оновлено...

Всередині Beaker кешу
---------------------

Кешування
^^^^^^^^^

Спочатку почнемо з **повільної** функції яку ми бажаємо закешувати. Насправді ця функція не є повільною, проте вона покаже нам коли вона буде закешована так що ми зможемо побачити що все працює так як ми очікували:

.. code-block:: python

    import time
    def slooow(myarg):
      # some slow database or template stuff here
      return "%s at %s" % (myarg,time.asctime())

Коли ми маємо закешовану функцію, множинні виклики скажуть нам чи ми бачимо закешовану чи нову версію.

DBMCache
^^^^^^^^

DBMCache зберігає (наспарвді серіалізує) результат в базі даних dbm стилю.

Те що може бути тут не очевидним, так це те що тут є два ступені ключів. Вони по суті створені, один для функції або імені шаблону (називається namespace) і другий для ''ключів''(називається ключ).  Так що для `Деяка_назва_функціїї`, створюється кеш як один файл/база даних.  Якщо функція викликається з різними аргументами, ці аргументи є ключами в dbm файлі. Спочатку створимо і заповнимо кеш. Цей кеш може бути кешом для `Деяка_назва_функціїї` яка викликається три рази з трьома різними аргументами: `x, yy, і zzz`:

.. code-block:: python

    from beaker.cache import CacheManager
    cm = CacheManager(type='dbm', data_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed 
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)

Нічого особливо нового тут нема. Тепер як ми маємо кеш, ми можем його використовувати як написано в Beaker документації.

.. code-block:: python

    import beaker.container as container
    cc = container.ContainerContext()
    nsm = cc.get_namespace_manager('Some_Function_name',
                                   container.DBMContainer,data_dir='beaker.cache')
    filename = nsm.file

Тепер ми маємо назву файла. Назва файла це `sha` хеш стрічки, яка складається з  ім’я класу контейнера і ім’я функції (яка вказувалась в виклику `get_cache`).  Вона буде виглядати щось на подобі цього:


.. code-block:: python

    'beaker.cache/container_dbm/a/a7/a768f120e39d0248d3d2f23d15ee0a20be5226de.dbm'

Маючи назву файла можна напряму глянути в базуданих (але лише для інтересу або відлагодження, **не** для роботи з кешем!)

.. code-block:: python

    ## this file name can be used directly (for debug ONLY)
    import anydbm
    import pickle
    db = anydbm.open(filename)
    old_t, old_v = pickle.loads(db['zzz'])

База даних містить лише old time і old value. Де знаходиться час закінчення дійсності і функція для створення/оновлення значення? Вони ніколи і не мали бути в базі даних. Зате знаходяться в `cache` об’єкті, який повернув метод `get_cache`.  

Майте на увазі, що createfunc, і час закінчення дійсності кешу зберігаються під час першого виклику `get_value` функції. Наступні виклики, з іншим значенням часу **не** оновлять цього значення.  This is a tricky part of the caching but perhaps is a good thing since different processes may have different policies in effect.

Якщо виникають якісь проблеми з цими значеннями, завжди памятайте один виклик :func:`cache.clear`, який все скидає.

Кеш в базі даних
^^^^^^^^^^^^^^^^

Використання типу кеша `ext:database`.

.. code-block:: python

    from beaker.cache import CacheManager
    #cm = CacheManager(type='dbm', data_dir='beaker.cache')
    cm = CacheManager(type='ext:database', 
                      url="sqlite:///beaker.cache/beaker.sqlite",
                      data_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed 
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)


Робота з цим кешем точно така сама як і з поданим вище, за однієї лише відмінності, в створенні `CacheManager`. Набагато простоіше переглядати кеші ззовні  beaker коду (знову ж таки тільки для навчання і для відлагодження, не для використання).

В нашому випадку ми використовуємо SQLite базу даних, прямий доступ до файла даних котрої, можна отримати використовуючи консольну SQLite прогаму або задопомогою плаґіна до Firefox:

.. code-block:: text

    sqlite3 beaker.cache/beaker.sqlite
    # from inside sqlite:
    sqlite> .schema
    CREATE TABLE beaker_cache (
            id INTEGER NOT NULL, 
            namespace VARCHAR(255) NOT NULL, 
            key VARCHAR(255) NOT NULL, 
            value BLOB NOT NULL, 
            PRIMARY KEY (id), 
             UNIQUE (namespace, key)
    );
    select * from beaker_cache;

.. warning:: Сруктура даних в Beaker 0.8 є іншою...

.. code-block:: python

    cache = sa.Table(table_name, meta,
                     sa.Column('id', types.Integer, primary_key=True),
                     sa.Column('namespace', types.String(255), nullable=False),
                     sa.Column('accessed', types.DateTime, nullable=False),
                     sa.Column('created', types.DateTime, nullable=False),
                     sa.Column('data', types.BLOB(), nullable=False),
                     sa.UniqueConstraint('namespace')
    )


Це включає час доступу, але зберігає рядки on a one-row-per-namespace basis, (зберігаючи серіалізований dict) а не один рядок на одне середовище імен чи ключ. Це є більш ефективний підхід коли потрібно обробляти велику кількість середовищ імен з обмеженою кількістю ключів.

Memcached Кеш
^^^^^^^^^^^^^

Для великої кількості ключів і коли дуже дорогий час їх пошуку, сам раз використати memcached кеш.

Якщо memcached є запущений на порті 11211 котрий є по замовчуванню:

.. code-block:: python

    from beaker.cache import CacheManager
    cm = CacheManager(type='ext:memcached', url='127.0.0.1:11211',
                      lock_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed 
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)
