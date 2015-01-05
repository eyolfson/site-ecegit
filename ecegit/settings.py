# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

"""
Django settings for site-ecegit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ssh',
    'django_gitolite',
    'django_gitolite_repositories',
    'emailer',
    'courses',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'ecegit.urls'
WSGI_APPLICATION = 'ecegit.wsgi.application'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
SECRET_KEY = 'SECRET_KEY'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Templates
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Databases
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-ca'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

# Auth
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# CAS
AUTHENTICATION_BACKENDS = (
    'django_cas.backends.CASBackend',
)
MIDDLEWARE_CLASSES += ('django_cas.middleware.CASMiddleware',)
CAS_SERVER_URL = 'https://cas.uwaterloo.ca/cas/'

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# Gitolite
GITOLITE_USER = 'git'
GITOLITE_HOOKS = (
    'emailer.hooks.email',
)
