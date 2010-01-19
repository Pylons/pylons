.. _debugging:

===========================
Troubleshooting & Debugging
===========================

.. _interactive_debugging:

Interactive debugging
---------------------

Things break, and when they do, quickly pinpointing what went wrong and why makes a huge difference. By default, Pylons uses a customized version of `Ian Bicking's <http://blog.ianbicking.org/>`_ EvalException middleware that also includes full Mako/Myghty Traceback information. 


The Debugging Screen 
-------------------- 

The debugging screen has three tabs at the top: 

``Traceback`` 
Provides the raw exception trace with the interactive debugger 

``Extra Data`` 
Displays CGI, WSGI variables at the time of the exception, in addition to configuration information 

``Template`` 
Human friendly traceback for Mako or Myghty templates 

Since Mako and Myghty compile their templates to Python modules, it can be difficult to accurately figure out what line of the template resulted in the error. The `Template` tab provides the full Mako or Myghty traceback which contains accurate line numbers for your templates, and where the error originated from. If your exception was triggered before a template was rendered, no Template information will be available in this section. 

Example: Exploring the Traceback 
-------------------------------- 

Using the interactive debugger can also be useful to gain a deeper insight into objects present only during the web request like the ``session`` and ``request`` objects. 

To trigger an error so that we can explore what's happening just raise an exception inside an action you're curious about. In this example, we'll raise an error in the action that's used to display the page you're reading this on. Here's what the docs controller looks like: 

.. code-block:: python 

    class DocsController(BaseController): 
        def view(self, url): 
            if request.path_info.endswith('docs'): 
                redirect(url('/docs/'))
            return render('/docs/' + url) 

Since we want to explore the ``session`` and ``request``, we'll need to bind them first. Here's what our action now looks like with the binding and raising an exception: 

.. code-block:: python 

    def view(self, url): 
        raise "hi" 
        if request.path_info.endswith('docs'): 
            redirect(url('/docs/'))
        return render('/docs/' + url) 

Here's what exploring the Traceback from the above example looks like (Excerpt of the relevant portion): 

.. image:: _static/doctraceback.png
    :width: 750px
    :height: 260px

Email Options 
-------------

You can make all sorts of changes to how the debugging works. For example if you disable the ``debug`` variable in the config file Pylons will email you an error report instead of displaying it as long as you provide your email address at the top of the config file: 

.. code-block:: ini 

    error_email_from = you@example.com 

This is very useful for a production site. Emails are sent via SMTP so you need to specify a valid SMTP server too. 

Error Handling Options 
====================== 

A number of error handling options can be specified in the config file. These are described in the :ref:`interactive_debugging` documentation but the important point to remember is that debug should always be set to ``false`` in production environments otherwise if an error occurs the visitor will be presented with the developer's interactive traceback which they could use to execute malicious code.
