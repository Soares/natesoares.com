""" Date and time utilities """

def month_diff(now, then):
    """
    >>> from datetime import date
    >>> now = date(2000, 1, 1)
    >>> then = date(1999, 11, 2)
    >>> month_diff(now, then)
    2
    """
    return ((now.year - then.year) * 12) + (now.month - then.month)
