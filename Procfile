release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn portfolio_project.wsgi --log-file -

