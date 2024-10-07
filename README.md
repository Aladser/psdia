# Личный дневник

Веб-приложение для ведения личного дневника. 
Приложение должно позволять пользователям создавать, редактировать и удалять записи в дневнике, 
а также просматривать свои записи в удобном интерфейсе. 

+ Все представления в CBV-стиле.

## Функционал сайта

+ Регистрация и аутентификация пользователей (приложение *authen*):
  * Пользователи должны иметь возможность зарегистрироваться, войти в систему и выйти из неё.
  * Модель ``User`` - пользователь: почта, телефон, аватар
  * Представления:
    + ``UserLoginView`` - авторизация. Форма ``AuthForm``
    
    ![Авторизация](/readme/AuthForm.png)
    + ``LogoutView`` - выход из системы. Стандаратное представление.
    + ``RegisterView`` - регистрация. Форма ``RegisterForm``
    
    ![Авторизация](/readme/RegisterForm.png)
    + ``ProfileView`` - профиль. Форма ``ProfileForm``
    
    ![Авторизация](/readme/ProfileForm.png)
    + ``CustomPasswordResetView`` - сброс пароля и отправка ссылки на сброс пароля на почту. Форма ``CustomPasswordResetForm``
    
    ![Авторизация](/readme/CustomPasswordResetForm.png)
    + ``CustomUserPasswordResetConfirmView`` - ввод нового пароля. Форма ``CustomSetPasswordForm``
    
    ![Авторизация](/readme/CustomSetPasswordForm.png)
    + ``CustomPasswordResetCompleteView`` - проверка ввода нового пароля
    + ``VerificateEmailView`` - подтверждение почты
    + ``RegisterCompleteView`` - завершение регистрации
  * Используется для всех шаблонов представлений базовый шаблон ``basic_auth``
  * Письмо подтверждения регистрации отправляется через отложенную функцию ``send_email()``
  
+ Создание, редактирование и удаление записей в дневнике:
  * Авторизованные пользователи могут добавлять новые записи в дневник, редактировать существующие записи (только свои) и удалять ненужные записи.
+ Просмотр записей:
  * Пользователи могут просматривать список всех своих записей.
  * Пользователи могут просматривать отдельные записи в подробном виде.
+ Поиск по записям: 
  * Возможность поиска записей по заголовку или содержимому в интерфейсе сайта.

## Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными *.env.example*. 
+ ``python manage.py createusers`` - создать пользователей
+ ``python manage.py seed`` - сидирование таблиц
+ ``celery -A config worker -l INFO`` - запуск отложенных задач


## Запуск на nginx (Ubuntu)
+ Настроить папку виртуального окружения так, чтобы путь до gurnicorn был:
``/venv/bin/gunicorn``
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
