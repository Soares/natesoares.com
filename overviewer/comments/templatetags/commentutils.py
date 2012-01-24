from django.contrib.contenttypes.models import ContentType
from overviewer.utilities.template import Library
from overviewer.comments.models import EditableComment

register = Library()


@register.setter
def get_comments_for(object):
    return EditableComment.objects.for_model(object)


@register.filter
def comment_depth_exceeded(depth):
    return depth <= 0


def comment_count(object):
    comments = EditableComment.objects.for_model(object)
    return reduce(lambda c, o: c + comment_count(o), comments, comments.count())

register.filter(comment_count)
