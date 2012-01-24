from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from personal.utilities import template
from personal.tags.models import Tag, TagLink
from personal.utilities.views import top
from personal.writing.models import Entry

register = template.Library()

@register.simple_tag
def describe_projects():
    return Project.display_name


@register.simple_tag
def describe_activities():
    return Activity.display_name


@register.simple_tag
def describe_jobs():
    return Job.display_name


@register.simple_setter
def recent_writing_updates(count):
    return Entry.objects.order_by('-published')[:count]


@register.simple_setter
def popular_writing_tags(count):
	entrytype = ContentType.objects.get_for_model(Entry)
	tag_ids = TagLink.objects.filter(content_type=entrytype).values_list('tag_id', flat=True)
	tags = Tag.objects.filter(id__in=tag_ids).annotate(Count('links'))
	return tags.order_by('links__count', 'name')[:int(count)]
