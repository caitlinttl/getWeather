application: python application.py
web: gunicorn --bind :8000 --workers 3 --threads 2 project.wsgi:application
weatherLineNotify: python weatherLineNotify.py