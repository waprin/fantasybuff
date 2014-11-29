# Django settings for league project.
import os
import urlparse
import dj_redis_url
import django

PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

DEBUG = os.path.isfile(".debug_file")
if DEBUG:
    print "Debug is TRUE"
else:
    print "Debug is FALSE"


TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

YAHOO_CONSUMER_KEY           = 'dj0yJmk9YUhSTTNlZFVyQ29yJmQ9WVdrOU1GTmlXSEpxTlRRbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0xMQ--'


try:
    if os.environ['FF_LOCAL'] == 'True':
        LOCAL=True
    else:
        LOCAL=False
except KeyError:
    LOCAL = True

MANAGERS = ADMINS

try :
    YAHOO_CONSUMER_SECRET        = os.environ['YAHOO_FF_SECRET']
except KeyError:
    if LOCAL:
        YAHOO_CONSUMER_KEY = ''
    else:
        raise Exception("No YAHOO_FF_SECRET")

TEST_RUNNER = 'django.test.runner.DiscoverRunner'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'league2',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config(default='postgres://localhost:5432/league2')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y2dipx&amp;nsv^(de@-l4dp5us#72e63f)17&amp;$(a^a-6@^kd6+)&amp;g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_name_backends',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'league.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'league.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'teams', # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    'django_rq',
    'social_auth',
    # Uncomment the next line to enable admin documentation:
     #'django.contrib.admindocs',
)

AUTHENTICATION_BACKENDS = (
     'django.contrib.auth.backends.ModelBackend',
     'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
)


LOGIN_URL = '/signin/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose' : {
            'format' : '%(levelname)s %(asctime)s [%(module)s.%(funcName)s] %(message)s'
        },
        'simple': {
            'format' : '%(levelname)s %(message)s'
         }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }, 'file': {
            'level' : 'INFO',
            'class' : 'logging.FileHandler',
            'formatter': 'verbose',
            'filename' : 'leagues.log',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propogate' : True,
            'level': 'INFO',
         },
         'django.request': {
            'handlers': ['console'],
            'propogate' : True,
            'level' : 'INFO',
           },
         'teams' : {
            'handlers' : ['console', 'file'],
            'propogate' : True,
            'level' : 'DEBUG',
         }
    }
}

redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))
#LOCAL_REDIS='redis://localhost:6379'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
            'IGNORE_EXCEPTIONS': True,
            'CONNECTION_POOL_KWARGS': {'max_connections': 10}
        },
        'KEY_PREFIX' : 'FBUFF_'
    }
}

RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
        'DEFAULT_TIMEOUT': 2000,
    },
    'low': {
        'USE_REDIS_CACHE': 'default',
        'DEFAULT_TIMEOUT': 2000,
    },
}

#REDIS = {"default": dj_redis_url.config(env='REDISTOGO_URL', default=LOCAL_REDIS), "low": dj_redis_url.config(env='REDISTOGO_URL', default=LOCAL_REDIS)}
#RQ_QUEUES = REDIS
#REDIS['default']['DEFAULT_TIMEOUT'] = 1800
#REDIS['low']['DEFAULT_TIMEOUT'] = 1800


try:
    ALLOW_SIGNUPS = os.environ['FF_ALLOW_SIGNUPS']
except KeyError:
    ALLOW_SIGNUPS = True

DB_SCRAPE=True
