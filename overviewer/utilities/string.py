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
