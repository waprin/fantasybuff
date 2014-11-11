web: gunicorn league.wsgi --log-file -

urgentworker: python manage.py rqworker default 
worker: python manage.py rqworker low
