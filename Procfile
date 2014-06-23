web: python mezzrow/manage.py syncdb --noinput; python mezzrow/manage.py migrate --merge --noinput; gunicorn --pythonpath mezzrow mezzrow.wsgi
