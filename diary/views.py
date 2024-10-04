from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView

from diary.forms import RecordForm
from diary.models import Record
from libs.login_required_mixin import ManualLoginRequiredMixin
from libs.object_permission_mixin import UpdateDeleteObjectPermissionMixin, DetailObjectPermissionMixin, \
    ListObjectPermissionMixin

month_name_list = [
    '', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября','декабря'
]

# LIST
class RecordListView(ListObjectPermissionMixin, ListView):
    title = 'список записей'
    extra_context = {
        'title': title,
        'header': title.capitalize(),
        'css_list': ['record_list.css'],
    }

    model = Record
    template_name = "record_list.html"
    paginate_by = 18

    def get_queryset(self):
        authuser = self.request.user
        queryset = super().get_queryset()
        return queryset if authuser.is_superuser else queryset.filter(owner=authuser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # урезание размера содержания
        for obj in context["object_list"]:
            obj.content = obj.content.replace("\n", "<br>")
            if len(obj.content) > 100:
                obj.content = obj.content[:100] + '..'

        return context

# CREATE
class RecordCreateView(ManualLoginRequiredMixin, CreateView):
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
class RecordDetailView(ManualLoginRequiredMixin, DetailObjectPermissionMixin, DetailView):
    model = Record
    template_name = "record_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'].content = context['object'].content.replace('\n', '<br>').replace(" ", "&nbsp;")

        created_at_obj = context['object'].created_at
        created_at = f"{created_at_obj.day} {month_name_list[created_at_obj.month]} {created_at_obj.year}г. {created_at_obj.hour}:{created_at_obj.minute}"

        context['title'] = created_at
        context['header'] = "Запись от " + created_at
        return context

# UPDATE
class RecordUpdateView(ManualLoginRequiredMixin, UpdateDeleteObjectPermissionMixin, UpdateView):
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
class RecordDeleteView(ManualLoginRequiredMixin, UpdateDeleteObjectPermissionMixin, DeleteView):
    title = 'удаление записи'
    extra_context = {
        'title': title,
        'header': title.capitalize(),
    }

    model = Record
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('diary:list')

