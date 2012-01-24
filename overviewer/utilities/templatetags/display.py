def style(string):
    return '<link rel="stylesheet" type="text/css" href="/media/css/%s.css">' % string


def script(string):
    return '<script type="text/javascript" src="/media/js/%s.js"></script>' % string


def feed(name, title='', type='atom'):
    return '<link href="/feeds/%s/" rel="alternate" type="application/%s+xml" title="%s">' % (name, type, title)


def feeds(name, title=''):
    atom = feed(name, title)
    rss = feed('%s-rss' % name, '%s (rss)' % title, 'rss')
    return atom
