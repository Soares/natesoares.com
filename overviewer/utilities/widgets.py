from django.forms.widgets import Textarea

class LargeTextarea(Textarea):
    def __init__(self, attrs=None):
        new_attrs = {'rows': 40, 'cols': 100, 'class': 'large'}
        if attrs:
            new_attrs.update(attrs)
        super(LargeTextarea, self).__init__(new_attrs)
