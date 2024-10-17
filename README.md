# Личный дневник

Веб-приложение для ведения личного дневника. 

Приложение позволяет пользователям создавать, редактировать и удалять записи в дневнике, просматривать свои записи в удобном интерфейсе.

## Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными *.env.example*.
+ ``python manage.py seed`` - сидирование таблиц
+ ``celery -A config worker -l INFO`` - запуск периодической задачи

## Запуск на nginx, Ubuntu:
  + Поменять в *config/settings.py*
  ```
  #STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
  ```
  на
  ```
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  #STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
  ```
  + ``python manage.py collectstatic``
  + Для работы локального сервера вернуть настройки обратно
  + ``sudo cp /var/www/install/psdia.service /etc/systemd/system/psdia.service``
  + ``sudo systemctl start psdia``
  + ``sudo systemctl enable psdia``
  + ``sudo cp /var/www/install/psdia /etc/nginx/sites-available/psdia``
  + ``sudo ln -s /etc/nginx/sites-available/psdia /etc/nginx/sites-enabled/psdia``
  + ``sudo systemctl restart nginx``
  

После копирования вернуть обратно для работы локального сервера

## Функционал сайта

+ Регистрация и аутентификация пользователей (приложение **authen**):
  * Пользователи должны иметь возможность зарегистрироваться, войти в систему и выйти из неё.
  * Модель ``User`` - пользователь: фамилия, имя, почта, телефон, аватар
  * Представления:
    + ``UserLoginView`` - авторизация. Форма ``AuthForm``
    
    ![UserLoginView](/readme/AuthForm.png)
    + ``LogoutView`` - выход из системы. Стандаратное представление.
    + ``RegisterView`` - регистрация. Форма ``RegisterForm``
    
    ![RegisterView](/readme/RegisterForm.png)
    + ``ProfileView`` - профиль. Форма ``ProfileForm``
    
    ![ProfileView](/readme/ProfileForm.png)
    + ``CustomPasswordResetView`` - сброс пароля и отправка ссылки на сброс пароля на почту. Форма ``CustomPasswordResetForm``
    
    ![CustomPasswordResetView](/readme/CustomPasswordResetForm.png)
    + ``CustomUserPasswordResetConfirmView`` - ввод нового пароля. Форма ``CustomSetPasswordForm``
    
    ![CustomUserPasswordResetConfirmView](/readme/CustomSetPasswordForm.png)
    + ``CustomPasswordResetCompleteView`` - проверка ввода нового пароля
    + ``VerificateEmailView`` - подтверждение почты
    + ``RegisterCompleteView`` - завершение регистрации
  * Используется для всех шаблонов представлений базовый шаблон ``basic_auth``
  * Письмо подтверждения регистрации отправляется через отложенную функцию ``send_email()``
  
+ Создание, редактирование и удаление записей в дневнике (приложение **diary**):
  * Авторизованные пользователи могут добавлять новые записи в дневник, редактировать существующие записи (только свои) и удалять ненужные записи.
  * Модель ``Record`` - запись: автор, содержание(заголовок), дата создания
  * Представления
    + ``RecordCreateView`` - создание записи

    ![RecordCreateView](/readme/RecordCreateView.png)

    + ``RecordUpdateView`` - обновление записи
    
    ![RecordUpdateView](/readme/RecordUpdateView.png)

    + ``RecordDeleteView`` - удаление записи
    
    ![RecordDeleteView(/readme/RecordDeleteView.png)

+ Просмотр записей:
  * Пользователи могут просматривать список всех своих записей.
  
    ``RecordListView`` - список записей пользователей.
  
    ![RecordListView](/readme/RecordListView.png)
  * Пользователи могут просматривать отдельные записи в подробном виде.
  
    ``RecordDetailView`` - детали записи
  
    ![RecordDetailView](/readme/RecordDetailView.png)

  За права пользователей на просмотр записей отвечают миксины
    + ``libs.object_permission_mixin.ListObjectPermissionMixin`` - список записей. Если пользователь не авторизован, показывается стандартная главная страница.
    + ``libs.object_permission_mixin.DetailObjectPermissionMixin`` - детали записи. Проверяютс права на просмотр страницы записи.
    + ``libs.object_permission_mixin.UpdateDeleteObjectPermissionMixin`` - обновление или удаление записи. Проверка прав на обновление или удаление записи.
    ![Permission_Denied](/readme/Permission_Denied.png)
  
+ Поиск по записям: 
  * Возможность поиска записей по заголовку или содержимому в интерфейсе сайта.
  
  ``RecordListView.get_queryset()`` - если введется поиск по записям, get_queryset() выдает записи согласно GET-параметрам элементов поиска.
  Поиск введется по дате создания И/ИЛИ фразе
  ![RecordListView_phrase_and_date](/readme/RecordListView_phrase_and_date.png)
  ![RecordListView_date](/readme/RecordListView_date.png)
  ![RecordListView_phrase](/readme/RecordListView_phrase.png)



