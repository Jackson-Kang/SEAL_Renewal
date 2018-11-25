"""
WSGI config for mysite2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os, sys
import traceback
import signal
sys.path.append('/home/cra/ClassSEAL/mysite2')
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/cra/ClassSEAL/mysite2/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite2.settings")

from django.core.wsgi import get_wsgi_application
def application(environ, start_response):
    if environ['mod_wsgi.process_group'] != '': 
        import signal
        os.kill(os.getpid(), signal.SIGINT)
    return ["killed"]
application = get_wsgi_application()
