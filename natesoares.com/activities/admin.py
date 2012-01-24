from models import Activity
from django.contrib import admin
from personal.tags.forms import taggable_model_form
    
class ActivityAdmin(admin.ModelAdmin):
    form = taggable_model_form(Activity)

admin.site.register(Activity, ActivityAdmin)
