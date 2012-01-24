from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from overviewer.utilities.views import render
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    name = request.POST['username']
    password = request.POST['password']
    next = request.POST.get('next', '/')
    if request.POST.get('honeypot'):
        return redirect(next)
    if User.objects.filter(username=name).count():
        return render(request, 'registration/login.html', {
            'next': next,
            'collision': True,
            'form': AuthenticationForm(request),
        })
    user = User.objects.create_user(name, '', password)
    user.save()
    user = authenticate(username=name, password=password)
    login(request, user)
    return redirect(next)
