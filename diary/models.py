from django.db import models
from authen.models import User


class Record(models.Model):
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
        return f"{self.owner} {self.updated_at}: {self.content}"
