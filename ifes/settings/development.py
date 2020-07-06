from configurations import values
from memcacheify import memcacheify
from .base import Base


class Development(Base):

    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG

    INSTALLED_APPS = Base.INSTALLED_APPS
    INSTALLED_APPS += ('debug_toolbar',)

    # Email Configs
    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_HOST_USER = 'postmaster@mg.electionguide.org'
    EMAIL_PORT = int(587)
    EMAIL_HOST_PASSWORD = 'test'
    EMAIL_SUBJECT_PREFIX = 'Eguide:'
    DEFAULT_FROM_EMAIL = 'electionguide@ifes.org'
    SERVER_EMAIL = 'electionguide@ifes.org'

    MAILGUN_API_KEY = 'test'
    MAILGUN_DOMAIN = 'mg.electionguide.org'
    MAILGUN_MAILINGLIST = 'newsletter@mg.electionguide.org'

    THUMBNAIL_DEBUG = True

    MIDDLEWARE_CLASSES = Base.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

    # STORAGE CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/index.html
    INSTALLED_APPS += (
        'storages',
    )
    # SJM----- the below media commands are needed to force Digest uploads to save locally.
    # you need to create a direcotry "media" under the root directory
    #MEDIA_ROOT = 'media/'
    #MEDIA_URL = 'media/'

    #SITE_ROOT = os.path.dirname(__file__)
    #THUMBNAIL_DEBUG = True
    MEDIA_ROOT = 'media/'
    MEDIA_URL = 'media/'


    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    #STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = values.Value('key')
    AWS_SECRET_ACCESS_KEY = values.Value('value')
    AWS_STORAGE_BUCKET_NAME = values.Value('eguide')
    AWS_AUTO_CREATE_BUCKET = False
    AWS_QUERYSTRING_AUTH = values.BooleanValue(False)

    # see: https://github.com/antonagestam/collectfast
    AWS_PRELOAD_METADATA = True

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIRY = 60 * 60 * 24 * 7
    AWS_HEADERS = {
        'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (
            AWS_EXPIRY, AWS_EXPIRY)
    }

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    try:
        STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME.setup('AWS_STORAGE_BUCKET_NAME')
    except ValueError:
        pass

    # END STORAGE CONFIGURATION

    CACHES = memcacheify()

    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ifes2020_e',
        'USER': 'ifesadmin',
        'PASSWORD': 'stR8t0nrED',
        'HOST': 'localhost',
        'PORT': '',
        }
    }
