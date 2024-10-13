web: gunicorn jobber.wsgi:application --bind 0.0.0.0:$PORT
release: python3 manage.py migrate --no-input