# Modified for my purposes from http://www.djangosnippets.org/snippets/360/
from pygments.lexers import LEXERS, get_lexer_by_name
from pygments import highlight
from pygments.formatters import HtmlFormatter
from BeautifulSoup import BeautifulSoup
from markdown2 import markdown

# a tuple of known lexer names
lexer_names = reduce(lambda a,b: a + b[2], LEXERS.itervalues(), ())

# default formatter
formatter = HtmlFormatter(cssclass='source')

def pretty(raw):
    '''
    Accepts raw markdown text for markup processing. Using BeatifuleSoup on the
    results of markdown processing, the following constructs will be replaced
    by with pygmented highlighting. E.g.::
    
        <pre class="???">
            ...
        </pre>
        
    Where ``???`` is the name of a supported pygments lexer, e.g.: ``python``, 
    ``css``, ``html``.
    
    Note: Semantically, it would make more sense to wrap the code in a 
    ``<code>...</code>`` tag; however, my tests using markdown.py - as well as 
    markdown.pl from John Gruber - have shown that the inner HTML of the 
    ``<code>`` tag is not immune to translation.
    '''
    soup = BeautifulSoup(markdown(raw))
    for tag in soup.findAll('pre'):
        lexer_name = tag.get('class')
        if lexer_name and lexer_name in lexer_names:
            lexer = get_lexer_by_name(lexer_name, stripnl=True, encoding='UTF-8')
            tag.replaceWith(highlight(tag.renderContents(), lexer, formatter))
    
    return unicode(soup)
