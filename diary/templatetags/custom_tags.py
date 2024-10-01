import os.path
from django import template
from config.settings import BASE_DIR, MEDIA_URL, STATIC_URL, APP_NAME

register = template.Library()


@register.filter()
def site_name_prefix(value):
    return f"{APP_NAME} - {value}" if value != '' else APP_NAME


@register.filter()
def full_image_path(image_file):
    if image_file != '' and os.path.isfile(BASE_DIR / MEDIA_URL.replace('/', '') / str(image_file)):
        return MEDIA_URL + str(image_file)
    else:
        return STATIC_URL + "empty_file.png"


@register.filter()
def format_datetime(datetime):
    return datetime.strftime("%d-%m-%Y %H:%M")


@register.filter()
def is_published(value):
    if value:
        return f"<span class='text-success'>Да</span>"
    else:
        return f"<span class='text-secondary'>Нет</span>"


@register.filter()
def top_menu_elem(value, section):
    """пункт главного меню"""
    if value == section and section is not None:
        return f"<span class='btn btn-outline-primary'>{value}</span>"
    else:
        return value


@register.filter()
def publish_action(value):
    return 'Снять с публикации' if value else 'Опубликовать'


@register.filter()
def product_version(value, version):
    return f"{value} {version}" if version else value


@register.filter()
def price(value):
    return f"{value} руб." if value else 'нет цены'


@register.filter()
def custom_label(value, required_fields):
    if value in required_fields:
        return f"<label class='fw-bolder' title='обязательно для заполнения'>{value}:*</label>"
    else:
        return f"<label>{value}:</label>"


@register.filter()
def author(value):
    return value if value else "без автора"
