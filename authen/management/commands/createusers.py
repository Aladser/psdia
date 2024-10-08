from django.core.management import BaseCommand

from authen.models import User
from config.settings import PHOTO_NOT_FOUND
from libs.seeding import Seeding

user_params_obj_list = [
    {
        'email': 'admin@test.ru',
        'first_name': 'Админ',
        'last_name': 'Админов',
        'is_superuser': True,
        'avatar': PHOTO_NOT_FOUND,
        'is_staff': True
    },
    {
        'email': 'user1@test.ru',
        'first_name': 'Пользователь 1',
        'last_name': 'Обычный',
        'avatar': PHOTO_NOT_FOUND,
    },
    {
        'email': 'user2@test.ru',
        'first_name': 'Пользователь 2',
        'last_name': 'Обычный',
        'avatar': PHOTO_NOT_FOUND,
    },
    {
        'email': 'user3@test.ru',
        'first_name': 'Пользователь 3',
        'last_name': 'Обычный',
        'avatar': PHOTO_NOT_FOUND,
    }
]

password = '_strongpassword_'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Seeding.seed_users(User, user_params_obj_list, password)
