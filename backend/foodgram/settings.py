import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', default='secret_key')

DEBUG = bool(os.getenv('DEBUG', default='false'))

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', default='*')]

ENTER_COOKING_TIME = 'Время приготовления'
ENTER_DESCRIPTION = 'Описание'
ENTER_HEX = 'HEX-код цвета'
ENTER_IMAGE = 'Изображение'
ENTER_INGREDIENT_NAME = 'Название ингредиента'
ENTER_QUANTITY_INGREDIENTS = 'Количество ингредиентов'
ENTER_SLUG = 'Slug'
ENTER_TAG = 'Название тега'
ENTER_TIME_CREATION = 'Дата и время создания'
ENTER_UNIT = 'Единица измерения'

MAX_LENGTH_INGREDIENT_NAME = 200
MAX_LENGTH_INGREDIENT_UNIT = 20
MAX_LENGTH_RECIPE_NAME = 200
MAX_LENGTH_TAG_COLOR = 7
MAX_LENGTH_TAG_NAME = 22
MAX_LENGTH_TAG_SLUG = 200
MAX_VALUE_COOKING_TIME = 4320
MIN_VALUE_COOKING_TIME = 1

PAGE_SIZE = 6

LENGTH_OF_FIELDS_USER = 150
LENGTH_OF_FIELDS_USERNAME = 254


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',

    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'foodgram.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv(
            'DB_ENGINE', default='django.db.backends.postgresql'
        ),
        'NAME': os.getenv('DB_NAME', default="postgres"),
        'USER': os.getenv('POSTGRES_USER', default="postgres"),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', default="127.0.0.1"),
        'PORT': os.getenv('DB_PORT', default='5432')
    }
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'SEARCH_PARAM': 'name',
}

DJOSER = {
    'HIDE_USERS': False,
    'SERIALIZERS': {
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    }
}


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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
