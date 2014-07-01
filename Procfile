web: python mezzrow/manage.py syncdb --noinput; python mezzrow/manage.py migrate --merge --noinput; newrelic-admin run-program gunicorn --pythonpath mezzrow mezzrow.wsgi
