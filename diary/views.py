import os

from django.shortcuts import render


def index(request):
    return render(request, "index.html", {'header': 'Главная страница'})
