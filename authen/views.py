import os
from secrets import token_hex
from urllib.request import Request

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from authen.forms import RegisterForm, AuthForm, ProfileForm, CustomPasswordResetForm, CustomSetPasswordForm
from authen.models import User
from config.settings import APP_NAME, EMAIL_HOST_USER
from libs.authen_mixin import AuthenMixin


# АВТОРИЗАЦИЯ
class UserLoginView(AuthenMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthForm

    extra_context = {
        'title': f"{os.getenv('APP_NAME')} - авторизация",
        'header': "Авторизация пользователя",
    }


# РЕГИСТРАЦИЯ
class RegisterView(AuthenMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('authen:login')

    extra_context = {
        'title': f"{os.getenv('APP_NAME')} -  регистрация",
        'header': "Регистрация пользователя",
    }

    def form_valid(self, form):
        if form.is_valid():
            # создание ссылки подтверждения почты
            self.object = form.save()
            self.object.is_active = False
            self.object.token = token_hex(10)
            self.object.save()

            url = f"http://{self.request.get_host()}/user/email-confirm/{self.object.token}"
            send_mail(
                "Подтвердите свою почту",
                f"Пройдите по ссылке {url} для подтверждения регистрации на сайте {APP_NAME}",
                EMAIL_HOST_USER,
                (self.object.email,),
                fail_silently=True
            )

            return redirect(reverse_lazy("authen:register-complete"))

        return super().form_valid(form)


# ПРОФИЛЬ
class ProfileView(AuthenMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'user_form.html'
    success_url = '/'

    title = "профиль пользователя"
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
        'title': f"{os.getenv('APP_NAME')} - сброс пароля",
        'header': "Сброс пароля"
    }


# ВВОД НОВОГО ПАРОЛЯ
class CustomUserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('authen:password_reset_complete')


# ПОДТВЕРЖДЕНИЕ ПОЧТЫ
def verificate_email_view(request: Request, token: str) -> HttpResponse:
    """Подтверждение почты"""

    if User.objects.filter(token=token).exists():
        user = User.objects.get(token=token)
        user.is_active = True
        user.token = None
        user.save()

        title = 'Почта успешно подтверждена'
    else:
        title = 'Ссылка недействительная'

    return render(
        request,
        'information.html',
        {
            'section': 'confirmation',
            'title': title,
            'header': title,
        }
    )

# ЗАВЕРШЕНИЕ РЕГИСТРАЦИИ
class RegisterCompleteView(TemplateView):
    template_name = "register_complete.html"
    extra_context = {
        'header': "Регистрация пользователя",
        'title': os.getenv("APP_NAME") + " - регистрация"
    }
