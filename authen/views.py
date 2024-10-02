from secrets import token_hex
from urllib.request import Request

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from authen.forms import RegisterForm, AuthForm, ProfileForm, CustomPasswordResetForm, CustomSetPasswordForm
from authen.models import User
from config.settings import APP_NAME, EMAIL_HOST_USER
from libs.authen_mixin import AuthenMixin


# АВТОРИЗАЦИЯ
class UserLoginView(AuthenMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthForm

    title = "Авторизация"
    extra_context = {
        'section': title,
        'header': title.title,
        'title': title
    }


# РЕГИСТРАЦИЯ
class RegisterView(AuthenMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('authen:login')

    title = "Регистрация"
    extra_context = {
        'section': 'register',
        'header': title,
        'title': title
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

            header = 'Регистрация успешно завершена!'
            description = 'Ссылка для подтверждения регистрации отправлена на вашу почту.'
            return render(
                self.request,
                'information.html',
                {'header': header, 'description': description}
            )

        return super().form_valid(form)


# ПРОФИЛЬ
class ProfileView(AuthenMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'user_form.html'
    success_url = '/'

    title = "профиль пользователя"
    extra_context = {
        'section': 'profile',
        'header': title.title(),
        'title': title
    }

    def get_object(self, queryset=None):
        return self.request.user


# СБРОС ПАРОЛЯ - ОТПРАВКА ССЫЛКИ НА ПОЧТУ
class ManualPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('authen:password_reset_done')

    title = "Сброс пароля"
    extra_context = {
        'section': title,
        'header': title,
        'title': title
    }


# ВВОД НОВОГО ПАРОЛЯ
class CustomUserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('authen:password_reset_complete')


# ПОДТВЕРЖДЕНИЕ ПОЧТЫ
def verificate_email_view(request: Request, token: str) -> HttpResponse:
    """подтверждение почты"""

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
