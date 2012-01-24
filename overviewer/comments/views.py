from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import comments
from overviewer.comments.models import EditableComment as Comment
from overviewer.utilities.views import render_just

def render(request, name, context=None, processors=()):
    from overviewer.utilities.views import render
    from overviewer.comments import context_processor
    processors += (context_processor,)
    return render(request, name, context, processors)


def edit(request, id):
    """
    Will redirect if 'next' is given in post.
    If 'next' is not given in post, will assume that the
    call is asynchronous and will return the new content.
    """
    comment = get_object_or_404(Comment, id=id)
    content = request.POST['comment']
    next = request.POST.get('next', '')
    user = request.user
    if content and user.is_authenticated() and user == comment.user:
        comment.comment = content
        comment.edited = True
        comment.save()
    return redirect(next) if next else HttpResponse(comment.render())


def form(request, id):
    """
    Should be called asynchronously.
    Returns the rendered comment form to reply to the comment with the given id.
    """
    comment = get_object_or_404(Comment, id=id)
    return render(request, 'comments/addform.html', {
        'object': comment,
    })


def continue_thread(request, id):
    return render(request, 'comments/continue.html', {
        'object': get_object_or_404(Comment, id=id),
    })


def new(request):
    """
    This is a special hook to bridge the gap between django's comment
    posting and asynchronous comment posting, and it's damn sexy. Django
    comment posting will be able to redirect somewhere. It puts the new
    comment id in request.GET['c']. If you redirect here, then this will
    render the comment and return the new HTML. Then you javascript
    can handle the rest.

    Note that if comments are disabled during the submission, this will 404.
    That's not necessarily a bad thing, though.
    """
    comment = get_object_or_404(Comment, id=request.GET['c'])
    return render(request, 'comments/comment.html', {
        'depth': 0,
        'allow_add': comment.ancestor().enable_comments,
        'comment': comment,
    })


def remove(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user.is_staff and request.method == 'POST':
        comment.is_removed = True
        comment.save()
        return render_just('Comment removed.')
    return render_just("Sorry Dave, but I can't do that.")
