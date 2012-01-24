from personal.tags.forms import taggable_model_form
from django.contrib import admin
from models import Entry
    
class EntryAdmin(admin.ModelAdmin):
    form = taggable_model_form(Entry)

admin.site.register(Entry, EntryAdmin)
