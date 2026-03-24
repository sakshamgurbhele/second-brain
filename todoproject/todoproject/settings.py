from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security -----------------------------------------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-only-change-in-production')
DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,172.31.9.223,54.78.97.183,sakshamm.duckdns.org').split(',')
CSRF_TRUSTED_ORIGINS = ['https://sakshamm.duckdns.org']

# Secure cookies (set to True when running HTTPS)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hour
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    'todoproject.mongo_apps.MongoAuthConfig',
    'todoproject.mongo_apps.MongoContentTypesConfig',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todoproject.mongo_apps.MongoAxesConfig',
    'todos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Lock out after 5 failed attempts for 1 hour
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hours
AXES_LOCKOUT_PARAMETERS = ['ip_address']
AXES_RESET_ON_SUCCESS = True

ROOT_URLCONF = 'todoproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'todoproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'HOST': os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/'),
        'NAME': 'todoapp',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'

MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,
    'sessions': None,
    'axes': None,
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Dublin'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB limit

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

BASE_PASSWORD = os.environ.get('BASE_PASSWORD', '')
