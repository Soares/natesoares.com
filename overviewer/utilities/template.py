from django import template

class Library(template.Library):
    def setter(self, fn, name=None):
        """
        Registers a setter template tag.
        The setter should be called as follows in the template:

        {% tag_name arg1 ... as name %}

        Any number of arguments are supported. The decorated function
        will be called with the given arguments (resolved in the context)
        and the result will be set to the given name in the context.
        """
        class SetterNode(template.Node):
            def __init__(self, name, *args):
                self.name = name
                self.vars = (template.Variable(a) for a in args)
            def render(self, context):
                context[self.name] = fn(*(v.resolve(context) for v in self.vars))
                return ''

        def do_setter(parser, token):
            bits = token.split_contents()
            args = bits[1:-2]
            name = bits[-1]
            return SetterNode(name, *args)

        return self.tag(name or fn.__name__, do_setter)
