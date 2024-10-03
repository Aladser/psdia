from struct import pack_into

from django.views.generic import ListView, DetailView
from sqlparse.utils import consume

from diary.models import Record
from django.views.generic import ListView, DetailView

from diary.models import Record


# СПИСОК
class RecordListView(ListView):
    model = Record
    template_name = "record_list.html"
    title = 'записи'
    extra_context = {
        'title': title,
        'header': title.title(),
    }

    def get_queryset(self):
        authuser = self.request.user
        if str(authuser) == 'AnonymousUser':
            return Record.objects.none()

        queryset = super().get_queryset()
        return queryset if authuser.is_superuser else queryset.filter(owner=authuser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['css_list'] = ['record_list.css']

        # урезание размера содержания
        for obj in context["object_list"]:
            if len(obj.content) > 100:
                obj.content = obj.content[:100] + '..'

        return context

# ДЕТАЛИ
class RecordDetailView(DetailView):
    model = Record
    template_name = "record_detail.html"
    extra_context = {
        'title': "детали сообщения",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        created_at = context['object'].created_at.strftime("%d/%m/%Y %H:%M")
        context['title'] = created_at
        context['header'] = "Запись от " + created_at
        return context
