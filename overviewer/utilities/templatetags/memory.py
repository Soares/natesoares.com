from django import template

class RecordNode(template.Node):
    def __init__(self, name, nodelist):
        self.name, self.nodelist = name, nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        context.dicts[-1].setdefault('recordings', {})[self.name] = content
        return ''


class RecallNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        return context.get('recordings', {}).get(self.name, '')


def do_record(parser, token):
    try:
        tag, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag should have only one argument' % token.contents.split()[0])
    nodelist = parser.parse(('endrecord',))
    parser.delete_first_token()
    return RecordNode(name, nodelist)


def do_recall(parser, token):
    try:
        tag, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag should have only one argument' % token.contents.split()[0])
    return RecallNode(name)
