.. _controllers:

===========
Контролери
===========

.. image:: _static/pylon2.jpg
   :alt: 
   :align: left
   :height: 450px
   :width: 368px

В парадигмі :term:`MVC`, *controller* інтерпритує ввід, який керується моделю чи/або 
виглядом( view в патерні MVC) для відповідних змін. В Pylons ця концепція злегка розширена,
а саме в тому що контролери Pylons не прямо взємодіють з  запитом клієнта, а діють так 
щоб визначити правильний шлях збирання даних із моделі і відобразити їх правильним шаблоном.

Контролери інтерпрритують запит від користувача і викликають частину моделі і частину
відображення, як небхідність виконання запиту.

Pylons використовує клас, батьківський клас якого забезпечує інтерфейс :term:`WSGI`,
а породжений клас імплементовує специфічну для застосування логіку контролера.

Pylons WSGI Controller обробляє вхідні веб запити, надіслані PylonsBaseWSGIApp.

Результат запиту створюється у новій змінній  WSGIController, яку потім викликано з dict опцією із відпвідності Маршрутів. Потім повертається стандартна WSGI відповідь за допомогою
виклику start_response.

Так як Pylons контролери фактично викликаються через WSGI інтерфейс, звичайна
WSGI програма також може бути Pylons ‘controllers’. 

Стандартні Контролери
=====================

Стандартні контролери призначені для наслідування веб розробниками. 

Зберігання методів приватними
-----------------------------

Так як звичайний маршрут проектуватиме будь який контролер і подію, ви
ймовірно захочите заборонити виклик деяких методів контролера із URL.

За замовчуванням маршрути використовують Python конвеншн приватних методів,
починаючи їх з ``_``. Щоб приховати метод ``edit_generic`` у цьому класі, просто
змінити імя, починаючи його із ``_`` буде достатньо.

.. code-block:: python

	class UserController(BaseController):
		def index(self):
			return Response("This is the index.")
	
		def _edit_generic(self):
			"I can't be called from the web!"
			return True

Спеціальні методи
-----------------

Спеціальні методи контролера, які ви можите визначити:

``__before__``
    Цей метод виконається перед настанням вашої події, і повинен 
    використовуватись для ініціалізації змінних/обєктів, обмежуючи доступ до
    інших подій, або інших завдань, які мають виконатися перед
    даною подією.

``__after__``
    Метод, який працюватиме після того, як дія виконається. Цей метод 
    *завжди* працюватиме після вашого методу, навіть якщо він спричинить 
    виняткову ситуацію чи редірект.
	
Додавання контролерів динамічно
-------------------------------

Програма може додати контролери без перезавантаження. Потрібно сказати Маршрутам повторно проглянути каталог контролерів.

Нові контролери можна додати з командного рядка за допогою команди paster (рекомедовано, оскільки одразу створюється файл використання тестів),
або будь-яким іншим засобом створення файлу контролера.

Для того щоб Маршрути взнали, що є нові контролери в каталозі контролерів, піднято внутрішній прапорець,
що вказує, що Маршрути повинні повторно проглянути каталог:

.. code-block:: python

    from routes import request_config

    mapper = request_config().mapper
    mapper._created_regs = False
	
На наступному запиті, Маршрути переглянуть каталог контролерів, і ті маршрути, які використовують
``:controller`` динамічну частину шляху, зможуть підібрати нового контролера.
	

Attaching WSGI apps
-------------------

.. note::

	Для використання цього методу потрібна базова обізнаність із WSGI Specification (PEP 333)

WSGI виконується повністю через Pylons і присутня у багатьох частинах архітетури. Так як контролери Pylons викликаються
фактично із WSGI інтерфейсом, звичйна WSGI програма також може бути Pylons 'controllers'.

Дадотково, якщо повну програму WSGI потрібно змонтувати і обробити залишок URL, Маршрути можуть автоматично модифікувати правильну частину 
URL у :envvar:`SCRIPT_NAME`,так  що WSGI програма може коректно обробити свою  :envvar:`PATH_INFO` частину.

Цей метод демонструватиме додавання базової WSGI програми як Pylons контролера.

Створіть новий контролер файл у вашому каталозі проекту Pylons:

.. code-block:: python

    paster controller wsgiapp

Це налаштує базовий імпорт який може вам знадобитися використовуючи інші WSGI програми.

Відредагуйте свого контролера, так щоб він виглядав ось так:

.. code-block:: python

    import logging

    from YOURPROJ.lib.base import *

    log = logging.getLogger(__name__)

    def WsgiappController(environ, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ["Hello World"]

Коли підєднюватимите інші програми WSGI, вони очікуватимуть частину URL, ту що використоувалась для
доступу до цього контролера, для того щоб перемістити її у :envvar:`SCRIPT_NAME`.
 :mod:`Routes`, може коректно реголювати environ, якщо мапу маршруту для цього контролера додано до файлу file:`config/routing.py`:

.. code-block:: python

    # CUSTOM ROUTES HERE

    # Map the WSGI application
    map.connect('wsgiapp/*path_info', controller='wsgiapp')

Визначаючи динамічний шлях ``path_info``, Маршрути будуть класти усе що передує ``path_info`` у :envvar:`SCRIPT_NAME`,
а решта буде йти у :envvar:`PATH_INFO`.

.. warning::

   Чи це все ще правда про Routes 2?


Використання Контролера WSGI для забезпечення WSGI сервісу
==========================================================

Pylons WSGI Контролер
--------------------------

Власний Pylons' WSGI Controller наслідує WSGI специфікацію для виклику і повернення значень

Pylons WSGI Controller обробляє вхідні веб-запити, відпраленні від ``PylonsBaseWSGIApp``.
Ці запити утворюють нову змінну ``WSGIController``, яка потім виклакається із dict опцією з
відбору Маршрутів. Стандартна WSGI відповідь потім повертається з :meth:`start_response`,
визваної відповідно до специфікації WSGI.


Методи WSGIController 
---------------------

Спеціальні методи WSGIController, які ви можите визначити 

``__before__``
    Цей метод виконається перед настанням вашої події, і повинен 
    використовуватись для ініціалізації змінних/обєктів, обмежуючи доступ до
    інших подій, або інших завдань, які мають виконатися перед
    даною подією.

``__after__``
    Метод, який працюватиме після того, як дія виконається. Цей метод 
    *завжди* працюватиме після вашого методу, навіть якщо він спричинить 
    виняткову ситуацію чи редірект.

Кожна дія, яку буде викликано, перевіряється за допомогою 
:meth:`_inspect_call`. так що вона передає лише ті аргументи у вибірку словника Маршрутів, які
вимагаються . Аргументи, які передані в подію можуть бути налаштованні, перевизначаючи функцію 
:meth:`_get_method_args`, яка повинна повернути словник.

У випадку якщо дії для обробки певного запиту не знайдено, Контроллер буде повертати помилку "Action Not Found" режимі відлагодження, інакше буде повернута помилка ``404 Not Found``.
 
.. _rest_controller:

Використання Контролера REST разом із RESTful API
=================================================

Виористання шаблону paster restcontroller
-----------------------------------------

.. code-block:: bash

    $ paster restcontroller --help

Створення REST контролера і супровідного фунціонального тесту

Команда RestController створить REST-базований Controller файл для використння із :meth:`~routes.base.Mapper.resource`.
REST-базованою дисптчиризацією. Цей шаблон містить метод, який :meth:`~routes.base.Mapper.resource` диспатчить у додаткову
стрічку документацї для зястосування, де метод буде викликано.

Перший аргумент повинен бути формою однини ресурсу REST. Другий аргументє формою множинни слова.
Якщо це вкладений контролер, розмістіть інформацію про каталог спереду як показано у наступному прикладі нижче:

Example usage:

.. code-block:: bash

    yourproj% paster restcontroller comment comments
    Creating yourproj/yourproj/controllers/comments.py
    Creating yourproj/yourproj/tests/functional/test_comments.py

Ящо ви бажаєте мати контролер внизу директорії,
просто включіть шлях, як ім’я контролера і потрібні вам каталоги будуть створенні для вас:

.. code-block:: bash

    yourproj% paster restcontroller admin/tracback admin/trackbacks
    Creating yourproj/controllers/admin
    Creating yourproj/yourproj/controllers/admin/trackbacks.py
    Creating yourproj/yourproj/tests/functional/test_admin_trackbacks.py

	
Контролер атомного стилю REST для користувачів
----------------------------------------------

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
            if format=='json':
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
                      headers=[('location', 
                                 url('user', id=user.name)), ])
            else:
                try:
                    # Validate the data that was sent to us
                    params = model.forms.UserForm.to_python(request.params)
                except Invalid, e:
                    # Something didn't validate correctly
                    abort(400, '400 Bad Request -- '+str(e))
                user = model.User(**params)
                model.objectstore.flush()
                response.headers['location'] = \
                    url('user', id=user.name)
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
                if (old_name != new_name) and \
                        model.User.get_by(name=new_name):
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
                              [('Location', 
                                url('users', id=user.name)),])
                    else:
                        return ''

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
            return ''

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

Використання Контролера Xml-Rpc для запитів Xml-Rpc
===================================================

Для того щоб розгорнути цей контролер вам необхідне як мінімум швидкоплинне знайомство із Xml-Rpc
Ми спочатку розглядатимемо основи Xml-Rpc а потім опишемо роботу ``Pylons XMLRPCController``. Зрештою, ми покажемо приклад як використовувати
контролер для написання простого веб сервісу.

Після того, як ви прочитали цей документ, ви, можливо, зацікаитесь в читанні супровідного документа: "A blog publishing web service in XML-RPC" ,
який продовжує тему, покриваючи деталі MetaWeblog API ( відомого XML-RPC сервісу) і, демонструє як сконструювати деякі основні сервісні методи,
щоб поводитись як базовий MetaWeblog blog видавничий сервіс. 

Коротке введення в Xml-Rpc
--------------------------

Xml-Rpc - специфікація, яка описує інтерфейс Віддаленої Процедури Виклику (RPC), програма може
використовувати Інтернет щоб виконувати вказаний виклик процедури на віддаленому сервері Xml-Rpc. 
Імя процедури, яку буде викликано і будь-які значення обов'язкових параметрів "розміщенні" у XML.
Xml формує тіло POST запиту, який послається через HTTP до XML-RPC сервера .
На сервері процедура виконується, поверненені значення  розміщують в Xml і посилають назад програмі.
XML-RPC призначений бути одначасно і простим, і також дозволяти передавати, обробляти і повертати складні структури даних.
	
XML-RPC Котролер, що говорить WSGI 
----------------------------------

Pylons використовує власну бібліотеку xmlrpclib, щоб надати
спеціалізований клас :class:`XMLRPCController` , який дає повний діапазон засобів самоаналізу XML-RPC для
використання у ваших методах сервісу і забезпечує основу для побудови множини спеціалізованих методів
сервісу. Ці методи надають корисний веб сервіс --- такий як інтерфейс опублікування блогу. 

Ці контролери обробляють XML-RPC відповіді і поводяться відповідно до  `XML-RPC Specification <http://www.xmlrpc.com/spec>`_ 
так само добре як із `XML-RPC Introspection <http://scripts.incutio.com/xmlrpc/introspection.html>`_ специфікацією.

Частиною  базової функціональності XML-RPC сервера є  надання трьох стандартних процедур самоаналізу або
по-іншому "service methods". Клас Pylons :class:`XMLRPCController` надає ці стандартні методи
готовими для вас.

* :meth:`system.listMethods` Повертає список  XML-RPC методів для цього XML-RPC ресурсу 
* :meth:`system.methodSignature` Повертає масив масивів для валідного підпису методу. Перше значення кожного масиву є значення, яке цей метод повертає. Результатом є масив щоб вказати множинні підписи, що метод може мати. 
* :meth:`system.methodHelp` Повертає документацію методу 

За замовчуванням, методи з іменнем, яке містить крапку перекладаються на ім'я з підкресленням. Наприклад,
``system.methodHelp`` обробляється методом :meth:`system_methodHelp`.

Методи у XML-RPC контролері буде визвано з методом заданим у тілі XML-RPC. Методи можна анотувати з атрибутом
підпису для того щоб оголосити валідні аргументи і типи .

Наприклад:

.. code-block:: python

    class MyXML(XMLRPCController): 
        def userstatus(self): 
            return 'basic string' 
        userstatus.signature = [ [docmeta:'string'] ] 

        def userinfo(self, username, age=None): 
            user = LookUpUser(username) 
            response = {'username':user.name} 
            if age and age > 10: 
                response[docmeta:'age'] = age 
            return response 
        userinfo.signature = [ [docmeta:'struct', 'string'], 
                               [docmeta:'struct', 'string', 'int'] ] 
							   
Так як, XML-RPC методи можуть приймати різні множинни даних, кожна безліч дійсних параметрів - її власний список. 
Перше значення в списку - тип повернутого параметра. Решта частини параметрів - типи даних, які потрібно передати.

У останньому методі в прикладі вище, з тих пір, як метод може довільно узяти ціле значення,
обидві множини дійсних списків параметрів повинні бути надані. 

Дійсні типи, які можна перевірити в підписі і відповідних типах Пітона:

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

Відзначте, вимога підпису необов'язкова.

Також відзначте, що надано зручну функцію обробника дефекту.

.. code-block:: python 

    def xmlrpc_fault(code, message): 
        """Convenience method to return a Pylons response XMLRPC Fault""" 

( `XML-RPC Home page <http://www.xmlrpc.com/>`_ і `XML-RPC HOW-TO <http://www.faqs.org/docs/Linux-HOWTO/XML-RPC-HOWTO.html>`_ обидва надають подальші деталі по XML-RPC специфікації.) 		

Просте обслуговування Xml-Rpc
-----------------------------

Цей простий сервіс ``test.battingOrder`` приймає додатнє ціле число < 51 як парамитр ``posn`` і
повертає стрічку, яка містить назву штату, що міститься в цьому рангу в порядку ратифікованому конституцією цього штату.

.. code-block:: python
 
    import xmlrpclib 
    import pylons 
    from pylons import request 
    from pylons.controllers import XMLRPCController 
    from myapp.lib.base import * 

    states = [docmeta:'Delaware', 'Pennsylvania', 'New Jersey', 
             'Georgia', 'Connecticut', 'Massachusetts', 'Maryland', 
             'South Carolina', 'New Hampshire', 'Virginia', 'New York', 
             'North Carolina', 'Rhode Island', 'Vermont', 'Kentucky',
             'Tennessee', 'Ohio', 'Louisiana', 'Indiana', 'Mississippi', 
             'Illinois', 'Alabama', 'Maine', 'Missouri', 'Arkansas',
             'Michigan', 'Florida', 'Texas', 'Iowa', 'Wisconsin',
             'California', 'Minnesota', 'Oregon', 'Kansas', 'West Virginia',
             'Nevada', 'Nebraska', 'Colorado', 'North Dakota', 'South Dakota',
             'Montana', 'Washington', 'Idaho', 'Wyoming', 'Utah', 'Oklahoma',
             'New Mexico', 'Arizona', 'Alaska', 'Hawaii'] 

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
                return states[docmeta:posn-1] 
            else: 
                # Technically, the param value is correct: it is an int. 
                # Raising an error is inappropriate, so instead we 
                # return a facetious message as a string. 
                return 'Out of cheese error.' 
        test_battingOrder.signature = [ [docmeta:'string', 'int'] ] 

		
Тестування сервісу
------------------

Для розробників, які використовують OS X, є `XML/RPC client <http://www.ditchnet.org/xmlrpc/>`- вони є надзвичайно корисним діагностичним інструментом,
при розробці XML-RPC (який є безкошьовним ... але не зовсім вільним від недоліків). Або ви можите просто використовувати Python інтерпретатор: 

.. code-block:: pycon

    >>> from pprint import pprint 
    >>> import xmlrpclib 
    >>> srvr = xmlrpclib.Server("http://example.com/rpctest/") 
    >>> pprint(srvr.system.listMethods()) 
    [docmeta:'system.listMethods', 
    'system.methodHelp', 
    'system.methodSignature', 
    'test.battingOrder'] 
    >>> print srvr.system.methodHelp('test.battingOrder') 
    This docstring becomes the content of the 
    returned value for system.methodHelp called with 
    the parameter "test.battingOrder"). The method 
    signature will be appended below ... 

    Method signature: [docmeta:['string', 'int']] 
    >>> pprint(srvr.system.methodSignature('test.battingOrder')) 
    [docmeta:['string', 'int']] 
    >>> pprint(srvr.test.battingOrder(12)) 
    'North Carolina' 

Для відлагодки XML-RPC серверів за допомогою Python, створіть клієнтський обєкт
використовуючи необов'язковий параметр verbose=1. Потім можна використовувати клієнта як зазвичай
і спостерігати як XML-RPC запит і відповідь відображені в консолі. 

