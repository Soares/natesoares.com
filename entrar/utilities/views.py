from django.shortcuts import render_to_response
from django.template import RequestContext


def render(request, name, context=None, instance=None, processors=()):
    instance = instance or RequestContext
    return render_to_response(name, context, instance(
        request, processors=processors
    ))
