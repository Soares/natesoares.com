from django.template import Library as OldLibrary
from django import template

class Library(OldLibrary):
    """
    The only difference between this and django.template.Library
    is extra decorator methods.
    """
    def setter(self, fn, name=None):
        """
        Registers a setter template tag. Decorate a function with it.
        Call the setter as follows in the template:

        {% tag_name arg1 ... as name %}

        all of the arguments (any number are supported) will be passed
        to the decorated function, and the result of the decorated
        function will be bound to 'name'.
        """
        class SetterNode(template.Node):
            def __init__(self, name, *args):
                self.name = name
                self.vars = map(template.Variable, args)

            def render(self, context):
                context[self.name] = fn(*(v.resolve(context) for v in self.vars))
                return ''

        def do_setter(parser, token):
            bits = token.split_contents()
            args = bits[1:-2]
            name = bits[-1]
            return SetterNode(name, *args)

        return self.tag(name or fn.__name__, do_setter)


    def simple_tag(self, fn, name=None):
        """ Just like django's simple tag, but allows variable length args. """
        class SimpleNode(template.Node):
            def __init__(self, *args):
                self.vars = map(template.Variable, args)

            def render(self, context):
                return fn(*(var.resolve(context) for var in self.vars))

        def do_simple_tag(parser, token):
            return SimpleNode(*token.split_contents()[1:])

        return self.tag(name or fn.__name__, do_simple_tag)
