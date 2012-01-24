from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.http import Http404
from personal.utilities.decorators import gets_tags
from personal.utilities.views import top, top_changes
from personal.writing.models import Entry

def new(request):
	try:
		first = Entry.objects.order_by('-published')[0]
	except IndexError:
		return render_to_response('welcome.html')
	view, args, kwargs = resolve(first.get_absolute_url())
	kwargs['request'] = request
	try:
		return view(*args, **kwargs)
	except Http404:
		return render_to_response('welcome.html')


@gets_tags
def updates(request, tags):
    try:
        count = int(request.GET.get('count'))
    except (TypeError, ValueError):
        count = 12
    return render_to_response('updates.html', {
        'items': top(count, tags),
        'count': count,
        'tags': tags,
    })


@gets_tags
def changes(request, tags):
    try:
        count = int(request.GET.get('count'))
    except (TypeError, ValueError):
        count = 12
    return render_to_response('changes.html', {
        'items': top_changes(count, tags),
        'count': count,
        'tags': tags,
    })
