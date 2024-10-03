from celery import shared_task


@shared_task
def send_message():
    """Отправляет отложенно почтовое сообщение """


