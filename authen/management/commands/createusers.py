from django.core.management import BaseCommand

from authen.models import User
from libs.seeding import Seeding

user_dict = [
    {
        'email': 'admin@test.ru',
        'first_name': 'Админ',
        'last_name': 'Админов',
        'is_superuser': True,
        'is_staff': True
    },
    {
        'email': 'user@test.ru',
        'first_name': 'Пользователь',
        'last_name': 'Обычный',
    }
]


class Command(BaseCommand):
    password = '_strongpassword_'

    def handle(self, *args, **kwargs):
        Seeding.seed_users(User, user_dict, self.password)
