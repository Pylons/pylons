.. about:

============
About Pylons
============

What, who and why
-----------------

.. image:: _static/pylon2.jpg
   :height: 480
   :width: 365
   :alt: The First Pylon of the Temple of Medinet-Habu.
   :align: left


Pylons brings a very broad but explicit :term:`Model-View-Controller` (:term:`MVC`) approach to the construction of web applications. It is specifically designed to give the application developer a high degree of flexibility when choosing ways of expressing business logic and application data; of managing the business logic and data; and of constructing a user interface (:term:`UI`) and/or an application programmer interface (:term:`API`) to afford and manage access to the model.

Pylons was written by Ben Bangert, James Gardner and Phil Jenvey, they explain here why they chose this particular approach:

    "The Pylons team are obsessed with reuse. Our vision is that in the near future Python web frameworks will all adopt the :term:`Web Server Gateway Interface` (or :term:`WSGI`) throughout their stack, making integration and reuse between frameworks extremely easy. Other frameworks don't necessarily share this vision to the same extent, preferring instead to keep their existing code base rather than opening it up to be replaced with standardized code. 

    There have been many other excellent developments in the Python web world recently such as :mod:`Paste` and :mod:`Myghty` and so, rather than duplicating the efforts of these teams by writing similar code for existing frameworks, we decided instead to put a new framework together using these existing projects with an emphasis on WSGI. We did this by working with the existing project teams and adding features to their code when possible rather than putting it all into the Pylons package.

    While we designed Pylons to have all the functionality of :term:`Rails` (porting Rails components to Python as necessary) we also designed it to be much more flexible, thanks mainly to :term:`WSGI`. This allowed us to design Pylons so that your projects are highly reusable and easy to integrate with existing projects, or integrate existing projects into Pylons. You can use Pylons in the way that feels most natural to you, and in smaller or larger chunks."

In summary, Pylons provides the connectivity for a wide set of relevant and useful components from which the web application developer can select those components that are considered best suited for the kind of application that is to be constructed.

The Model-View-Controller pattern
---------------------------------

:term:`Model-View-Controller` is an architectural pattern used in software engineering. Its defining characteristic is that the modeling of the external world, the handling of user input and the feedback to the user are explicitly separated and handled by three types of object, each specialized for its task:

The **model** 
    is a representation of the application data and the business rules used to manipulate the data. It manages the representation of the application domain, responding to requests for information about its state and responding to instructions to change state (c.f. Pylons :ref:`models`)

The **controller** 
    interprets the inputs from users or applications, commanding the model and/or the view to change as appropriate. Web applications often have several distinct controllers, each handling a different aspect of the application's behavior; a separate URL *dispatcher* maps incoming requests to the appropriate controller, as directed by a URL mapping scheme defined by the developer (c.f. Pylons :ref:`controllers`)

The **view** 
    manages the presentation of the output and renders the model into a form suitable for interaction via a UI element (for human use) or an API function (for machine use). Multiple views can exist for a single model for different purposes (c.f. Pylons :ref:`views`)

The explicit separation of these three tasks isolates the business logic and data from user interface considerations. By decoupling models and views, MVC helps to reduce the complexity in architectural design and to increase flexibility and reuse.

Developer's choice
------------------

It is becoming increasingly important for web app developers to be able to operate at an elevated level of abstraction. The choice of data store implementation is driven by the dictates of expressing the business model. Similarly, the selection of a template engine to render views of the data has to acknowledge both operational concerns and development requirements.

Making an *informed* choice entails becoming informed about the candidates: understanding their different capabilities, their respective strengths and weaknesses. In this way, Pylons encourages the development of more sophisticated attitudes towards component elements. The old saying "If all you have is a hammer, then everything looks like a nail" simply doesn't hold true for Pylons developers with their well-equipped toolboxes.

The benefits of adopting a MVC architecture for application development typically appear in the form of superior applications: they are more capable (more can be done),  they are more robust (fewer errors are made), they are easier to maintain (the separation *really* helps), they are more readily scalable and extensible (again, the separation is a key factor) ... the list goes on.

Information
-----------

Pylons is similar in many ways to Ruby on Rails since it uses similar methodologies and includes direct ports of useful Rails components such as Routes and AJAX Helpers. By combining ideas from Mason, TurboGears and various Python frameworks with a highly extensible API, Pylons provides a framework that is:

**Fast and Stable**
    Built on Mako, Routes and Paste, Pylons harnesses the full power of Mako for maximum performance. Although Pylons is still in development the core packages it uses are mature and Pylons is already being used in production systems.

**Easy to Use**
    Pylons implements the very best web development methodologies in straightforward pure-Python code. People new to Pylons are often surprised by how natural it is to use. If you already know Python you will feel right at home with Pylons, if not the Python Tutorial is an excellent starting point. Pylons plays nicely with other frameworks; you can even run TurboGears, Django and other WSGI applications from within a Pylons application making transition that bit easier. The web based interactive debugging makes even tough problems easy to resolve.

**Compatible**
    Pylons and its underlying components have been designed with great care to run on operating systems from Windows to MacOS to Linux on all types of computer from embedded devices to dedicated servers, in fact anywhere with a full Python 2.3 installation or above. Pylons can be deployed with its own server or integrated with other servers through WSGI / FastCGI / SCGI / CGI / mod_python and more. For example you can run Pylons applications on an Apache shared hosting account with ease.

**Component-Based**
    Most Pylons functionality is implemented through extension packages distributed as eggs rather than as part of Pylons Core. This enables you to only include functionality you need in your application and avoid slowdown caused by unnecessary code. Even the Pylons Core APIs have been designed so that they can be tweaked, customized, extended or replaced with the minimum of effort, often just by modifying files in your application's config directory.

**Extensible**
    If your application needs extra functionality you can install a Pylons Extension of your own. Pylons Extensions already exist to add Internationalization, Auth facilities and Rails helpers. You can easily write and distribute your own Pylons Extensions using the Extension API. Pylons Extensions are also designed to be integrated with other web frameworks and this integration is actively encouraged.

**Growing Rapidly**
    Pylons' ease of use and sophisticated features mean that it is rapidly gaining support. Its extensible architecture is enabling more people to write new packages to extend the core functionality and its careful and flexible design mean that Pylons can rapidly evolve and grow as new methodologies and ideas take root.

**Knowing Python makes Pylons easy**
    Pylons makes it easy to expand on your knowledge of Python to master Pylons for web development. Using a MVC style dispatch, Python knowledge is used at various levels:
        The Controller is just a basic Python class, called for each request. Customizing the response is as easy as overriding __call__ to make your webapp work how you want.

        Mako templating compiles directly to Python byte-code for speed and utilizes Python for template control rather than creating its own template syntax for "for, while, etc"
