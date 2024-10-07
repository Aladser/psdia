# Личный дневник

## Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными *.env.example*.
+ ``python manage.py createusers`` - создать пользователей
+ ``python manage.py seed`` - сидирование таблиц
+ ``celery -A config worker -l INFO`` - запуск отложенных задач

## Запуск на nginx (Ubuntu)
+ скопировать *install/psdia.service* -> */etc/systemd/system/*
+ скопировать *install/psdia* -> */etc/nginx/sites-available/*
+ ``ln -s /etc/nginx/sites-available/psdia /etc/nginx/sites-enabled/psdia``
+ расскомментировать ``STATIC_ROOT = os.path.join(BASE_DIR, 'static')`` в *settings.py*, выполнить
```python manage.py collectstatic```
Для работы runserver закомментировать строку обратно
