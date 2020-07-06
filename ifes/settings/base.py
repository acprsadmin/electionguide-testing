# Django settings for ifes project.
from os.path import join, dirname

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from configurations import Configuration, values

BASE_DIR = dirname(join(dirname(__file__), '../../'))


class Base(Configuration):

    BASE_DIR = BASE_DIR

    DEBUG = values.BooleanValue(False)

    ADMINS = (
        ('AJ', 'jazayeri@gmail.com'),
    )
    #
    # MANAGERS = ADMINS

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # In a Windows environment this must be set to your system time zone.
    TIME_ZONE = 'America/New_York'

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = 'en-us'

    SITE_ID = 1

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False

    # If you set this to False, Django will not format dates, numbers and
    # calendars according to the current locale.
    USE_L10N = True

    # If you set this to False, Django will not use timezone-aware datetimes.
    USE_TZ = True

    # STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(dirname(BASE_DIR), 'staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    # END STATIC FILE CONFIGURATION

    # MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    # END MEDIA CONFIGURATION

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'change me!'

    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    MIDDLEWARE_CLASSES = (
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    ROOT_URLCONF = 'ifes.urls'

    DATABASES = values.DatabaseURLValue('sqlite:///%s' % join(BASE_DIR, 'db.sqlite3'))

    # Python dotted path to the WSGI application used by Django's runserver.
    WSGI_APPLICATION = 'wsgi.application'

    TEMPLATE_DIRS = (
        join(BASE_DIR, 'ifes/templates'),
    )

    TEMPLATE_CONTEXT_PROCESSORS = TCP + (
        'django.core.context_processors.request',
        'djangojs.context_processors.booleans',
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",

    )

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'django.contrib.sitemaps',
        # Uncomment the next line to enable the admin:
        'suit',
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        # 'smart_selects',
        'autocomplete_light',
        'eztables',
        's3_folder_storage',
        'tagging',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'captcha',
        'eguide',
        'mailgun',
        'sorl.thumbnail',
        'rest_framework',
        'rest_framework_swagger',
        'rest_framework.authtoken',
        'api',
        'ckeditor',
        'corsheaders',
    )


    REST_FRAMEWORK = {
        'PAGINATE_BY': 100,  # Default to 10
        'PAGINATE_BY_PARAM': 'page_size',   # Allow client to override, using `?page_size=xxx`.
        'MAX_PAGINATE_BY': 1000,            # Maximum limit allowed when using `?page_size=xxx`.

        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',  # <-- And here
            #'rest_framework.authentication.SessionAuthentication',
        ],
    }


    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",

        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    AUTH_USER_MODEL = 'eguide.EguideUser'

    LOGIN_REDIRECT_URL = '/myeguide/'
    LOGIN_URL = '/myeguide/login'

    # AllAuth settings

    ACCOUNT_AUTHENTICATION_METHOD = "username_email"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_UNIQUE_EMAIL = True

    SUIT_CONFIG = {
        # header
        'ADMIN_NAME': 'Election Guide - IFES',

        'MENU': (
            # Separator
            '-',

            # Custom app and model with permissions
            {'label': 'Country Data',
             'icon': 'icon-globe',
             'models': ['eguide.country',
                        'eguide.institution',
                        'eguide.region',
                        'eguide.institution_type',
                        'eguide.election_system'
                        ]
             },

            # Separator
            '-',

            {'label': 'Election Data',
             'icon': 'icon-ok',
             'models': ['eguide.election',
                        'eguide.provision_votes',
                        'eguide.party',
                        'eguide.person',
                        'eguide.election_status',
                        'eguide.party_type',
                        'eguide.election_type'
                        ]
             },

            # Separator
            '-',

            # Custom app, with models
            {'label': 'Digest',
             'icon': 'icon-pencil',
             'models': ['eguide.digest',
                        'eguide.author',
                        'eguide.category',
                        'eguide.newsletter'
                        ]
             },

            # Separator
            '-',

            # Custom app, with models
            {'label': 'Settings',
             'icon': 'icon-cog',
             'models': ['eguide.page',
                        'eguide.eguideuser',
                        'auth.group'
                        ]
             },
        )
    }

    #REST_FRAMEWORK = {
    #    'PAGINATE_BY': 100,                 # Default to 10
    #    'PAGINATE_BY_PARAM': 'page_size',   # Allow client to override, using `?page_size=xxx`.
    #    'MAX_PAGINATE_BY': 1000             # Maximum limit allowed when using `?page_size=xxx`.
    #}

    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

    SWAGGER_SETTINGS = {
        'exclude_namespaces': [],
        'api_version': '1.0',
        'api_path': '/',
        'enabled_methods': [
            'get',
        ],
        'info': {
            'contact': 'info@ifes.org',
            'description': 'API Documentation',
            'license': '',
            'licenseUrl': '',
            'termsOfServiceUrl': '',
            'title': 'Election Guide',
        },
        'doc_expansion': 'none',
    }

    RECAPTCHA_PUBLIC_KEY = 'somekey'
    RECAPTCHA_PRIVATE_KEY = 'somekey'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    CKEDITOR_UPLOAD_PATH = "uploads/"
    CKEDITOR_IMAGE_BACKEND = 'pillow'

    ck_editor_toolbar_full = [
        {'name': 'document', 'groups': ['mode', 'document', 'doctools'],
                             'items': ['Source', 'Save', 'NewPage', 'DocProps', 'Preview',
                                       'Print', 'Templates', 'document']},
        {'name': 'editing', 'groups': ['find', 'selection', 'spellchecker'],
                            'items': ['Find', 'Replace', 'SelectAll', 'Scayt']},
        {'name': 'insert', 'items': ['CreatePlaceholder', 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley',
                                     'SpecialChar', 'PageBreak', 'Iframe', 'InsertPre']},
        '/',
        {'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup'],
                                'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript',
                                          'RemoveFormat']},
        {'name': 'paragraph', 'groups': ['list', 'indent', 'blocks', 'align'],
                              'items': ['NumberedList', 'BulletedList', 'Outdent', 'Indent', 'Blockquote',
                                        'CreateDiv', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
                                        'BidiLtr', 'BidiRtl']},
        {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
        '/',
        {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
        {'name': 'colors', 'items': ['TextColor', 'BGColor']},
        {'name': 'tools', 'items': ['UIColor', 'Maximize', 'ShowBlocks']},
        {'name': 'about', 'items': ['About']}
    ]

    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': ck_editor_toolbar_full,
            "removePlugins": "stylesheetparser",
        },
        'custom_newsletter': {
            'toolbar': 'Basic',
            'fullPage': True,
            'allowedContent': True
        }

    }

    CORS_ORIGIN_ALLOW_ALL = values.BooleanValue(True)
    CORS_URLS_REGEX = r'^/api/.*$'
    CORS_ALLOW_METHODS = (
        'GET',
        'HEAD',
        'OPTIONS',
    )
