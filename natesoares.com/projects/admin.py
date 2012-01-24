from models import Project
from django.contrib import admin
from personal.tags.forms import taggable_model_form
    
class ProjectAdmin(admin.ModelAdmin):
   form = taggable_model_form(Project)

admin.site.register(Project, ProjectAdmin)
