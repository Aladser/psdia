import os
from secrets import token_hex

from django.contrib.auth.views import LoginView, PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from authen.forms import RegisterForm, AuthForm, ProfileForm, CustomPasswordResetForm, CustomSetPasswordForm
from authen.models import User
from authen.services import verificate_user
from authen.tasks import send_email
from config.settings import APP_NAME, EMAIL_HOST_USER
from libs.authen_mixin import AuthenMixin


# АВТОРИЗАЦИЯ
class UserLoginView(AuthenMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthForm

    extra_context = {
        'title': "авторизация",
        'header': "Авторизация пользователя",
    }


# РЕГИСТРАЦИЯ
class RegisterView(AuthenMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('authen:login')

    extra_context = {
        'title': "регистрация",
        'header': "Регистрация пользователя",
    }

    def form_valid(self, form):
        if form.is_valid():
            # создание ссылки подтверждения почты
            self.object = form.save()
            self.object.is_active = False
            self.object.token = token_hex(10)
            self.object.save()
            send_email.delay(self.object.email, self.object.token)
            return redirect(reverse_lazy("authen:register-complete"))

        return super().form_valid(form)


# ПРОФИЛЬ
class ProfileView(AuthenMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'user_form.html'
    success_url = '/'

    extra_context = {
        'title':  f"{os.getenv("APP_NAME")} - профиль  пользователя",
        'header': "Профиль пользователя",
    }

    def get_object(self, queryset=None):
        return self.request.user


# СБРОС ПАРОЛЯ - ОТПРАВКА ССЫЛКИ НА ПОЧТУ
class ManualPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('authen:password_reset_done')

    extra_context = {
        'title': "сброс пароля",
        'header': "Сброс пароля пользователя"
    }


# ВВОД НОВОГО ПАРОЛЯ
class ManualUserPasswordResetConfirmView(PasswordResetConfirmView):
    extra_context = {
        'title':  f"{os.getenv("APP_NAME")} - ввод нового пароля",
        'header': "Ввод нового пароля",
    }

    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('authen:password_reset_complete')

# ПРОВЕРКА ВВОДА НОВОГО ПАРОЛЯ
class ManualPasswordResetCompleteView(PasswordResetCompleteView):
    extra_context = {
        'title': f"{os.getenv("APP_NAME")} - ввод нового пароля",
        'header': "Ввод нового пароля",
    }


# ПОДТВЕРЖДЕНИЕ ПОЧТЫ
class VerificateEmailView(TemplateView):
    template_name = "information.html"
    extra_context = {
        'title':  f"подтверждение регистрации",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        if kwargs.get('token'):
            context['description'] = verificate_user(kwargs['token'])
        return context


# ЗАВЕРШЕНИЕ РЕГИСТРАЦИИ
class RegisterCompleteView(TemplateView):
    template_name = "register_complete.html"
    extra_context = {
        'title':  f"{os.getenv("APP_NAME")} - регистрация пользователя",
    }
