"""Decorator module

Author:         Michele Simionato
E-mail:         michele.simionato@gmail.com
Version:        0.7
License:        Python license

For more details, see:
http://www.phyast.pitt.edu/~micheles/python/documentation.html
"""

__all__ = ["decorator", "newfunc", "getinfo"]

import inspect
import itertools
import new
import sys

def getinfo(func):
    """Return an info dictionary containing:
    - name (the name of the function : str)
    - argnames (the names of the arguments : list)
    - defarg (the values of the default arguments : list)
    - fullsign (the full signature : str)
    - shortsign (the short signature : str)
    - arg0 ... argn (shortcuts for the names of the arguments)

    >>> def f(self, x=1, y=2, *args, **kw): pass

    >>> info = getinfo(f)

    >>> info["name"]
    'f'
    >>> info["argnames"]
    ['self', 'x', 'y', 'args', 'kw']
    
    >>> info["defarg"]
    (1, 2)

    >>> info["shortsign"]
    'self, x, y, *args, **kw'
    
    >>> info["fullsign"]
    'self, x=defarg[0], y=defarg[1], *args, **kw'

    >>> info["arg0"], info["arg1"], info["arg2"], info["arg3"], info["arg4"]
    ('self', 'x', 'y', 'args', 'kw')
    """
    assert inspect.ismethod(func) or inspect.isfunction(func)
    regargs, varargs, varkwargs, defaults = inspect.getargspec(func)
    argnames = list(regargs)
    if varargs: argnames.append(varargs)
    if varkwargs: argnames.append(varkwargs)
    counter = itertools.count()
    fullsign = inspect.formatargspec(
        regargs, varargs, varkwargs, defaults,
        formatvalue=lambda value: "=defarg[%i]" % counter.next())[1:-1]
    shortsign = inspect.formatargspec(
        regargs, varargs, varkwargs, defaults,
        formatvalue=lambda value: "")[1:-1]
    dic = dict([("arg%s" % n, name) for n, name in enumerate(argnames)])
    dic.update(name=func.__name__, argnames=argnames, shortsign=shortsign,
        fullsign = fullsign, defarg = func.func_defaults or ())
    return dic

def _contains_reserved_names(dic): # helper
    return "_call_" in dic or "_func_" in dic

def _decorate(func, caller, infodict=None):
    """Takes a function and a caller and returns the function
    decorated with that caller. The decorated function is obtained
    by evaluating a function with the correct signature.
    """
    infodict = infodict or getinfo(func)
    assert not _contains_reserved_names(infodict["argnames"]), \
           "You cannot use _call_ or _func_ as argument names!"
    execdict= dict(_func_=func, _call_=caller, defarg=infodict["defarg"])
    if infodict['name'] == "<lambda>":
        lambda_src = "lambda %(fullsign)s: _call_(_func_, %(shortsign)s)" \
                     % infodict
        dec_func = eval(lambda_src, execdict)
    else:
        func_src = """def %(name)s(%(fullsign)s):
        return _call_(_func_, %(shortsign)s)""" % infodict
        # import sys; print >> sys.stderr, func_src # for debugging 
        exec func_src in execdict 
        dec_func = execdict[infodict['name']]
    dec_func.__doc__ = func.__doc__
    dec_func.__dict__ = func.__dict__
    dec_func.__module__ = func.__module__
    return dec_func

class decorator(object):
    """General purpose decorator factory: takes a caller function as
input and returns a decorator. A caller function is any function like this::

    def caller(func, *args, **kw):
        # do something
        return func(*args, **kw)
    
Here is an example of usage:

    >>> @decorator
    ... def chatty(f, *args, **kw):
    ...     print "Calling %r" % f.__name__
    ...     return f(*args, **kw)
    
    >>> @chatty
    ... def f(): pass
    ...
    >>> f()
    Calling 'f'
    """
    def __init__(self, caller):
        self.caller = caller
    def __call__(self, func):
        if sys.version < '2.4': # gracefull fallback
            return lambda *args, **kw : self.caller(func, *args, **kw)
        else:
            return _decorate(func, self.caller)

def newfunc(func, model=None): # not used internally
    """Creates an independent copy of a function. If model is not None,
    the new function copies the signature, as well the attributes
    __name__, __doc__, __dict__ and __module__ from the model, which
    must be a compatible function. Here is an example of usage:
    
    >>> def f(*args, **kw):
    ...     return args[0]*2

    >>> def double(x):
    ...     pass

    >>> help(change_signature(f, double))
    Help on function double in module __main__:
    <BLANKLINE>
    double(x)
    <BLANKLINE>    
    """
    if model is None:
        return new.function(func.func_code, func.func_globals, func.func_name,
                            func.func_defaults, func.func_closure)
    else:
        return _decorate(func, lambda f, *a, **kw : f(*a,**kw),
                         getinfo(model))
