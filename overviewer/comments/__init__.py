def context_processor(request):
    context = {'comment_depth': 5}
    get, names = request.GET, ('reply_to', 'edit')
    context.update(dict((name, get[name]) for name in names if name in get))
    return context


def get_model():
    from models import EditableComment
    return EditableComment


def get_form():
    from forms import EditableCommentForm
    return EditableCommentForm
