.. _helpers:

=========
Помічники 
=========

Помічники це функції для роботи з шаблонами, які прийшли на допомогу
загальному HTML, і призначені для маніпулювання текстом, конструкціями вищого рівня такими
як HTML тег builder (який безпечно екранує змінні), і більш досконалішою
функціональністю такою як розбиття на сторінки набору даних.

Більшість помічників які доступні у Pylons забезпечені пакетом 
:mod:`webhelpers`. Деякі з них також використовуються у контролерах,
для того щоб приготувати дані для подальшого використання в темплейтах іншими
помічниками, такими як :func:`~webhelpers.rails.secure_form_tag` - функція
яка в свою чергу має відповідну :func:`~pylons.decorators.secure.authenticate_form`.

Для того щоб зробити власнний тег доступним для використання в шаблонах
під :term:`h`, треба імпортувати потрібні функції у :file:`lib/helpers.py`.
Всі функції які знаходяться в цьому файлі є доступними під 
:term:`h` так як і інші модульні посилання.

Налаштовуючи модуль :file:`lib/helpers.py` ви можите швидко
додати будь-які функції і класи для використання у своїх шаблонах.

Функції-помічники упорядковані в модулі за темою. Усі генератори
HTML є у пакеті ``webhelpers_html``, за винятком кількох другорядних
модулів які є прямо у  ``webhelpers``. Вони також окремо документовані,
дивіться :mod:`webhelpers`.
.. _pagination:

Розбиття на сторінки
====================

.. note::

	Модуль `paginate` не є відповідним застарілому `pagination`, що постачався з
	попереднюю версією пакету Webhelpers.

Мета розбивача сторінок
-----------------------

Коли ви відображаєте велику кількість даних, наприклад результат  SQL запиту
і не можите зазвичай відобразити всі результати на одній сторінці. Їх буде
аж надто багато. Тоді ви ділите дані на менші куски. Це саме те що робить розбивач сторінок (paginator).
Він показує одну сторінку з шматком даних в момент часу. Уявіть що ви надаєте телефонний довідник компанії
через інтернет і дозволяти користувачам пошук по ньому. Припустимо що пошук видав 23 результати.
Можливо ви вирішите показати не більше десяти на сторінку. Отже, перша сторінка міститиме 1-10 результатів,
друга 11-20 і третя відповідно 21-23. І ви також показуєе навігаційний елемент, щось схоже на 
``Page 1 of 3: [1] 2 3``, який дозволить користувачу переключатись між доступними сторінками.

Клас ``Page`` 
-------------

Пакет :mod:`webhelpers` надає модуль *нумерування*, який вживається для цієї мети. Він може створити сторінки
з простого Python-списку негірше ніж SQLAlchemy запити чи SQLAlchemy обєкти-вибірки.
Модуль надає обєкт ``Page`` що представляє собою єдину сторінку з більшого набору результатів.
Така ``Page`` в основному поводиться як список елементів на цій сторінці. Давайте 
попередній приклад з 23 елементів розібємо на 3 сторінки ::

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


За додатковими параметрами виклику обєкта ``Page`` дивіться тут
:class:`webhelpers.paginate.Page`

.. note::
	Номера сторінок та елементів починаються з 1. Якщо ви доступаєтесь до
	елементів на сторінці за їхнім індексом  зверніть увагу що перший елемент-
	це ``item[1]``, а не ``item[0]``.


Перемикання між сторінками, використовуючи `pager`
--------------------------------------------------

Користувачу потрібний спосіб для отримання іншої сторінки. Це зазвичай зроблено списком лінків,
наприклад, ``Page 3 of 41 - 1 2 [3] 4 5 .. 41``. Такий список можна створити
за допомогою Page's :meth:`~webhelpers.paginate.Page.pager` методів. Звернимось до нашого
прикладу знову ::

   >>> page2.pager()
    
        <a class="pager_link" href="/content?page=1">1</a>
        <span class="pager_curpage">2</span>
        <a class="pager_link" href="/content?page=3">3</a>

Без  HTML це виглядає як ``1 [2] 3``. Лінк вказує на URL де знайдена необхідна сторінка.
Також виділено поточну сторінку (2).

Вигляд пейджера можна налаштувати . За замовчуванням формат стрічки є ``~2~`` ,
що означає показувати суміжні сторінки від поточної сторінки з максимальним радіусом 2.
В більшій множині це виглядатиме так ``1 .. 34 35 [36] 37 38 .. 176``. Радіус двох означає,
що показано дві сторінки до поточної і дві після.
 
Декілька спеціальних змінних можна використати в форматі стрічки.
Дивіться :meth:`~webhelpers.paginate.Page.pager` за повним списком.
Деякі приклади для пейджера з 20 сторінок (знаходячись на 10 сторінці)::

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


Пейджинг через SQLAlchemy запит
-------------------------------

Якщо дані до сторінки over comes from базу диних через
SQLAlchemy, тоді модуль ``paginate`` може прямо доступитись 
до ``query`` обєкту. Це зручно при використанні ORM-mapped моделі.
Приклад::

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

Модуль `paginate` є достатньо розумним для того щоб запитувати в бази даних 
лише ті обєкти, що потрібні на цій сторінці. Наприклад, якщо сторінка складається із
10-20 елементів тоді SQLAlchemy попросять вибрати точно тих
10 рядків через `LIMIT` і `OFFSET` у фактичному SQL запиті.
Отже, вам не потрібно завантажувати повний результат в памятьі передавати його.
Натомість,створюючи `Page` завжди передавайте `query`.


Пейджинг через SQLAlchemy select
--------------------------------

SQLAlchemy також дозволяє запустити довільний селект на таблицю
бази дних. Це корисно для не-ORM запитів. `paginate` може також використовувати
такі селект обєкти. Приклад::

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

Єдиною різницею у використанні SQLAlchemy *query* обєктів є необхідність передачі
SQLAlchemy *сесію* через ``sqlalchemy_session`` параметр.
Сам по собі чистий ``select`` не має призначеного з'єднання. Зате, сесія має.


Використання в Pylons контролера і шаблонів
-------------------------------------------

Маленький приклад для початку.

Controller::

    def list(self):
        c.employees = webhelpers.paginate.Page(
            model.Session.query(model.Employee),
            page = int(request.params['page']),
            items_per_page = 5
            )
        return render('/employees/list.mako')

Template:

.. code-block:: mako

    ${ c.employees.pager('Page $page: $link_previous $link_next ~4~') }
    <ul>
    % for employee in c.employees:
        <li>${ employee.first_name } ${ employee.last_name}</li>
    % endfor
    </ul>
	
`pager()` створює посилання на попереднє URL і лише
встановлює *page* параметри, відповідно. Ось чому вам необхідно
надіслати номер сторінки, яку запитують  (``request.params['page']``), коли
ви створюєте `Page`.


Часткові оновлення з AJAX
-------------------------

Легко оновити частину сторінки. Потрібно лише використати
Javascript, який замість повного завантаження оновлює лише
частину сторінки, яка містить "paginated" елементи. Метод
``render()`` приймає параметром ``onclick`` для цієї мети. Це значення 
додано як ``onclick`` параметр тегів A-HREF. Отже, параметр ``href`` вказує на
URL, що завантажує цілу сторінку, натомість ``onclick`` параметр забезпечує
Javascript, що завантажує частину сторінки. Приклад (використовується бібліотека 
Javascript jQuery для простоти) допоможе зрозуміти це.

Controller::

    def list(self):
        c.employees = webhelpers.paginate.Page(
            model.Session.query(model.Employee),
            page = int(request.params['page']),
            items_per_page = 5
            )
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
            ${ webhelpers.html.tags.javascript_link('/public/jQuery.js') }
        </head>
        <body>
            <div id="page-area">
                <%include file="list-partial.mako"/>
            </div>
        </body>
    </html>

Template ``list-partial.mako``:

.. code-block:: mako

    ${ c.employees.pager(
        'Page $page: $link_previous $link_next ~4~',
        onclick="$('#my-page-area').load('%s'); return false;"
        ) }
    <ul>
    % for employee in c.employees:
        <li>${ employee.first_name } ${ employee.last_name}</li>
    % endfor
    </ul>

Для уникнення дублювання коду в темплейті - повний темплейт включає частковий 
темплейт. Коли запитується частковве завантаженння - виконується
``list-partial.mako``. І коли запитується повне
завантаження сторінки - тоді ``list-full.mako`` виконується, який
в свою чергу містить ``list-partial.mako``.

Змінна ``%s`` у  стрічці ``onclick`` замінюється URL, яка вказує на
відповідну сторінку з додаванням  ``partial=1`` (налаштувати імя
параметрів можна через параметер ``partial_param``) Приклад :

* ``href`` parameter points to ``/employees/list?page=3``
* ``onclick`` parameter contains Javascript loading
  ``/employees/list?page=3&partial=1``

jQuery's синтаксис завантаження URL у певний DOM обєкт (e.g. a DIV) ::

    $('#some-id').load('/the/url')

Переваги цієї техніки в тому що вона граціозно погіршується. Якщо користувач
не має влюченого Javascript - тоді завантажується повна сторінка. І якщо Javascript
працює - часткове завантаження відбувається за допомогою ``onclick`` події.


.. _secure-forms:

Безпечні помічники тега форми
=============================

Для запобігяння атак Підробки міжсайтових запитів (CSRF). 

Генерують форми, які містять клієнтську авторизацію, що перевіряється призначеною
web app.

Ознаки авторизації зберігаються в клієнтській сесії. Потім web app
може перевіряти авторизацію представлену запитом із значенням у клєнтській сесії.

Це гарантує, що запит прийшов від початкової сторінки.
Дивіться у Вікепедії про  `Cross-site request forgery` за додатковою інформацією.

.. __: http://en.wikipedia.org/wiki/Cross-site_request_forgery

Pylons надає декоратор ``authenticate_form``, що виконує цю перевірку від імені контролерів.
Ці хелпери залежать від пайлінівського обєкту ``session``. Більшість з них
можна легко перенести на інший фреймворк, замінюючи виклики API.

Помічники зроблені таким чином, що розробникам повинно бути легко
створити свої власні хелпери, для використання у викликах AJAX.

:func:`authentication_token` повертає поточний маркер автентифікації, створюючи його
і зберігаючи у сесії, якщо він ще не існує.

:func:`auth_token_hidden_field` створює приховане поле, що містить
ознаку автентифікації.

:func:`secure_form` є :func:`form` плюс :func:`auth_token_hidden_field`.



