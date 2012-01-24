from django.contrib import admin
from django.db.models import TextField
from django.forms.widgets import Textarea
from models import Entry

class LargeTextarea(Textarea):
    def __init__(self, attrs={}):
        attrs = dict({'rows': 40, 'cols': 100, 'class': 'large'}, **attrs)
        super(LargeTextarea, self).__init__(attrs)
    
class EntryAdmin(admin.ModelAdmin):
    model = Entry
    exclude = 'outgoing',
    list_filter = 'published',
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = {TextField: {'widget': LargeTextarea}}

admin.site.register(Entry, EntryAdmin)
