from django import db
from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from django.contrib.contenttypes import generic
from utilities.widgets import LargeTextarea
from datetime import datetime
import models

class EntryAdmin(admin.ModelAdmin):
    list_filter = 'published',
    search_fields = 'name',
    exclude = 'entry_added',

    formfield_overrides = {db.models.TextField: {'widget': LargeTextarea}}

    def publish(self, request, queryset):
        map(lambda e: e.publish(), queryset)
    publish.short_description = 'Mark selected enrties as published'
    
    actions = [publish]


class SubentryAdmin(admin.StackedInline):
    formfield_overrides = {db.models.TextField: {'widget': LargeTextarea}}
    extra = 1


# Writing
    

class WritingEntryAdmin(SubentryAdmin):
    model = models.WritingEntry


class WritingAdmin(EntryAdmin):
    model = models.Writing
    inlines = [WritingEntryAdmin]


# Projects


class ProjectEntryAdmin(SubentryAdmin):
    model = models.ProjectEntry


class ProjectAdmin(EntryAdmin):
    model = models.Project
    inlines = [ProjectEntryAdmin]


# Activities


class ActivityEntryAdmin(SubentryAdmin):
    model = models.ActivityEntry


class ActivityAdmin(EntryAdmin):
    model = models.Activity


# Jobs


class JobEntryAdmin(SubentryAdmin):
    model = models.JobEntry


class JobAdmin(EntryAdmin):
    model = models.Job


# Tutorials


class TutorialSectionInline(generic.GenericStackedInline):
    formfield_overrides = {db.models.TextField: {'widget': LargeTextarea}}
    model = models.TutorialSection
    extra = 1


class TutorialSectionAdmin(EntryAdmin):
    model = models.TutorialSection
    inlines = [TutorialSectionInline]
    list_display = 'informative_name',
    exclude = 'object_id', 'content_type'


class TutorialAdmin(EntryAdmin):
    model = models.Tutorial
    inlines = [TutorialSectionInline]


# Registration


admin.site.register(models.Writing, WritingAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.Job, JobAdmin)
admin.site.register(models.Tutorial, TutorialAdmin)
admin.site.register(models.TutorialSection, TutorialSectionAdmin)
