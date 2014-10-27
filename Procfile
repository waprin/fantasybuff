web: gunicorn league.wsgi --log-file -

worker: python manage.py rqworker default 
worker: python manage.py rqworker low
