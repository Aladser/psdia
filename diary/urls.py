from django.urls import path
from diary.apps import PsdiaConfig
from diary.views import RecordListView, RecordDetailView, RecordCreateView

app_name = PsdiaConfig.name

urlpatterns = [
    path('', RecordListView.as_view(), name="list"),
    path('detail/<int:pk>', RecordDetailView.as_view(), name="detail"),
    path('create/', RecordCreateView.as_view(), name="create")
]
