"""
WSGI config for TxerAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/DanielRiesen/TxerDjango/Venv/local/lib/python3.5/sit-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/DanielRiesen/TxerDjango')
sys.path.append('/home/DanielRiesen/TxerDjango/TxerAPI')

os.environ['DJANGO_SETTINGS_MODULE'] = 'TxerAPI.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/DanielRiesen/TxerDjango/Venv/bin/activate_this.py")
exec(open(activate_env).read(), dict(__file__=activate_env))


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TxerAPI.settings")

application = get_wsgi_application()
