"""
WSGI config for infra_tester project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infra_tester.settings')

application = get_wsgi_application()
