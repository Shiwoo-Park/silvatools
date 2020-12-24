# ===== Pure Django =====

# create django app
python manage.py startapp {APP_NAME}

# create admin
python manage.py createsuperuser

# execute django shell
python manage.py shell --settings=silvatools.settings.local

# ===== Django Extenstion =====

# execute script with django settings
python manage.py runscript {FILE_NAME} --settings=silvatools.settings.local --script-args arg1 arg2

# execute django shell
# : show sql, auto import basic modules
python manage.py shell_plus --settings=silvatools.settings.local --print-sql

