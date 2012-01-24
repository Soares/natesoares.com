"""
Nate's functional utilities:
    Because sometimes map and reduce aren't enough.
"""
from functools import update_wrapper

def curry(fn, *args, **kwargs):
    """
    >>> def fn(a, b, c=3):
    ...     return a, b, c
    ...
    >>> x = curry(fn, 1)
    >>> x(2, 3)
    (1, 2, 3)
    >>> y = curry(fn, b=2)
    >>> y(1)
    (1, 2, 3)
    >>> y(1, c=2)
    (1, 2, 2)
    >>> z = curry(fn, 1, c=1)
    >>> z(1)
    (1, 1, 1)
    >>> 
    """
    def curried(*a, **k):
        return fn(*(args + a), **dict(kwargs, **k))
    update_wrapper(curried, fn)
    return curried


def take(num, iterable):
    """
    >>> list(take(5, xrange(3)))
    [0, 1, 2]
    >>> list(take(5, xrange(10)))
    [0, 1, 2, 3, 4]
    """
    for i, e in enumerate(iterable):
        if i >= num:
            break
        yield e


def decorator(candidate):
    """
    Turns a function of (fn, *args, **kwargs) into a decorator that
    decorates function, waits for *args and **kwargs, and then applies
    the decorator.

    >>> @decorator
    ... def add_one_to_first_arg(fn, a):
    ...     return fn(a+1)
    ...
    >>> @add_one_to_first_arg
    ... def addone(x):
    ...     return x
    ...
    >>> addone(2)
    3
    """
    def real_decorator(fn):
        return lambda *args, **kwargs: candidate(fn, *args, **kwargs)
    update_wrapper(real_decorator, candidate)
    return real_decorator
