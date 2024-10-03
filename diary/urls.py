from django.urls import path

from diary.apps import PsdiaConfig
from diary.views import RecordListView

app_name = PsdiaConfig.name

urlpatterns = [
    path('', RecordListView.as_view(), name="index")
]
