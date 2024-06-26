from datetime import timedelta
from os.path import join as path_join
from pathlib import Path

from decouple import config


# Load env vars
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
EMAIL_SERVICE_API_KEY = config('EMAIL_SERVICE_API_KEY')
APP_NAME = config('APP_NAME')
USER_SELF_REGISTRATION_ENABLED = config('USER_SELF_REGISTRATION_ENABLED', default=False, cast=bool)
CS__ALLOWED_HOSTS = config('CS__ALLOWED_HOSTS')
CS__CORS_ORIGIN_WHITELIST = config('CS__CORS_ORIGIN_WHITELIST')
FRONTEND_BASE_URL = config('FRONTEND_BASE_URL')
BACKEND_BASE_URL = config('BACKEND_BASE_URL')
CLOUD_STORAGE_BASE_URL = config('CLOUD_STORAGE_BASE_URL')
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT', cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)
REDIS_PASSWORD = config('REDIS_PASSWORD', default=None)


ALLOWED_HOSTS=["*"] if DEBUG else CS__ALLOWED_HOSTS.split(',')

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
# CORS_ORIGIN_WHITELIST = ["*"] # CS__CORS_ORIGIN_WHITELIST.split(',')
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'core',
    'frontend_core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path_join(BASE_DIR, "build"),
            path_join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_app.wsgi.application'
AUTH_USER_MODEL = 'core.CustomUser'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = path_join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    path_join(BASE_DIR, "build"),
    path_join(BASE_DIR, "build/static"),
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PASSWORD_RESET_JWT_EXPIRY_TIMEDELTA = timedelta(minutes=15)
PASSWORD_RESET_JWT_EXPIRY_TIMEDELTA_IN_WORDS = "15 minutes"
USER_INVITE_JWT_EXPIRY_TIMEDELTA = timedelta(days=7)
USER_INVITE_JWT_EXPIRY_TIMEDELTA_IN_WORDS = "7 days"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15) if DEBUG else timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}