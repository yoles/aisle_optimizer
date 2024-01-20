from api.settings.base import * # noqa

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1', "api"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost/",
    "http://127.0.0.1/",
    "http:/0.0.0.0/",
]

# https://testdriven.io/blog/django-spa-auth/
# https://parthkoshta.medium.com/dockerize-your-react-django-rest-api-application-and-serve-using-nginx-6f9ccf17105b
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1', "http://0.0.0.0"]

# PROD ONLY
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True