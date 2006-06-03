import itertools
from copy import copy
from inspect import getargspec, formatargspec

try:
    from protocols.advice import add_assignment_advisor
except:
    msg = "Unable to import from PyProtocols, to remedy, download the latest"
    msg += " PyProtocols > 1.0a with the following command:\n"
    msg += "sudo easy_install -U -f http://peak.telecommunity.com/snapshots/ PyProtocols"
    raise Exception, msg


# Inspired by Michele Simionato's decorator library
# http://www.phyast.pitt.edu/~micheles/python/documentation.html

def decorate(func, caller, signature=None):
    """Decorate func with caller."""
    if signature is not None:
        argnames, varargs, kwargs, defaults = signature
    else:
        argnames, varargs, kwargs, defaults = getargspec(func)
    if defaults is None:
        defaults = ()
    parameters = formatargspec(argnames, varargs, kwargs, defaults)[1:-1]
    defval = itertools.count(len(argnames)-len(defaults))
    args = formatargspec(argnames, varargs, kwargs, defaults,
                         formatvalue=lambda value:"=%s" % (
                         argnames[defval.next()]))[1:-1]

    func_str = """
def %s(%s):
  return caller(func, %s)
""" % (func.__name__, parameters, args)

    exec_dict = dict(func=func, caller=caller)
    exec func_str in exec_dict
    newfunc = exec_dict[func.__name__]
    newfunc.__doc__ = func.__doc__
    newfunc.__dict__ = func.__dict__.copy()
    newfunc.__module__ = func.__module__
    if hasattr(func, "__composition__"):
        newfunc.__composition__ = copy(func.__composition__)
    else:
        newfunc.__composition__ = [func]
    newfunc.__composition__.append(newfunc)
    return newfunc

def decorator(entangler, signature=None):
    """Decorate function with entangler.

    Use signature as signature or preserve original signature if signature
    is None.

    Enables alternative decorator syntax for Python 2.3 as seen in PEAK:

        [my_decorator(foo)]
        def baz():
            pass

    Mind, the decorator needs to be a closure for this syntax to work.
    """
    def callback(frame, k, v, old_locals):
        return decorate(v, entangler(v), signature)
    return add_assignment_advisor(callback, 3)

def weak_signature_decorator(entangler):
    """Decorate function with entangler and change signature to accept
    arbitrary additional arguments.

    Enables alternative decorator syntax for Python 2.3 as seen in PEAK:

        [my_decorator(foo)]
        def baz():
            pass

    Mind, the decorator needs to be a closure for this syntax to work.
    """
    def callback(frame, k, v, old_locals):
        return decorate(v, entangler(v), make_weak_signature(v))
    return add_assignment_advisor(callback, 3)

def simple_decorator(caller, signature=None):
    """Decorate function with caller."""
    def entangle(func):
        return decorate(func, caller, signature)
    return entangle

def simple_weak_signature_decorator(caller):
    """Decorate function with caller and change signature to accept
    arbitrary additional arguments."""
    def entangle(func):
        return decorate(func, caller, make_weak_signature(func))
    return entangle

def make_weak_signature(func):
    """Change signature to accept arbitrary additional arguments."""
    argnames, varargs, kwargs, defaults = getargspec(func)
    if kwargs is None:
        kwargs = "_decorator__kwargs"
    if varargs is None:
        varargs = "_decorator__varargs"
    return argnames, varargs, kwargs, defaults

def compose(*decorators):
    """Compose decorators."""
    return lambda func: reduce(lambda f, g: g(f), decorators, func)

def func_composition(func):
    """Return composition (decorator wise) of function."""
    return getattr(func, "__composition__", [func])

def func_original(func):
    """Return original (undecorated) function."""
    return func_composition(func)[0]

def func_id(func):
    """Return identity of function.

    Identity is invariant under decorator application (if decorator is
    created with decorator() or weak_signature_decorator()).
    """
    return id(func_original(func))

def func_eq(f, g):
    """Check if functions are identical."""
    return func_id(f) == func_id(g)

__all__ = ["decorator", "compose", "func_id", "func_eq", "func_original",
           "func_composition", "weak_signature_decorator", "decorate",
           "make_weak_signature", "simple_decorator",
           "simple_weak_signature_decorator",]
