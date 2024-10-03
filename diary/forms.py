from django.forms import ModelForm
from diary.models import Record


class RecordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # стилизация полей
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control text-danger'
            field.widget.attrs['placeholder'] = "Напишите, о чем вы думаете"

    class Meta:
        model = Record
        fields = ('content',)
