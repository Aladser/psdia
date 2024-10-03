import os

from django.shortcuts import render
from django.views.generic import ListView

from diary.models import Record


def index(request):
    return render(request, "index.html", {'header': 'Главная страница'})


# СПИСОК РАССЫЛОК
class RecordListView(ListView):
    model = Record
    template_name = "list.html"
    extra_context = {
        'title': 'записи',
        'header': "Записи",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # урезание размера содержания
        for obj in context["object_list"]:
            if len(obj.content) > 100:
                obj.content = obj.content[:100] + '..'

        return context
