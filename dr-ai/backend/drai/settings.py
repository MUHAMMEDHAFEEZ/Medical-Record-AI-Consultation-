import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qz$ru@(bfs+3s-3ornbw925kct0%9frhh$k5@si1sw8^53q@j_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [
#     'localhost',
#     '127.0.0.1',
#     'rj8vq174-8000.uks1.devtunnels.ms',
#     "localhost:8000",
#     "localhost:5173",
#     "localhost:5174",
#     "localhost:5175",
#     "rj8vq174-5173.uks1.devtunnels.ms",
#     "rj8vq174-8000.uks1.devtunnels.ms",
#     "rj8vq174-8000.uks1.devtunnels.ms",
#     "rj8vq174-5173.uks1.devtunnels.ms",
# ]
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.authentication',
    'apps.medical_records',
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

ROOT_URLCONF = 'drai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'drai.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'authentication.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://localhost:5173",
#     "http://localhost:5174",
#     "http://localhost:5175",
#     "https://rj8vq174-5173.uks1.devtunnels.ms",
#     "https://rj8vq174-8000.uks1.devtunnels.ms",
#     "https://rj8vq174-8000.uks1.devtunnels.ms",
#     "https://rj8vq174-5173.uks1.devtunnels.ms",
# ]

# Admin Interface settings
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

# Admin branding
ADMIN_SITE_HEADER = "DR AI Administration"
ADMIN_SITE_TITLE = "DR AI Admin Portal"
ADMIN_INDEX_TITLE = "Welcome to DR AI Administration"

# Admin Interface Theme settings
ADMIN_INTERFACE_THEME_SETTINGS = {
    'name': 'DR AI Theme',
    'active': True,
    'title': 'DR AI Admin',
    'title_visible': False,  # We'll handle the title in our custom template
    'logo_visible': False,   # We'll handle the logo in our custom template
    'logo_max_height': 35,
    'logo_max_width': 180,
    'css_header_background_color': '#2c3e50',
    'css_header_text_color': '#FFFFFF', 
    'css_header_link_color': '#FFFFFF',
    'css_header_link_hover_color': '#3498db',
    'css_module_background_color': '#3498db',
    'css_module_text_color': '#FFFFFF',
    'css_module_link_color': '#FFFFFF',
    'css_module_link_hover_color': '#2c3e50',
    'css_generic_link_color': '#3498db',
    'css_generic_link_hover_color': '#2c3e50',
    'css_save_button_background_color': '#3498db',
    'css_save_button_background_hover_color': '#2c3e50',
    'css_save_button_text_color': '#FFFFFF',
    'css_delete_button_background_color': '#e74c3c',
    'css_delete_button_background_hover_color': '#c0392b',
    'css_delete_button_text_color': '#FFFFFF',
    'list_filter_dropdown': True,
    'related_modal_active': True,
    'related_modal_background_color': '#000000',
    'related_modal_background_opacity': 0.8,
    'list_filter_sticky': True,
    'form_submit_sticky': True,
    'form_pagination_sticky': True,
}
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')