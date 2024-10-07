# Личный дневник

## Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными *.env.example*. Настроить папку виртуального окружения так, чтобы путь до gurnicorn был:
``/venv/bin/gunicorn``
+ ``python manage.py createusers`` - создать пользователей
+ ``python manage.py seed`` - сидирование таблиц
+ ``celery -A config worker -l INFO`` - запуск отложенных задач


## Запуск на nginx (Ubuntu)
+ скопировать *install/psdia.service* -> */etc/systemd/system/*
+ скопировать *install/psdia* -> */etc/nginx/sites-available/*
+ ``ln -s /etc/nginx/sites-available/psdia /etc/nginx/sites-enabled/psdia``
+
  * Для копирования css стилей в папку static установить в settings.py:
    ```
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    #STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    ```
  * Выполнить
    
    ```python manage.py collectstatic```

  Для работы на локальном сервере вернуть изначальные настройки
+ Включить и активировать службу
    ```
    sudo systemctl start psdia
    sudo systemctl enable psdia
    ```
