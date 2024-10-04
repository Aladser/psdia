from django import template

from config.settings import APP_NAME

register = template.Library()


@register.filter()
def site_name_prefix(value):
    return f"{APP_NAME} - {value}" if value != '' else APP_NAME


@register.filter()
def format_datetime(datetime):
    return datetime.strftime("%d-%m-%Y %H:%M")


@register.filter()
def custom_label(value, required_fields):
    if value in required_fields:
        return f"<label class='fw-bolder' title='обязательно для заполнения'>{value}:*</label>"
    else:
        return f"<label>{value}:</label>"
