# Meta
ROOT = '/home/nate/webapps/'
PROJNAME = 'overviewer'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'dk8rq3$(@a=%$y%7eq$1)ljo^8fd0s1aoz32+7wt9bh9rrc5#@'

# Cache

CACHE_BACKEND = 'dummy:///'
CACHE_MIDDLEWARE_SECONDS = 60 * 15

# Management

ADMINS = (
	('Nate','nate@natesoares.com'),
)

MANAGERS = ADMINS

# Databale

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'overviewer'
DATABASE_USER = 'nate'
DATABASE_PASSWORD = 'heartofgold'
DATABASE_HOST = ''
DATABASE_PORT = ''

# Emailing

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'contact@natesoares.com'
EMAIL_HOST_PASSWORD = 'the heart asks pleasure first'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Defaults

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

# Media 

MEDIA_ROOT = ROOT + PROJNAME + '/media/'

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

# Confs

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'overviewer.urls'

TEMPLATE_DIRS = (
    ROOT + PROJNAME + '/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.webdesign',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',

    'overviewer.meta',
    'overviewer.utilities',
    'overviewer.comments',
    'overviewer.tags',

    'overviewer.threads',
)

# Overrides
COMMENTS_APP = 'overviewer.comments'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'overviewer.threads.views.thread_processor',
)
