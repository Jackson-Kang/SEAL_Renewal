
import os
import sys
sys.path.append('/srv/www/mysite2')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite2.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
