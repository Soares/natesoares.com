import os
import sys

sys.path = ['/home/soares/webapps/myapache', '/home/soares/webapps/myapache/entrar', '/home/soares/webapps/myapache/lib/python2.6'] + sys.path
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'entrar.settings'
application = WSGIHandler()
