# utils/forms_mixins.py

class StyleFormMixin:
    def add_form_control_class(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
