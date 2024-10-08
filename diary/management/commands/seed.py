from datetime import timedelta

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import datetime

from authen.management.commands.createusers import user_params_obj_list
from authen.models import User
from diary.models import Record
from libs.seeding import Seeding

user_list = [
    get_object_or_404(User, email=user_params_obj_list[1]['email']),
    get_object_or_404(User, email=user_params_obj_list[2]['email']),
    get_object_or_404(User, email=user_params_obj_list[3]['email'])
]

content_list = [
    "Сегодня утром гуляла по парку, слышала, как поют птицы. Чудесное время года!",
    "Сделала вечернюю пробежку и почувствовала прилив энергии. Это так воодушевляет!",
    "На работе меня похвалили за проект. Всегда приятно получать положительные отзывы.",
    "Недавно начала изучать новую специальность, это требует много сил и усердия, но я уверена, что справлюсь и добьюсь результатов.",
    "Планирую учебную поездку за границу, надеюсь, что смогу улучшить свои навыки и погрузиться в новую культуру, это всегда вдохновляет.",
    "В выходные мы с друзьями собираемся в горы, чтобы насладиться природой и активным отдыхом, это всегда приносит радость и новые впечатления.",
    "Провела вечер с родными, обсуждая планы на лето. Такие моменты укрепляют нашу связь и наполняют душу теплом.",
    "На днях прошел дождь, и я осталась дома, смотрела фильмы и пила чай, уютный вечер, которого так ждала.",
    "Познакомилась с интересным человеком. Его истории о путешествиях были настолько захватывающими, что я не заметила, как пролетело время."
]

record_params_obj_list = []
ri = 0
for i in range(3):
    for j in range(3):
        record_params_obj_list.append({'owner': user_list[j], 'content': content_list[ri]})
        ri += 1


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Seeding.seed_table(Record, record_params_obj_list)

        # разное время для записей
        created_at = datetime.now()
        for record in Record.objects.all():
            record.created_at = created_at
            record.save()
            created_at -= timedelta(days=1)
