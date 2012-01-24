import re

def truncate(string, length, suffix='...'):
    """
    Truncates a string down to at most @length characters.

    >>> truncate('hello', 12)
    'hello'

    If the string is longer than @length, it will cut the
    string and append @suffix to the end, such that the
    length of the resulting string is @length.

    >>> truncate('goodbye', 4)
    'g...'
    >>> truncate('goodbye', 6)
    'goo...'

    @suffix defaults to '...'.

    >>> truncate('hello', 3, '..')
    'h..'

    >>> truncate('hello', 3, '')
    'hel'
    """
    if len(string) <= length:
        return string
    return string[:length-len(suffix)] + suffix

def slugify(string, length=50, lower=True, space='-'):
    """
    Replaces spaces with underscores and then removes all non-slug characters.
    Truncates to @length, default 50

    >>> slugify('Hello, World!')
    'hello-world'

    >>> slugify('Hello, World!', spaces='_')
    'hello_world'

    >>> slugify('Hello, World!', lower=False)
    'Hello-World'

    >>> slugify('Hello, World!', 5, False)
    'Hello'
    """
    spaces = re.compile(r' ')
    others = re.compile(r'[^-\w]')
    string = truncate(others.sub('', spaces.sub(space, string)), length, '')
    return string.lower() if lower else string


def slug_models(model, slug_list, field_name='slug'):
    if not slug_list:
        return ()
    slugs = map(type(slug_list).strip, slug_list.split(','))
    return model.objects.filter(**{'%s__in' % field_name: slugs})


def curried(fn):
    """
    I use this for decorators.

    >>> def x(a, b):
    ...     return a, b
    ... 
    >>> y = curried(x)

    Positional  arguments work.

    >>> y(1)(2)
    (1, 2)

    Keyword arguments work.

    >>> y(b=2)(1)
    (1, 2)

    Multiple arguments work.

    >>> y(b=2, a=1)()
    (1, 2)
    """
    return lambda *a, **k: lambda *ar, **kw: fn(*(a + ar), **dict(k, **kw))
