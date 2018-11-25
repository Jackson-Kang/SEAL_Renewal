"""
Django settings for mysite2 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SESSION_EXPIRE_AT_BROWSER_CLOSE =True
SESSION_COOKIE_AGE =1440
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_AGE = 1440

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's^rn*+_r&jbt_x+x3hm8p$a2qu1pnc$1nj43wl2(oxu5esz#hv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'login',
    'rest_framework',
    'index',
    'lecture',
    'schedule',
    'course',
    'notice',
    'qna',
    'mypage',
    'mycourse',
    'functionhelper',
    'databasehelper',
    'dbbackup', # django-dbbackup
    'sugangpage',
    'django_mobile',

)
AUTH_USER_MODEL = 'auth.User'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
   
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware'
)

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/sealbackup'}

ROOT_URLCONF = 'mysite2.urls'

WSGI_APPLICATION = 'mysite2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'customdb',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'dnwnchlrkd'
      
      }
}
DATABASE_OPTIONS={
    'unix_socket' : '/tmp/mysql.sock',
}
TIME_ZONE = 'Asia/Seoul'
LANGUAGE_CODE = 'ko-kr'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_ROOT = '/home/cra/ClassSEAL/mysite2/static'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
('css', '/home/cra/ClassSEAL/mysite2/template/css'),
('js', '/home/cra/ClassSEAL/mysite2/template/js'),
('assets', '/home/cra/ClassSEAL/mysite2/template/assets'),
('html','/home/cra/ClassSEAL/mysite2/template/html'),
('m_html','/home/cra/ClassSEAL/mysite2/template/m_html'),
('m_css','/home/cra/ClassSEAL/mysite2/template/m_css'),
('m_js','/home/cra/ClassSEAL/mysite2/template/m_js'),

]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                '/home/cra/ClassSEAL/mysite2/static'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                "django_mobile.context_processors.flavour"

    ]
        },
    },
]


TEMPLATE_LOADERS = (
    "django_mobile.loader.Loader",
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader")

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

LogFile = os.path.join(os.path.dirname(__file__),"..","site.log")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LogFile,  
            'formatter': 'verbose'
        },
    },
    'loggers': {
	#'django': {
        #    'handlers': ['file'],
	#    'level' : 'DEBUG', 
	#    'propagate': True,
        #},
      'mysite2.course':{
	'handlers' : ['file'],
	'level' : 'DEBUG',
	'propagate':True
	},
 
      'mysite2.lecture': { 
            'handlers': ['file'],
            'level': 'DEBUG',    
	    'propagate':True       
 },                              
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
	
    ]

}

