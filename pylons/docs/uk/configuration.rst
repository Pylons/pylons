.. _configuration:

============
Конфіґурація
============

В Pylons є два шляхи щоб сконфіґурувати програму:

* Конфіґураційни файл (:ref:`run-config`)
* Каталог ``config`` в вашій програмі

Файли в каталозі ``config`` змінють певні аспекти в поведінці вашої програми. любі опції які вебмайстру прийдеться міняти під час розгортання, повинні бути визначені в конфіґураційному файлі.

.. tip::
    Хорошим індикатором в якому випадку пторібно використовувати ``config`` каталог, а в якому конфіґураційни файл, є те чи дана опція є обовязковою для функціонування програми чи ні. Якщо програма не буде працювати без даної опції, дана опція повинна бути визначена в файлі :file:`config/` каталога. Якщо опція повинна бути змінена під час розгортання програми, її потрібно визначити в :ref:`run-config` файлі.

Каталог :file:`config/` вашої програми включає:

* :file:`config/environment.py` описується в :ref:`environment-config`
* :file:`config/middleware.py` описується в :ref:`middleware-config`
* :file:`config/routing.py` описується в :ref:`url-config`

Кожен з цих файлів дозволяє розробникикам міняти ключові аспекти в поведінці програми.
 
.. _run-config:

********************
Runtime Конфіґурація
********************

Коли ви створюєте новий проект, файл з назвою :file:`development.ini` автоматично створюється з усіма іншими файлами проекту. Цей конфіґураційний файл містить опції для використання під час розробки, наприклад дуже зручно під час розробки отримувати звіт про помилку кожного разу як вона трапляється. Даний :file:`development.ini` файл містить опції, які включають режим відлагодження, так що помилки починають відображатись.

Оскільки конфігураційний файл використовується для визначення того, які додатки запускати, багато конфіґураційних файлів можна використовувати для того щоб легко переключатись між різними наборами опцій. Типово розробник може мати ``development.ini`` кнфоґураційний файл для тестування, і ``production.ini`` файл створений командою :command:`paster make-config` for testing the command produces sensible production output. Також в проект включаєься :file:`test.ini` конфіґураційний файл, для специфічних для тестування опцій.

Щоб вказати конфіґураційний файл який буде використовуатись під час виконння програми, змініть останню частину команди :command:`paster serve` включивши потрібний конфіґураційний файл:

.. code-block :: bash 

    $ paster serve production.ini

.. seealso::
    Формат конфіґураційного файлу **і його опції** описані дуже детально в `Paste Deploy документації <http://pythonpaste.org/deploy/>`_.


Отримання інформації з конфіґураційного файлу
=============================================

Вся інформація з конфіґураційного файла є доступна в ``pylons.config`` обє’кті. Також даний об’єкт містить конфігурацію, яка визначена в :file:`config.environment` модулі, вашого проекту. 

.. code-block :: python

    from pylons import config 

``pylons.config`` поводиться як python словник. Для прикладу, якщо конфіґураційний файл містить записи всередині ``[app:main]`` блоку:

.. code-block :: ini

    cache_dir = %(here)s/data

Тоді ці дані можуть бути прочитані в коді вашої програми:

.. code-block :: python

    from pylons import config 
    cache_dir = config['cache_dir']

Або статус відлагодження, як це: 

.. code-block :: python 

    debug = config['debug']

Обробка не текстових даних в конфіґураційних файлах
---------------------------------------------------

По замовчуванню, всі значення вконфіґураційному файлі розглядаються як стрічки тексту.
Щоб легко оперувати булевими значеннями, Paste бібіліотека містить функцію яка конвертує
``true`` і ``false`` в правильні булеві значення:

.. code-block :: python
    
    from paste.deploy.converters import asbool
    
    debug = asbool(config['debug'])

Такий підхід вже використовується в :ref:`middleware-config` проекту по замовчуванню  щоб вказати middleware, яке повинно працювати лише в режимі відлагодження, потрібно встановити опцію ``debug`` в ``true``.


Production Крнфіґураційні файли
===============================

Щоб вказати змінні по замовчуванні в конфіґураційному INI файлі, які повинні використовуватись під час розгортання вашої програми, відредагуйте файл :file:`config/deployment.ini_tmpl`. Цей файл буде використовуватись як шаблон під час розгортання програми, так що людина яка буде провдити розгортання буде мати встановлений мінімальний набіор опцій які вимагає ваша програма.

Одна з най більш важливих опцій яку потрібно зімнити це ``debug = true`` опція. Також email опції повинні бути правильно встановленні, так що помилки будуть відправлятись відповідному розробнику чи веб майстру, у випадку коли вони будуть виникати.

Ґенерація Production конфіґурації
---------------------------------------

Щоб зґенерувати production.ini файл з :file:`config/deployment.ini_tmpl` файла, він спочатку повинен бути встановлений як :term:`egg` or under development mode. Якщо вважати що назва вошої Pylons програми є ``helloworld``, виконайте:

.. code-block :: bash

    $ paster make-config helloworld production.ini

.. note::
    Дана команда також буде працювати всередині проекту під час його розробки.

Вся відповідальність лягає на розробника, який повинен бути впевненим що всі потрібні типові конфіґураційні значення існують коли він виконує ``paster make-config`` команду. 

.. warning::
    **Завжди** перевіряйте чи значення ``debug`` встановлене в ``false``, коли ви розгортаєте Pylons програму.


.. _environment-config:

**********
Середовище
**********

Модуль :file:`config/environment.py` встановлює базові змінні середовища Pylons,
які потрібні для запуску програми. Кожен об’єкт, який встановлюється один раз для всієї програми
повинен бути встановлений тут, або в
:file:`lib/app_globals` :meth:`__init__.py` методі.

Він також викликає :ref:`url-config` функцію, щоб встановити як URL адреси будуть відповідати :ref:`controllers`, створює :term:`app_globals`
об’єкт, визначає на який модуль буде ссилатись :term:`h`, і визначає де встановлений двигун шаблонів.

Коли ви використовуєте SQLAlchemy, ми рекомендуємо щоб він був встановлений в цьому модулі. Типова SQLAlchemy конфіґурація з якою постачається Pylons, створює тут двигун який потім використовується в :file:`model/__init__.py`.


.. _url-config:

****************
URL Конфіґурація
****************

Python бібілотека Routes, обробляє приєднані до контроллерів і їніх методів URL адреси, або їх :term:`action` як Routes що посилаються на них. По замовчуванню, Pylons встановлює наступні  :term:`route`\s (які знаходяться в :file:`config/routing.py`):

.. code-block:: python

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

.. versionchanged:: 0.9.7
    Prior to Routes 1.9, all map.connect statements required variable parts
    to begin with a ``:`` like ``map.connect(':controller/:action')``. This
    syntax is now optional, and the new ``{}`` syntax is recommended.

Any part of the path inside the curly braces is a variable (a `variable part`
) that will match
any text in the URL for that 'part'. A 'part' of the URL is the text between
two forward slashes. Every part of the URL must be present for the
:term:`route` to match, otherwise a 404 will be returned.

Подані тут шляхи транслюються Routes бібліотекою в регулярні вирази
щоб забезпечити високу швидкодію в сівпадінні URL адрес. По замовчуванню, всі частини змінних (за винятком
спеціального випадка ``{controller}``) співпадають регулярному виразу ``[^/]+``, що відпоідає любому символу окрім зворотнього слеша. це можна легко змінити,
наприклад щоб частині ``{id}`` співпадали лише цифри:

.. code-block :: python
    
    map.connect('/{controller}/{action}/{id:\d+}')

Якщо регулярний вираз містить ``{}``, далі потрібно вказати змінну для даної частини. Щоб обмежити ``{id}``, щоб він відповідав лише 2 або 4 цифрам:

.. code-block :: python
    
    map.connect('/{controller}/{action}/{id}',  requirements=dict(id='\d{2,4}'))

Контроллер і action також можуть бути вказані як аргументи, так що тоді не потрібно включати їх в URL адресу:

.. code-block :: python
    
    # Archives by 2 digit year -> /archives/08
    map.connect('/archives/{year:\d\d}', controller='articles',  action='archives')

Люба змінна, або аргумент в операторі ``map.connect`` будуть доступні для використання в action. Наприклад для вищенаведеного маршруту:

.. code-block :: python
    
    class ArticlesController(BaseController):
        def archives(self, year):
            # etc.

Частина в URL адресі, яка співпала як рік, є доступна по імені в аргументі функціїї.

.. note::
    Routes також містять можливість мінімізації URL адерси. Цей режим в загальному не є дуже інтиютивним, і починаючи з Pylons 0.9.7 є по замовчуванню виключеним за допомогою  ``map.minimization=False`` опції.

The default mapping can match to any controller and any of their
actions which means the following URLs will match:

.. code-block:: text

    /hello/index       >>    controller: hello, action: index
    /entry/view/4      >>    controller: entry, action: view, id:4
    /comment/edit/2    >>    controller: comment, action: edit, id:2

This simple scheme can be suitable for even large applications when complex URL's aren't needed.

Controllers can be organized into directories as well. For example, if the admins should have a separate ``comments`` controller:

.. code-block:: bash
    
    $ paster controller admin/comments

Will create the ``admin`` directory along with the appropriate ``comments``
controller under it. To get to the comments controller:

.. code-block:: text
    
    /admin/comments/index    >>    controller: admin/comments, action: index

.. note::
    The ``{controller}`` match is special, in that it doesn't always stop
    at the next forward slash (``/``). As the example above demonstrates,
    it is able to match controllers nested under a directory should they
    exist.

Adding a route to match ``/``
=============================

The controller and action can be specified directly in the :meth:`map.connect`
statement, as well as the raw URL should be matched.

.. code-block:: python

    map.connect('/', controller='main', action='index')

will result in ``/`` being handled by the ``index`` method of the ``main``
controller.

Ґенерація URL адрес
===================

URL адреси можуть бути зґенеровані використовуючи допоміжний метод :func:`~routes.util.url`, який по замовчуванню в проекті Pylons буде в глобальній змінній :data:`url`.
Аргументи що вказують на використання контроллера або action, можуть бути прописані всередині:

.. code-block:: python
    
    # generates /content/view/2
    url(controller='content', action='view', id=2)  

Всередині шаблонів, контроллерів і інших змінних очевидно буде краще перейти до використання ґенераціїї URL адрес. Це належить до `Routes memory <http://routes.groovie.org/manual.html#route-memory>`_ і може бути вимкнено, вказавши контроллер з ``/`` на початку:

.. code-block:: python

    # ALWAYS generates /content/view/2
    url(controller='/content', action='view', id=2)   


.. seealso::

    `Routes manual <http://routes.groovie.org/manual.html>`_
    Full details and source code.


.. _middleware-config:

**********
Middleware
**********

A projects WSGI stack should be setup in the :file:`config/middleware.py`
module. Ideally this file should import middleware it needs, and set it up
in the `make_app` function.

The default stack that is setup for a Pylons application is described in
detail in :ref:`wsgi-middleware`.

Default middleware stack:

.. code-block :: python

    # The Pylons WSGI app
    app = PylonsApp()
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])

    # Establish the Registry for this application
    app = RegistryManager(app)

    # Static files (If running in production, and Apache or another web 
    # server is handling this static content, remove the following 3 lines)
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, javascripts_app, app])
    return app
    
Since each piece of middleware wraps the one before it, the stack needs to be
assembled in reverse order from the order in which its called. That is, the
very last middleware that wraps the WSGI Application, is the very first that
will be called by the server.

The last piece of middleware in the stack, called Cascade, is used to
serve static content and JavaScript files during development. For top
performance, consider wrapping the line that wraps the app with
Cascade in an if block that checks to see if ``debug`` is set to true.
Then have the webserver or a :term:`CDN` serve static files.

.. warning::

    When unsure about whether or not to change the middleware, **don't**. The
    order of the middleware is important to the proper functioning of a
    Pylons application, and shouldn't be altered unless needed.

Adding custom middleware
========================

Custom middleware should be included in the :file:`config/middleware.py` at
comment marker::

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)

For example, to add a middleware component named `MyMiddleware`,
include it in :file:`config/middleware.py`::

    # The Pylons WSGI app
    app = PylonsApp()
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    app = MyMiddleware(app)
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
The app object is simply passed as a parameter to the `MyMiddleware` middleware which in turn should return a wrapped WSGI application.

Care should be taken when deciding in which layer to place custom
middleware. In most cases middleware should be placed between the
Pylons WSGI application instantiation and the Routes middleware; however,
if the middleware should run *before* the session object or routing is handled::

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    
    # MyMiddleware can only see the cache object, nothing *above* here
    app = MyMiddleware(app)
    
    app = CacheMiddleware(app, config)

What is full_stack?
===================

In the Pylons ini file {:file:`development.ini` or :file:`production.ini`} this block determines if the flag full_stack is set to true or false::

    [app:main]
    use = egg:app_name
    full_stack = true

The full_stack flag determines if the ErrorHandler and StatusCodeRedirect is included as a layer in the middleware wrapping process. The only condition in which this option would be set to `false` is if multiple Pylons applications are running and will be wrapped in the appropriate middleware elsewhere.


.. _setup-config:

*****************
Application Setup
*****************

There are two kinds of 'Application Setup' that are occasionally referenced
with regards to a project using Pylons.

* Setting up a new application
* Configuring project information and package dependencies

Setting Up a New Application
============================

To make it easier to setup a new instance of a project, such as setting up
the basic database schema, populating necessary defaults, etc. a setup
script can be created.

In a Pylons project, the setup script to be run is located in the projects'
:file:`websetup.py` file. The default script loads the projects configuration
to make it easier to write application setup steps:

.. code-block :: python
    
    import logging

    from helloworld.config.environment import load_environment

    log = logging.getLogger(__name__)

    def setup_app(command, conf, vars):
        """Place any commands to setup helloworld here"""
        load_environment(conf.global_conf, conf.local_conf)

.. note::
    If the project was configured during creation to use SQLAlchemy this file
    will include some commands to setup the database connection to make it
    easier to setup database tables.

To run the setup script using the development configuration:

.. code-block :: bash
    
    $ paster setup-app development.ini

Configuring the Package
=======================

A newly created project with Pylons is a standard Python package. As a Python
package, it has a :file:`setup.py` file that records meta-information about
the package. Most of the options in it are fairly self-explanatory, the most
important being the 'install_requires' option:

.. code-block :: python
    
    install_requires=[
        "Pylons>=0.9.7",
        "Mako",
    ],
    
These lines indicate what packages are required for the proper functioning
of the application, and should be updated as needed. To re-parse the
:file:`setup.py` line for new dependencies:

.. code-block :: bash

    $ python setup.py develop

In addition to updating the packages as needed so that the dependency
requirements are made, this command will ensure that this package is active
in the system (without requiring the traditional
:command:`python setup.py install`).

.. seealso::
    `Declaring Dependencies <http://peak.telecommunity.com/DevCenter/setuptools#declaring-dependencies>`_
