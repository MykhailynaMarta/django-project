from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_classes):
    # Додаємо всі класи через пробіл
    classes = css_classes.split()
    current_classes = field.field.widget.attrs.get("class", "")
    all_classes = current_classes + " " + " ".join(classes) if current_classes else " ".join(classes)
    return field.as_widget(attrs={"class": all_classes})
