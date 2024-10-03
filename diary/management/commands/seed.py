from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from authen.management.commands.createusers import user_params_obj_list
from authen.models import User

users_list = [
    get_object_or_404(User, email=user_params_obj_list[1]['email']),
    get_object_or_404(User, email=user_params_obj_list[2]['email']),
    get_object_or_404(User, email=user_params_obj_list[3]['email']),
]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        [print(user) for user in users_list]
