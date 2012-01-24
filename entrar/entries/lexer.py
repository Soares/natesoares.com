"""
In order to link to an internal entry, put the link text in
curly braces and the link slug in parentheses. This will be converted
to correct markdown for the link.

>>> lex('{lex1}(lex1)')
'[lex1](/lex1/)'

If you don't have parentheses after the curly braces, nothing will
be changed.

>>> lex('{lex2}')
'{lex2}'

To escape your curly-brace / parenthese pair, put two curly braces.
They will be collapsed to one curly brace, and not turned in to links.

>>> lex('{{lex2}}(lex2)')
'{lex2}(lex2)'

Escaping with three curly braces yields two curly braces, and so on.

>>> lex('{{{lex3}}}(lex3)')
'{{lex3}}(lex3)'
"""

import re

link = re.compile(r'\{(.*?)\}\(([-\w]+?)\)')
escaped = re.compile(r'\{(\{.*?\})\}(\([-\w]+?\))')


def lex(string, stubs):
    def replace(match):
        whole = match.group(0)
        if escaped.match(whole):
            return escaped.sub(r'\1\2', whole)
        if match.group(2) in stubs:
            return '<a class="stub" href="/{1}/">{0}</a>'.format(*match.groups())
        return '[%s](/%s/)' % match.groups()
    return link.sub(replace, string)


def slugs(string):
    return tuple(m[1] for m in link.findall(string))
