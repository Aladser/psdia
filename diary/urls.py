from django.urls import path

from diary.apps import PsdiaConfig
from diary.views import index

app_name = PsdiaConfig.name

urlpatterns = [
    path('', index, name="index")
]
