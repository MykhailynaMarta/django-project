from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_classes):
    # Додаємо всі класи через пробіл
    classes = css_classes.split()
    current_classes = field.field.widget.attrs.get("class", "")
    all_classes = current_classes + " " + " ".join(classes) if current_classes else " ".join(classes)
    return field.as_widget(attrs={"class": all_classes})

@register.filter
def attr(obj, attr_name):
    """Фільтр для отримання атрибутів моделі"""
    return getattr(obj, attr_name, None)

@register.filter
def get_pk(obj):
    # Перевіряємо, чи є у об'єкта атрибут '_meta', щоб бути впевненим, що це модель
    if hasattr(obj, '_meta'):
        return getattr(obj, obj._meta.pk.name)
    return None

@register.filter
def getattr_safe(obj, attr):
    try:
        return getattr(obj, attr, None)
    except AttributeError:
        return None