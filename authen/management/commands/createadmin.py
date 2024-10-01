from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from authen.models import User, Country
from libs.seeding import Seeding


class Command(BaseCommand):
    country_obj_list = [
        {'pk': 1, 'name': 'russia', 'description': 'Россия'},
        {'pk': 2, 'name': 'ukraine', 'description': 'Украина'},
        {'pk': 3, 'name': 'belarus', 'description': 'Беларусь'},
        {'pk': 4, 'name': 'kazakhstan', 'description': 'Казахстан'},
        {'pk': 5, 'name': 'armenia', 'description': 'Армения'},
    ]
    user_dict = [
        {
            'email': 'admin@test.ru',
            'first_name': 'Админ',
            'last_name': 'Админов',
            'is_superuser': True,
            'is_staff': True
        }
    ]
    password = '_strongpassword_'

    def handle(self, *args, **kwargs):
        Seeding.seed_table(Country, self.country_obj_list)
        self.user_dict[0]['country'] = get_object_or_404(Country, name='russia')
        Seeding.seed_users(User, self.user_dict, self.password)
