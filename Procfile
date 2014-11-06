web: gunicorn league.wsgi --log-file -

worker-high: python manage.py rqworker default 
worker-low: python manage.py rqworker low
