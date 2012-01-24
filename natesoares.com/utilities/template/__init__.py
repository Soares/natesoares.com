from functools import update_wrapper
from django import template
import re

class Library(template.Library):
    def basic_setter(self, fn):
        class SetterNode(template.Node):
            def __init__(self, name):
                self.name = name
            def render(self, context):
                context[self.name] = fn()
                return ''

        def do_setter(parser, token):
            try:
                tag_name, arg = token.contents.split(None, 1)
            except ValueError:
                raise template.TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])
            match = re.search(r'as (\w+)', arg)
            if not match:
                raise template.TemplateSyntaxError('%r requires the word "as", then a name.' % tag_name)
            name, = match.groups()
            return SetterNode(name)

        return self.tag(fn.__name__, do_setter)

    def simple_setter(self, fn):
        class SetterNode(template.Node):
            def __init__(self, parameter, name, lookup):
                self.parameter = parameter
                self.name = name
                self.lookup = lookup
            def render(self, context):
                if self.lookup:
                    try:
                        self.parameter = template.Variable(self.parameter).resolve(context)
                    except template.VariableDoesNotExist:
                        return ''
                context[self.name] = fn(self.parameter)
                return ''

        def do_setter(parser, token):
            try:
                tag_name, arg = token.contents.split(None, 1)
            except ValueError:
                raise template.TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])
            match = re.search(r'(.+) as (\w+)', arg)
            if not match:
                raise template.TemplateSyntaxError('%r requires an argument, the word "as", then a name.' % tag_name)
            parameter, name = match.groups()
            if (parameter[0] != parameter[-1]) or (parameter[0] not in ('"', "'")):
                lookup = True
            else:
                parameter = parameter[1:-1]
                lookup = False
            return SetterNode(parameter, name, lookup)

        return self.tag(fn.__name__, do_setter)
