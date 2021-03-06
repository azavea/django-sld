# Django settings for djangosld project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # djsld requires a spatial database
        'NAME': 'djsld_test',
        'USER': 'djsld',
        'PASSWORD': 'djsld',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

POSTGIS_TEMPLATE = 'djsld_test'

INSTALLED_APPS = (
    'django.contrib.gis',
    'djsld',
    'djsld-test'
)
