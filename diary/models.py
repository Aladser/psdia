from django.db import models
from authen.models import User
from config.settings import NULLABLE
from libs.truncate_table_mixin import TruncateTableMixin


class Record(TruncateTableMixin, models.Model):
    owner = models.ForeignKey(
        to=User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name='records',
    )
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Обновлен", auto_now=True)

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        ordering = ('owner', 'updated_at')

    def __str__(self):
        return self.content
