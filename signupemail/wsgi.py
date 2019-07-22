"""
WSGI config for signupemail project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signupemail.settings')
os.environ['https_proxy'] = "http://proxy.127.0.0.1:8000"

application = get_wsgi_application()
