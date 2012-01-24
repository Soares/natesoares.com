from django.shortcuts import get_object_or_404
from utilities.views import render
from models import Entry

def entry(request, slug):
    entry = get_object_or_404(Entry, slug=slug)
    if request.user.is_staff and 'publish' in request.POST:
        entry.publish()
    if request.user.is_staff and 'pull' in request.POST:
        entry.pull()
    entry.shown = entry.shown_to(request.user)
    return render(request, 'entry.html', {'object': entry})
