"""
Django settings for wganmgr project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2grl6bv%e6ngdh8at2w$fr$n3#s1vd6w2s&jlrs(!shd=x31+l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ["192.168.1.199","127.0.0.1","localhost"]
else:
    ALLOWED_HOSTS = ["*"]


# Application definition

if DEBUG:
    INSTALLED_APPS = [
        'wganbrowser.apps.WganbrowserConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
else:
    INSTALLED_APPS = [
        'wganbrowser.apps.WganbrowserConfig',
    #   'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
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

ROOT_URLCONF = 'wganmgr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'wganmgr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_wganmgr',
        'USER': 'django',
        'PASSWORD': 'EggFishPants99DJ',
        'HOST': '192.168.1.199',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
if DEBUG:
    LOGIN_REDIRECT_URL = '/wganbrowser/models'
else:
    LOGIN_REDIRECT_URL = '/a/wganbrowser/models'
    LOGIN_URL = '/a/accounts/login'    

# email needs setting up, in the meantime emails go to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STATIC_ROOT = "/var/www/html/static"
#wganbrowser specific
if DEBUG:
    JENKINS_URL='http://matt-desktop.local:8080/'
else:
    JENKINS_URL='http://matt-desktop.local:8080/'

JENKINS_USER='matt'
JENKINS_PWD='matt'

JENKINS_TRAIN_JOB="wgan-train-and-upload"
JENKINS_WAVEGAN_REPO_ROOT='/home/matt/dev/git_repos/wavegan'
JENKINS_PYENV_ACTIVATE='source ~/dev/venvs/tf/bin/activate'

JENKINS_TRAINING_NODES=['ubuntu-wavegan-2222']
JENKINS_PASSTHROUGH_JOB='wganmgr-shell-passthrough'

JENKINS_DB_HOST_SSH_CREDENTIALS_ID='' #if empty, jenkins will rely on node user ssh .conif & pwdless access setup
                                      #otherwise ssh keypair credentials
JENKINS_DB_HOST_SSH_USERNAME='' #if empty will use jenkins node process username
JENKINS_DB_HOST_SQL_CREDENTIALS_ID='django_mysql' #mysql username, password credentials
JENKINS_DB_HOST_SQL_DB_NAME='django_wganmgr' #mysql DB name
JENKINS_DB_HOST_ADDRESS='ubuntu-1' #192.168.1.199

JENKINS_STORAGE_HOST_SSH_CREDENTIALS_ID='' #if empty, jenkins will rely on node user ssh .conif & pwdless access setup
                                           #otherwise ssh keypair credentials
JENKINS_STORAGE_HOST_ADDRESS='ubuntu-1' #192.168.1.199
JENKINS_STORAGE_HOST_STORAGE_ROOT='/home/matt/incoming_models'

JENKINS_APP_HOST_SSH_CREDENTIALS_ID='' #if empty, jenkins will rely on node user ssh .conif & pwdless access setup
                                       #otherwise ssh keypair credentials
JENKINS_APP_HOST_ADDRESS='ubuntu-1'

#construct model url from model path name
#See also wgan-publish-model.groovy SNAPSHOT_PACKAGES_FS_ROOT
MODEL_SNAPSHOT_PACKAGES_WEBROOT='/wlse/models'
MODEL_SNAPSHOT_PACKAGES_FS_ROOT='/var/www/html/wlse/models'

#how we exec shell commands on the training node
TRAINING_HOST_EXECUTION_MODE='JENKINS_PASSTHROUGH' #or SSH

NODE_STORAGE_ROOT='/home/matt'