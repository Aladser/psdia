from datetime import datetime, timedelta

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView

from diary.forms import RecordForm
from diary.models import Record
from libs.login_required_mixin import CustomLoginRequiredMixin
from libs.object_permission_mixin import UpdateDeleteObjectPermissionMixin, DetailObjectPermissionMixin, \
    ListObjectPermissionMixin

month_name_list = [
    '', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
    'декабря'
]


# LIST
class RecordListView(ListObjectPermissionMixin, ListView):
    extra_context = {
        'header': 'Список записей',
        'css_list': ['record_list.css'],
    }

    model = Record
    template_name = "record_list.html"
    paginate_by = 18

    def get_queryset(self):
        # Показ своих записей, поиск записей

        if 'search_date' in self.request.GET and 'search_phrase' in self.request.GET and self.request.GET['search_date'] != '' and \
                self.request.GET['search_phrase'] != '':
            "по дате и фразе"

            created_at_start = datetime.strptime(self.request.GET['search_date'], "%Y-%m-%d").date()
            created_at_end = created_at_start + timedelta(hours=24)
            phrase = self.request.GET['search_phrase']
            queryset = super().get_queryset().filter(
                content__contains=phrase,
                created_at__gt=created_at_start,
                created_at__lt=created_at_end
            )
        elif 'search_date' in self.request.GET and self.request.GET['search_date'] != '':
            "по дате"

            created_at_start = datetime.strptime(self.request.GET['search_date'], "%Y-%m-%d").date()
            created_at_end = created_at_start + timedelta(hours=24)
            queryset = super().get_queryset().filter(
                created_at__gt=created_at_start,
                created_at__lt=created_at_end
            )
        elif 'search_phrase' in self.request.GET and self.request.GET['search_phrase'] != '':
            "по фразе"

            queryset = super().get_queryset().filter(content__contains=self.request.GET['search_phrase'])
        else:
            queryset = super().get_queryset()

        authuser = self.request.user
        return queryset if authuser.is_superuser else queryset.filter(owner=authuser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # поля поиска записей
        if 'search_date' in self.request.GET:
            context['search_date'] = self.request.GET['search_date']
            context['search_phrase'] = self.request.GET['search_phrase']

        # урезание размера содержания
        for obj in context["object_list"]:
            obj.content = obj.content.replace("\n", "<br>")
            if len(obj.content) > 100:
                obj.content = obj.content[:100] + '..'

        return context


# CREATE
class RecordCreateView(CustomLoginRequiredMixin, CreateView):
    title = "добавить запись"
    extra_context = {
        'title': title,
        'header': title.capitalize(),
    }

    model = Record
    form_class = RecordForm
    template_name = "record_form.html"

    def form_valid(self, form):
        if form.is_valid():
            content = form.__dict__['data']['content']
            owner = self.request.user
            self.object = Record.objects.create(owner=owner, content=content)
            return redirect(self.get_success_url())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("diary:detail", kwargs={"pk": self.object.pk})


# DETAIL
class RecordDetailView(CustomLoginRequiredMixin, DetailObjectPermissionMixin, DetailView):
    model = Record
    template_name = "record_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'].content = context['object'].content.replace('\n', '<br>')

        created_at_obj = context['object'].created_at
        created_at_hour = created_at_obj.hour if created_at_obj.hour > 9 else '0' + str(created_at_obj.hour)
        created_at_minute = created_at_obj.minute if created_at_obj.minute > 9 else '0' + str(created_at_obj.minute)
        created_at = f"{created_at_obj.day} {month_name_list[created_at_obj.month]} {created_at_obj.year}г. {created_at_hour}:{created_at_minute}"
        context['title'] = created_at
        context['header'] = "Запись от " + created_at
        return context


# UPDATE
class RecordUpdateView(CustomLoginRequiredMixin, UpdateDeleteObjectPermissionMixin, UpdateView):
    title = "обновить запись"
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }

    model = Record
    form_class = RecordForm
    template_name = 'record_form.html'

    def get_success_url(self):
        return reverse_lazy("diary:detail", kwargs={"pk": self.object.pk})


# DELETE
class RecordDeleteView(CustomLoginRequiredMixin, UpdateDeleteObjectPermissionMixin, DeleteView):
    title = 'удалить запись'
    extra_context = {
        'title': title,
        'header': title.capitalize(),
    }

    model = Record
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('diary:list')
