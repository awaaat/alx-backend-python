from pathlib import Path
import environ  # type: ignore
from datetime import timedelta

  # Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # reads .env file from BASE_DIR by default

  # Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

  # SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default='django-insecure-j=&t1t8$$8jc-6-tg1z2!axxzg566vx^(^nqu*@cw442p2d*d1')  # type: ignore

DEBUG = env.bool("DEBUG", default=True)  # type: ignore

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add localhost for development

  # Application definition
INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      # added apps
      'rest_framework',
      'chats',
      'drf_yasg',
      'rest_framework_simplejwt',
      'corsheaders',
  ]

MIDDLEWARE = [
      'corsheaders.middleware.CorsMiddleware',  # Must be at the top
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
  ]

ROOT_URLCONF = 'messaging_app.urls'

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

WSGI_APPLICATION = 'messaging_app.wsgi.application'

  # PostgreSQL Database Configuration from .env
DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': env("DB_NAME"),
          'USER': env("DB_USER"),
          'PASSWORD': env("DB_PASSWORD"),
          'HOST': env("DB_HOST"),
          'PORT': env("DB_PORT"),
      }
  }

  # Password validation
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

  # REST framework default authentication & permission
REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework_simplejwt.authentication.JWTAuthentication',
          'rest_framework.authentication.BasicAuthentication',
          'rest_framework.authentication.SessionAuthentication',
      ],
      'DEFAULT_PERMISSION_CLASSES': [
          'rest_framework.permissions.IsAuthenticated',
      ],
      'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
      'PAGE_SIZE': 20,
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
      'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
      'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
      'ROTATE_REFRESH_TOKENS': False,
      'BLACKLIST_AFTER_ROTATION': False,
      'AUTH_HEADER_TYPES': ('Bearer',),
      'USER_ID_FIELD': 'user_id',
      'USER_ID_CLAIM': 'user_id',
}

AUTH_USER_MODEL = 'chats.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
 "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True  # Allow credentials (like tokens)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'