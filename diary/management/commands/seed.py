from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

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
    'Сегодня солнце светило ярко, а в сердце поселилась надежда. Новый день — новые возможности!',
    'Встреча с другом напомнила, как важно ценить моменты. Смех скрасил серый день.',
    'Пока шёл дождь, я мечтал. Иногда просто нужно остановиться и послушать свои мысли.',
    'Успех сегодня — это шаг к мечте. Маленькие победы добавляют сил для больших свершений.',
    'Прогулка в парке подарила спокойствие. Природа — лучший лекарь для уставшей души.',
    'Сегодня начала новое хобби. Рисование помогает выразить то, что не могу сказать словами.',
    'Провела вечер с книгой. Погружение в другую реальность — идеальный способ сбежать от рутины.',
    'Позвонила бабушке. Её голос наполнил сердце теплом и любовью. Семья — это важно.',
    'Сделала утреннюю пробежку. Чувствую себя энергично и готова к новым приключениям!'
]

record_params_obj_list = []
ri = 0
for i in range(3):
    for j in range(3):
        record_params_obj_list.append({'owner':user_list[j], 'content':content_list[ri]})
        ri+=1

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Seeding.seed_table(Record, record_params_obj_list)
