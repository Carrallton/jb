import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-uh4us2oooi(hjf=-&5-36)ftrzt4ikv3i(0j_4&#5cjz@e4&pj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost:3000', 'broover.ru', '213.109.202.98', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'django_ckeditor_5',
    'corsheaders',
    'storages',
    'leaflet',
    'django_filters',
    'blog.apps.BlogConfig',
    'walking_routes.apps.WalkingRoutesConfig',
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

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'myblog',
#        'USER': 'broover',
#        'PASSWORD': 'Yumshanov39',
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modeltranslation settings
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru')

# Email settings
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'your-email@gmail.com'
#EMAIL_HOST_PASSWORD = 'your-email-password'

# Celery settings
#CELERY_BROKER_URL = 'redis://redis:6379/0'
#CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

customColorPalette = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
]

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 
            'numberedList', 'blockQuote', 'imageUpload', 'undo', 'redo'
        ],
        'language': 'ru',
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|', 'bulletedList', 'numberedList',
            '|', 'blockQuote', 'imageUpload'
        ],
        'toolbar': [
            'heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 
            'link', 'underline', 'strikethrough', 'code', 'subscript',
            'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing',
            'insertImage', 'bulletedList', 'numberedList', 'todoList', '|',
            'blockQuote', 'imageUpload', '|', 'fontSize', 'fontFamily',
            'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
            'insertTable', 'undo', 'redo'
        ],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                       'imageStyle:alignRight', 'imageStyle:alignCenter',
                       'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                              'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        },
        'language': 'ru'
    }
}

# Maps

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (55.75, 37.61),  # Москва
    'DEFAULT_ZOOM': 10,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'SCALE': 'both',
    'ATTRIBUTION_PREFIX': 'Walking Routes',
}

# Настройки GDAL
if os.name == 'nt':
    GDAL_LIBRARY_PATH = r'C:\OSGeo4W\bin\gdal304.dll'
    OSGEO4W = r"C:\OSGeo4W"
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
else:
    GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')