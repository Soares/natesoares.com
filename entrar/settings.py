from local_settings import *

# Global

PROJNAME = 'entrar'
ADMINS = ('Nate','nate@natesoares.com'),
MANAGERS = ADMINS
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
ROOT_URLCONF = PROJNAME + '.urls'

# Email

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'contact@natesoares.com'
EMAIL_HOST_PASSWORD = 'the heart asks pleasure first'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Media

MEDIA_ROOT = ROOT + PROJNAME + MEDIA_URL
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Templates

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    ROOT + PROJNAME + '/templates'
)

# Apps

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.webdesign',

    'entrar.utilities',
    'entrar.entries',
)
