## Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными *.env.example*.
+ ``python manage.py createusers`` - создать пользователей
+ ``python manage.py seed`` - сидирование таблиц
+ ``celery -A config worker -l INFO`` - запуск отложенных задач

