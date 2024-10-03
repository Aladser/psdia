from pydoc import replace

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView

from diary.forms import RecordForm
from diary.models import Record


# LIST
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
            obj.content = obj.content.replace("\n", "<br>")
            if len(obj.content) > 100:
                obj.content = obj.content[:100] + '..'

        return context

# CREATE
class RecordCreateView(CreateView):
    title = "добавить запись"
    extra_context = {
        'title': title,
        'header': title.title()
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
class RecordDetailView(DetailView):
    model = Record
    template_name = "record_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'].content = context['object'].content.replace('\n', '<br>').replace(" ", "&nbsp;")

        created_at = context['object'].created_at.strftime("%d/%m/%Y %H:%M")
        context['title'] = created_at
        context['header'] = "Запись от " + created_at
        return context
