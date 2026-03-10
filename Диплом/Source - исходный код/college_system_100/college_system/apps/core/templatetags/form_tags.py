from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css):
    """Добавляет CSS‑класс к виджету поля формы."""
    return field.as_widget(attrs={**field.field.widget.attrs, "class": css})


@register.filter(name="get_item")
def get_item(dictionary, key):
    """Получить значение из словаря по ключу."""
    if dictionary is None:
        return None
    return dictionary.get(key)


