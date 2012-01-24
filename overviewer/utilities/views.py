from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, RequestContext


def render_to_404(request, message):
    return render(request, '404.html', {'message': message})


def render(request, name, context=None, processors=(), instance=None):
    instance = instance or RequestContext
    return render_to_response(name, context, instance(
        request, processors=processors
    ))


def render_just(message):
    return render_to_response('just.html', {'message': message}) 
