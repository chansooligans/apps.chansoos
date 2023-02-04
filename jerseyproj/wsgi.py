"""
WSGI config for jerseyproj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/bitnami/projects/jerseystuff')
sys.path.append('/home/bitnami/projects/jerseystuff/jerseyproj')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jerseyproj.settings')
os.environ.setdefault('devmode', 'prod')

application = get_wsgi_application()
