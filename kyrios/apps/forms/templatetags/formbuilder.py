from django import forms
from django.template.loader import get_template
from django import template

register = template.Library()

@register.filter
def build_form(element):
    markup_classes = {'label': '', 'value': '', 'single_value': ''}
    return render(element, markup_classes)

@register.filter
def add_input_classes(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) \
       and not is_radio(field) and not is_file(field):
        field_classes = field.field.widget.attrs.get('class', '')
        field_classes += ' form-control'
        field.field.widget.attrs['class'] = field_classes


def render(element, markup_classes):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        add_input_classes(element)
        template = get_template("formbuilder/field.html")
        context = {'field': element, 'classes': markup_classes, 'form': element.form}
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template = get_template("formbuilder/formset.html")
            context = {'formset': element, 'classes': markup_classes}
        else:
            for field in element.visible_fields():
                add_input_classes(field)

            template = get_template("formbuilder/form.html")
            context = {'form': element, 'classes': markup_classes}

    return template.render(context)


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_password(field):
    return isinstance(field.field.widget, forms.PasswordInput)

@register.filter
def is_image(field):
    return isinstance(field.field, forms.ImageField)