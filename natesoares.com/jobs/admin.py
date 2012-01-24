from models import Job
from django.contrib import admin
from personal.tags.forms import taggable_model_form
    
class JobAdmin(admin.ModelAdmin):
    form = taggable_model_form(Job)

admin.site.register(Job, JobAdmin)
