"""
Django settings for GSI project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ht!6=9x07@-1v9p8&f9x2v19d57cja_4g!k%nrjnwo34j8cj+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'solo',
    'registration',
    'crispy_forms',

    'ckeditor',
    'ckeditor_uploader',

    'cards',
    'gsi',
    'customers',
    'log',
    'tags',
    'articles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'gsi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'gsi.context_processors.get_current_year',
            ],
        },
    },
]

WSGI_APPLICATION = 'gsi.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
                       "django.contrib.staticfiles.finders.AppDirectoriesFinder")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "collected_static/")
STATIC_DIR = STATICFILES_DIRS[0]
STATIC_URL = '/static/'

DEBUG_TOOLBAR_PATCH_SETTINGS = True
ENABLE_DEBUG_TOOLBAR = False

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAdminUser',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGINATE_BY': 10
}

# home folder for new cripts
SCRIPTS_HOME = '/lustre/w23/mattgsi/'

# settings for django-registration-redux
REGISTRATION_OPEN = True
LOGIN_URL = 'users:auth_login'
LOGOUT_URL = 'users:auth_logout'

# to send the activation code
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# DEFAULT_FROM_EMAIL = 'info@google.ru'

# mailgun settings
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.mailgun.org'
# EMAIL_HOST_USER = 'postmaster@sandboxb0a57a3959a74e848bcdde911debdc02.mailgun.org'
# EMAIL_HOST_PASSWORD = 'b8eaad09132286b3742260a52dbcba6a'
# EMAIL_PORT = 587

# send email for forgot password
# EMAIL_USE_TLS = True
MAIL_USE_SSL = True
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 12333
EMAIL_HOST_USER = 'user@user.post.com'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'noreply@exemple.com'
EMAIL_BACKEND = 'smtp.backend'

# Logging settings for django projects
MAIN_FILE = os.path.join(BASE_DIR, "core/main.log")
MAIN_DEBUG_FILE = os.path.join(BASE_DIR, "core/main_debug.log")

# # Time Format
# TIME_FORMAT = (
#     '%H:%M:%S.%f',  # '14:30:59.000200'
# )

# Logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '==============  %(levelname)s:%(name)s:::: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': MAIN_FILE,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': MAIN_DEBUG_FILE,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'null': {
            "class": 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': "DEBUG",
        },
    }
}

EXECUTE_FE_COMMAND = '/home/gsi/gsi_files/bin/execute_FE_command'
FE_SUBMIT = '/home/w23/mattgsi/bin/fe_submit'
PATH_RUNS_SCRIPTS = '/lustre/w23/mattgsi/scripts/runs'
PROCESS_NUM = 10
CONFIGFILE_PATH = '$RF_AUXDATA_DIR/'

# results_directory
RESULTS_DIRECTORY = '/lustre/w23/mattgsi/satdata/RF/Projects/'
POLYGONS_DIRECTORY = '/lustre/w23/mattgsi/satdata/RF/Polygons/kml/'

# number paginations
NUM_PAGINATIONS = 7

# number execute runs
EXEC_RUNS = 2000

# Google maps
GOOGLE_MAP_ZOOM = 11
DAFAULT_LAT = 63.817957
DAFAULT_LON = -151.147061
PNG_PATH = 'media/png'
TIF_PATH = 'media/tif'

# Card Type
CARD_TYPE = {
    'rftrain': 'RFTrain',
    'mergecsv': 'MergeCSV',
    'preproc': 'PreProc',
    'collate': 'Collate',
    'yearfilter': 'YearFilter',
    'remap': 'Remap',
    'rfscore': 'RFScore',
    'qrf': 'QRF',
    'randomforest': 'RandomForest',
    'calcstats': 'CalcStats'
}

try:
    from settings_local import *
except ImportError:
    pass

if ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
