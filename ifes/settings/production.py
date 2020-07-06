import os
from configurations import values
from memcacheify import memcacheify
from .base import Base

try:
    from boto.s3.connection import OrdinaryCallingFormat
    AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
except ImportError:
    # TODO: Fix this where even if in Dev this class is called.
    pass


class Production(Base):


    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

    SECRET_KEY = values.SecretValue()

    CACHES = memcacheify()

    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_HOST_USER = values.SecretValue()
    EMAIL_PORT = int(587)
    EMAIL_HOST_PASSWORD = values.SecretValue()
    EMAIL_SUBJECT_PREFIX = 'Eguide:'
    DEFAULT_FROM_EMAIL = 'electionguide@ifes.org'
    SERVER_EMAIL = 'electionguide@ifes.org'

    MAILGUN_API_KEY = values.SecretValue()
    MAILGUN_DOMAIN = 'mg.electionguide.org'
    MAILGUN_MAILINGLIST = 'newsletter@mg.electionguide.org'

    # STORAGE CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/index.html
    INSTALLED_APPS = Base.INSTALLED_APPS + (
        'storages',
    )

    RECAPTCHA_PUBLIC_KEY = values.SecretValue()
    RECAPTCHA_PRIVATE_KEY = values.SecretValue()

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = values.SecretValue()
    AWS_SECRET_ACCESS_KEY = values.SecretValue()
    AWS_STORAGE_BUCKET_NAME = values.SecretValue()
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
