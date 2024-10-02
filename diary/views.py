import os

from django.shortcuts import render
from dotenv import load_dotenv

def index(request):
    return render(request, "index.html", {'header': os.getenv('APP_NAME')})
