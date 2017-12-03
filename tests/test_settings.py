import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'instagram_auth',
    'tests',
]
AUTH_USER_MODEL = 'instagram_auth.User'
AUTHENTICATION_BACKENDS = [
    'instagram_auth.authentication.InstagramAuthenticationBackend',
]
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
]
ROOT_URLCONF = 'tests.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
