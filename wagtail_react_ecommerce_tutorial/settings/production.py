from .base import *

# @39:00: https://www.youtube.com/watch?v=6DI_7Zja8Zc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=17
import django_heroku


DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())                 # https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html



"""Whitenoise Static Files"""
django_heroku.settings(locals(), staticfiles=False)                                                    # @39:00: https://www.youtube.com/watch?v=6DI_7Zja8Zc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=17
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'     # See: https://wagtail.io/blog/deploying-wagtail-heroku/
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


"""AWS"""
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
#AWS_S3_FILE_OVERWRITE = False                                       # When saving file with same name instead of overwriting the old one, rename the new one. (django-storages docs: https://django-storages.readthedocs.io/en/latest/)
AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

INSTALLED_APPS += [
    'storages',
]



"""Deployment Security"""
# Honor the 'X-Forwarded-Proto header for request.is_secure()
# See @ 10:00 - https://www.youtube.com/watch?v=RQ0eKv6HrpM
""" SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') """

# Deployment checklist: https://www.youtube.com/watch?v=_mgMth4im9E
""" SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool) """

#SECURE_HSTS_SECONDS = 31536000
""" SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool)

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)

SECURE_REFERRER_POLICY = config('SECURE_REFERRER_POLICY', default='no-referrer')

SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=False, cast=bool)
 """


try:
    from .local import *
except ImportError:
    pass
