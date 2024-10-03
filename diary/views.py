from django.views.generic import ListView

from diary.models import Record


# СПИСОК ЗАПИСЕЙ
class RecordListView(ListView):
    model = Record
    template_name = "list.html"
    title = 'записи'
    extra_context = {
        'title': title,
        'header': title.title(),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # урезание размера содержания
        for obj in context["object_list"]:
            if len(obj.content) > 100:
                obj.content = obj.content[:100] + '..'

        return context

