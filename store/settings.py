import os
import json
from pathlib import Path
from decouple import config
import dj_database_url

# === Базовая конфигурация ===
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)

AUTH_USER_MODEL = 'accounts.User'  # пример

# Импорт GCP credentials только в продакшене
if not DEBUG:
    from google.oauth2 import service_account

# === Хосты ===
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# === Приложения ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Локальные
    'currencies',
    'anymail',
    'storages',
    'category',
    'accounts',
    'stores',
    'carts',
    'orders',
    'admin_thumbnails',
]

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Для статики
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

ROOT_URLCONF = 'store.urls'

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
                'currencies.context_processors.currencies',
            ],
        },
    },
]

WSGI_APPLICATION = 'store.wsgi.application'
AUTH_USER_MODEL = 'accounts.Account'

# === Базы данных ===
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }

# === Валидация паролей ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Язык и время ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_CURRENCY = 'KZT'

# === Статика ===
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    BASE_DIR / "stock" / "static",
]


# === Медиа ===
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# === Хранилище (GCS) ===
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = config('GS_BUCKET_NAME', default='ernur-project')
    GS_PROJECT_ID = 'ernur-project'
    GOOGLE_CREDENTIALS_JSON = config("GOOGLE_CREDENTIALS_JSON", default=None)

    if GOOGLE_CREDENTIALS_JSON:
        try:
            GOOGLE_CREDS = json.loads(GOOGLE_CREDENTIALS_JSON)
            if isinstance(GOOGLE_CREDS, str):
                GOOGLE_CREDS = json.loads(GOOGLE_CREDS)
            GS_CREDENTIALS = service_account.Credentials.from_service_account_info(GOOGLE_CREDS)
            MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
        except Exception as e:
            raise Exception(f"Google credentials load failed: {e}")

# === Email через Mailjet ===
ANYMAIL = {
    "MAILJET_API_KEY": config('MAILJET_API_KEY'),
    "MAILJET_SECRET_KEY": config('MAILJET_SECRET_KEY'),
}
EMAIL_BACKEND = config("EMAIL_BACKEND", default="anymail.backends.mailjet.EmailBackend")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="support@yourdomain.com")

# === Курс валют ===
OPENEXCHANGERATES_APP_ID = config('OPENEXCHANGERATES_APP_ID', default=None)

# === Логирование (для отладки ошибок 500) ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
