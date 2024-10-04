from django.urls import path
from diary.apps import PsdiaConfig
from diary.views import RecordListView, RecordDetailView, RecordCreateView, RecordDeleteView, RecordUpdateView, SearchView

app_name = PsdiaConfig.name

urlpatterns = [
    path('', RecordListView.as_view(), name="list"),
    path('detail/<int:pk>', RecordDetailView.as_view(), name="detail"),
    path('create/', RecordCreateView.as_view(), name="create"),
    path('delete/<int:pk>', RecordDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>', RecordUpdateView.as_view(), name='edit'),
    path('search/', SearchView.as_view(), name='search'),
]
