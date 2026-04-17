release: mkdir -p staticfiles && python manage.py migrate && python manage.py collectstatic --noinput
web: python -m gunicorn portfolio_project.wsgi --log-file -