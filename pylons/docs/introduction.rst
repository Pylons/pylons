.. _introduction:

Welcome to Pylons
=================

Welcome to Pylons. This is the right place if you want to create web-based
applications in Python easily. Maybe you have even written web applications in
other languages like PHP or programmed CGIs in Perl. This introduction will tell
you how using Pylons is different from that. Basically Pylons is a *web
framework*. It provides a basis for your own web applications. 

Features
--------

Pylons has a lot of nice features that make writing web applications easy.

Comfortable interactive debugger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Programming means making mistakes. And searching for the cause of an error
distracts you from the task at hand and is annoying. Especially in web
applications you usually do not have a fancy debugger at hand that allows you
to view all variables and the piece of code where the error occured. Pylons
offers a great online debugger. If your application throws an exception you
will get a traceback on the web page, can view local variables and can even
enter Python statements interactively. Sometimes people even deliberately throw
in a ``raise Exception`` statement to make the application stop at that line so
they can investigate what is going on. The debugger even works with AJAX
requests as it prints the debug URL on the console for a sub-request that you
can just paste in your browser and debug it. And in case your application
runs on a production server and get into an error situation it will collect
all that information and send your an email.

.. TODO: Screenshot of debugger

Exploring the world: Paster shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Pylons application uses many different Python modules. The environment
in which your application is running seems pretty opaque. Fortunately you can
run the ``paster shell`` which is a normal Python shell (or even an *ipython*
shell if you have it installed) but has access to all the global variables and
utility functions that Pylons offers. Play with your database models, explore
the "Webhelpers" utilities, browse through the available global variables and
even simulate requests as if you used a browser. And if things work as you
expect you just copy the code into your application.

.. TODO: Screenshot of console window with paster-shell and a few statements

Web server built in
^^^^^^^^^^^^^^^^^^^

Pylons uses *Paste* for setting up a project, upgrading it to a newer Pylons
version and deploying the application. And it even features a built-in web
server that you can use to develop and test your applications. You don't have to
install an additional web server like Apache to run your application.
Development happens directly on your workstation. And the Paste web server is
even powerful enough that some people use in on production servers.

Simplifying the development cycle: --reload
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Developing under a web framework means that your framework has to be restarted
once you changed something. If you use the Paste web server you can toss in the
``--reload`` option so that Paste will monitor your files. Once you save a
changed file it will automatically detect that and reload the framework. Your
development cycle is essentially saving the file and reloading the page in the
browser. It could not be simpler.

WSGI - ready for production use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pylons does not depend on a certain web server. Other frameworks may have a web
server built in - so you depend on its stability, security and features. Pylons
is a WSGI framework which means that it works on any web server that speaks
WSGI. WSGI is a protocol between web servers and web applications - similar to
CGI. Basically any WSGI web application can run with any WSGI web server. And
you can even use WSGI *middleware* which is code you can simply plug between the
web server and the web application to provide features like authentication or
logging.

Smooth upgrades
^^^^^^^^^^^^^^^

Pylons is a template for your project. It creates a number of files and
directories where your HTML templates, database models and controller code goes
into. You will surely change that template a lot. But what happens when a new
version of Pylons is released? No problem. Pylons can show you the differences
between your files and the new template and you are free to adopt any changes.
So you are always up-to-date without starting from scratch.

.. TODO: Screenshot showing an upgrade with a conflicting file

The web developer's toolbox: Webhelpers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To avoid reinventing the wheel Pylons applications can use the *Webhelpers*
package. It contains functions to deal with HTML tags and HTML forms, they convert
numbers into human-readable forms, deal with RSS feeds and split large outputs
(like database tables) into pages by only a few lines of Python code.

Beautiful URLs
^^^^^^^^^^^^^^

Usually you don't have complete control over the URL in web applications. They
look like ``/cgi-bin/myscript.pl?search=weather`` or
``/customers/settings.php?customerid=123``. Pylons instead uses *Routes*
to map any URL scheme to different parts of your application. So you will
rather end up with user-friendly and memorable URLs like ``/articles/2008``
or ``/products/computer/keyboards``.

Exchangable components
^^^^^^^^^^^^^^^^^^^^^^

Pylons is open-minded. You can use it with different templating languages and
different database toolkits. A good selection of components is already
configured so that you can get started quickly. But it is really easy to replace
them if they do not match your taste.

Seperated models, views and controllers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Pylons you seperate the models (your database schema), the views (HTML
templates) and the controllers (your application code). That is called *MVC*
(model, view, controller). Using this MVC approach you can change database
models or the HTML templates without risking to break your application code.

Friendly community
^^^^^^^^^^^^^^^^^^

Join the Pylons community by subscribing to the
`mailing list <http://googlegroups.com/group/pylons-discuss>`_ or join us on
``#pylons`` on irc.freenode.net. Meet both users and developers. Get your
questions answered and make proposals that the developers may include in the
next release.


What is a framework?
--------------------

You read it already: Pylons is a web *framework*. Generally a framework is a
collection of components (like other programs, code libraries or even scripting
languages) that work together as a basis for your own application. The
application that you write runs inside the context of the framework. When you
develop a web application you often have the need for...

- something that prints HTML tags
- something that reads parameters that are sent via HTTP forms
- something that stores information in a database and gets it back
- something that contains your application logic
- something that maintains cookie-based sessions
- something that speaks HTTP and sends web pages to your browser
- something that maps URLs to parts of your application

If you have already written a web application you will have done most of the
above parts yourself. You probably used ``print`` statements to create the HTML
and did not care about complex *templating* systems. That works well in simple
applications. But programs tends to grow larger and without a good concept
become less maintainable. You may later have a dozen programs that output HTML
pages that look similar. Sure, you can move some common parts into a module that
you use from all your programs. But basically you create solutions for typical
tasks that almost every web applications have.

Fortunately some developers invested their spare time to create Python modules
that fulfil these everyday tasks. For example there is a Python package called
*Mako* that deals with creating HTML output - a so called *templating* system.
Using the *Mako syntax* you create a template file that contains your HTML page.
But you can add Python statements right in that file where you need it and can
access variables from other parts of your application. There are if/then/else
constructs so that every user of your web site only sees what is needed. And as
these templates can even include each other you can easily change the looks of
your web site by just changing a parent template.

This is just one example of how such components can make your life as a
programmer easier. There are a lot of helpful components. And it is a good idea
to use them instead of dealing with these boring everyday tasks. Now imagine
you take a number of these useful components and get them to work together. A
*web framework* like Pylons is exactly doing that. You may think of Pylons as
the "glue" between these components.

What does MVC mean?
-------------------

You may have heard the abbrevation *MVC* in the context of web frameworks. MVC
is short for *Model - View - Controller* and depicts a design pattern used in
software engineering. The MVC approach splits your application into:

Models
    They contain data that your application works with. Models do not
    contain any information on the meaning of this data. Often the model
    refers to database tables.

View
    It is responsible for reading data from a model and displaying it to the
    user. (While models and controllers are called the same in Pylons you may
    notice that the equivalent part to a *view* in Pylons is basically the
    *template*.)

Controller
    Here lies the logic of your application. The controller uses views to
    display data to the user or gets information from the user and stores them
    back into the models.

You may wonder what is so special about that design pattern. You already wrote
programs that communicate with your database, send HTML to the user and contain
some kind of intelligence to steer everything. The idea of MVC is that you
seperate all these tasks so that you can change one part without breaking
another.

For a more complete explanation see `Wikipedia's article
<http://en.wikipedia.org/wiki/Model_View_Controller)>`_ on MVC.

Pylons' components
------------------

What puzzles many beginners is that Pylons works as a collection of components.
Pylons is not a framework that *contains* everything you need. So there is no
single handbook describing all the components because they have their own
documentation already. Pylons rather *connects* all the
components so you can easily use them together. That means you will still have
to learn about each of the components. During this introductory article we will
explain the basics of each one. But to fully understand the components you will
have to read their respective documentation. Pylons does not even force you to
use a fixed set of components. The standard Pylons project uses a good
selection though that we would like to show you. It all begins with...

Create, run and deploy a Pylons application: Paste
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Paste is a collection of all kinds of tools and programs that help developing
and running WSGI applications. It comes with a WSGI web server that you can use
to run your application. The central place to store configuration information in
your Pylons project is the *ini file*. By default it is called
"development.ini". Later on your deployment server you will likely call it
differently - e.g. "myserver.ini". This file is important for Paste so it knows
which web applications to load and run.

Paste also maintains your project in other ways. It creates your initial
project's directory tree. It allows you to smoothly update your project to a new
Pylons version. And it helps turning your application into an egg and deploying
it.

Write HTML templates: Mako
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the templating system. Instead of using ``print`` statements to print
out HTML that is sent to the user's browser you will use templates. A template
can contain pure HTML that is displayed in the browser. You would tell your
application to::

    render('/welcome.mako')

and Mako will load the file ``templates/welcome.mako`` and send it to
the browser. Templates are helpful so that you can keep the structure
of your document in the template and most of the programming logic
in the Python part (called controllers).

One of the more interesting features of templates is that they can be jazzed up
by control statements and Python code. A simple example:

.. code-block:: mako

    <html>
    <body>
        <h1>Welcome</h1>
        <p>Today we serve:</p>
        <ul>
    % for meal in ['calzone', 'porkpie', 'pizza']:
            <li>${ meal }</li>
    % endfor
        </ul>
    </body>
    </html>

Templates offer some amazing features. You can use variables that you defined
elsewhere in your application. You can include or inherit from other templates.
If you know PHP a little then this way to mix HTML with programming logic may
appear well-known to you.

Access your database: SQLAlchemy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most web applications need a database as a persistent storage. You can save
your customer information in there, articles of your web shop or any other data
that needs to live longer than the duration of an HTTP request. An SQL database
can be accessed by the SQL query language. But with SQL toolkits like
SQLAlchemy you can make database access more convenient and pythonic. That
doesn't mean that you will save time instantly because you need to carefully
define your database models but in the long run you will find it easier. And
SQL toolkits are not bound to specific database backends. You can easily
switch from MySQL to PostgreSQL by just changing the connect string. SQLAlchemy
consists of two parts:

- an SQL toolkit
- an object relational mapper

The 'SQL toolkit' part is easy to explain: you tell SQLAlchemy how your
database tables look in Python and don't need to write SQL statements any more.
Think of SQLAlchemy as an abstraction layer. If you use that abstraction
everywhere in your application you do not have to depend on a certain database
backend and in many cases don't need to care about subtleties of the different
database servers.

An even more interesting part is the *object relational mapping* that SQLAlchemy
delivers. Imagine that you define a trivial empty Python class like::

    class Customer(object):
        pass

Then you call a *mapper* function that connects your class to a database table.
Now you do not even need to work with tables any more but have some new useful
methods on your class. A simple example::

    mycustomer = query(Customer).filter_by(name='Jack').first()

This will query the database and get a database record with the name 'Jack'
from the table that represents your customers. All the database fields are
automatically added to the mycustomer object as class properties. Example::

    print "The customer's phone number is", mycustomer.phone

Isn't this more readable than writing SQL queries? And there's more like e.g.
many-to-many relationships that are maintained easily or automatic retrieval of
rows from other tables that are connected by foreign keys.

SQLAlchemy comes with `excellent documentation
<http://www.sqlalchemy.org/docs/>`__, too.

Invent your personal URL scheme: Routes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An interesting feature of web frameworks is that you entirely control what you
do with the user's HTTP request. That includes the URL itself. Routes' job is
to determine what Python code must be run depending on how the URL looks like.
Let's take the following URL as an example:

    http://example.com/blog/2007/01

You can tell Routes that you want the ``BlogController`` to handle this
request and pass on the '2007' as a year and the '01' as the month.
In Routes syntax this looks like:

    m.connect('blog/:year/:month', controller='blog')

The URL routing configuration is found in ``config/routing.py`` of your
application by the way. By default a URL like

    http://example.com/blog/2007/01

is passed to the BlogController (the controller name is indeed computed
by taking the string "blog" by adding the word "controller" and using
camel-case) with ``action='2007'`` and ``id='01'``.

Few wheels to reinvent: Webhelpers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Even with the components described above you will still find yourself writing
utility functions for common tasks. The *Webhelpers* is a package of such
helper functions that you can use in your Pylons applications. Some examples of
what they do:

- split up large amounts of data into pages (pagination)
- format text and numbers into human-readable forms
- print URLs, links, HTML form elements
- create RSS feeds

Caching and cookie-based sessions: Beaker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Beaker is one of the less visible parts of Pylons. It provides cookie-based
sessions for example. A session is basically a dictionary where you can store
per-user information. To attribute a dictionary to a certain user Beaker sends
a randomly created session identification to the user - stored in a cookie. So
when the user accesses your web site, their browser will send the cookie along
with the HTTP request and Beaker gets the respective session dictionary for
you. So you can store temporary sessions per-user like whether they are logged
in, what their username is or what language they like to read your web site in.
As the sessions are server-based the user can't change the information directly
by sending fake cookies. And Beaker also uses a secret string to
cryptographically sign the cookie string so the user cannot easily change the
cookie and hope to get accidental access to other users' sessions. Beware that
sessions are not a permanent storage. They expire after a day by default.
Use a database if you need to store information for longer.

Beaker is also used to cache HTML output from the Mako templates. If possible
Beaker takes a HTML page that has already been rendered instead of having Mako
compute the page again. That saves a few CPU cycles.


Are there other web frameworks?
-------------------------------

Yes, a lot of them. See the `Python Wiki
<http://wiki.python.org/moin/WebFrameworks>`_ for an impressive list. Two other
commonly used frameworks are Django and Turbogears. It is hard to write an
unbiased comparison because basically all three frameworks provide similar
functionality. And different programmers may have different expectations. The
main difference is that Pylons is rather glueing together other Python
components that are powerful and proven to work well. While other frameworks
like Django reinvent a lot of wheels and those components work together
smoothly. But you often cannot replace them with other components. Nor are they
always WSGI frameworks so you are stuck with the web server that is contained
with the framework. Pylons fans appreciate the flexibility of being able to
replace almost any component of it to their liking. Even though that may mean
that they have to learn about the external components.


How is using a web framework different from CGI programming?
------------------------------------------------------------

Many developers have programmed CGIs in a scripting language like Perl. Mostly
because that is what most web hosting services offer. A CGI is a program
that is launched by the web server when a user requests a certain URL in the
browser. The CGI reads information it gets sent from the browser (and some
environment variables that are set by the web server) and prints HTML that is
shown in the browser. Your CGIs can't work as standalone applications.
You always need a web server like Apache to accept the request and launch
the CGI.

Pylons (WSGI) applications are actually similar to CGI applications. While you
need a CGI-aware web server to run CGI scripts you need a WSGI-aware web server
to run WSGI applications. Unless you have any special needs you can well use
the web server built into Paste. Pylons makes excessive use of the "Paste"
tools anyway so you will not have to install any extra software. This approach
has several advantages:

- you can develop your application on your workstation easily because you
  do not need a complex set up with a third-party web server like Apache.
  Just start up the built-in web server process and try out your application.
  The server will even check if any of your program parts will change
  and reload the server automatically. So your development cycle is simple:
  save your changes in your text editor and press reload in the browser.
- you can control all aspects of the web server within your application
  (like returning HTTP error codes) that are otherwise handled by the web
  server. That enables you to add middleware for authentication or to deal
  with 404 (page not found) errors exactly in the way you want.
- you can have flexible URL schemes. In CGIs the URLs always reflect
  the name of the CGI to be run. With Pylons you define what action is run
  when a certain URL pattern matches (e.g. /articles/2007/01)
- the web server keeps the whole application in memory which boosts the speed
  of your application. When using CGIs the web server will load and launch your
  script interpreter everytime the CGI is requested which creates much overhead
  on busy web sites. Pylons initialises everything it needs upon startup and
  connects to the database already.
