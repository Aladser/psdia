# Личный дневник

Веб-приложение для ведения личного дневника. 
Приложение позволяет пользователям создавать, редактировать и удалять записи в дневнике, просматривать свои записи в удобном интерфейсе. 

+ Все представления в CBV-стиле.

## Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными *.env.example*.
+ ``docker-compose up --build`` - пересобрать контейнеры
+ ``docker-compose up`` - запуск контейнеров

## Функционал сайта

+ Регистрация и аутентификация пользователей (приложение **authen**):
  * Пользователи должны иметь возможность зарегистрироваться, войти в систему и выйти из неё.
  * Модель ``User`` - пользователь: фамилия, имя, почта, телефон, аватар
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
  
+ Создание, редактирование и удаление записей в дневнике (приложение **diary**):
  * Авторизованные пользователи могут добавлять новые записи в дневник, редактировать существующие записи (только свои) и удалять ненужные записи.
  * Модель ``Record`` - запись: автор, содержание(заголовок), дата создания
  * Представления
    + ``RecordCreateView`` - создание записи

    ![Авторизация](/readme/RecordCreateView.png)

    + ``RecordUpdateView`` - обновление записи
    
    ![Авторизация](/readme/RecordUpdateView.png)

    + ``RecordDeleteView`` - удаление записи
    
    ![Авторизация](/readme/RecordDeleteView.png)

+ Просмотр записей:
  * Пользователи могут просматривать список всех своих записей.
  
    ``RecordListView`` - список записей пользователей.
  
    ![Авторизация](/readme/RecordListView.png)
  * Пользователи могут просматривать отдельные записи в подробном виде.
  
    ``RecordDetailView`` - детали записи
  
    ![Авторизация](/readme/RecordDetailView.png)
  * ![Авторизация](/readme/Permission_Denied.png)
  
  За права пользователей на просмотр записей отвечают миксины
    + ``libs.login_required_mixin.CustomLoginRequiredMixin`` - список записей
    + ``libs.object_permission_mixin.DetailObjectPermissionMixin`` - детали записи
    + ``libs.object_permission_mixin.UpdateDeleteObjectPermissionMixin`` - обновление или удаление записи
+ Поиск по записям: 
  * Возможность поиска записей по заголовку или содержимому в интерфейсе сайта.
  
  ``RecordListView.get_queryset()`` - если введется поиск по записям, get_queryset() выдает записи согласно GET-параметрам элементов поиска.
  Поиск введется по дате создания И/ИЛИ фразе
  ![Авторизация](/readme/RecordListView_phrase_and_date.png)
  ![Авторизация](/readme/RecordListView_date.png)
  ![Авторизация](/readme/RecordListView_phrase.png)



